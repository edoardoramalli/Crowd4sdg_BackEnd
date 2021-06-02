from Filter.Filters.Filter import Filter
import caffe
import numpy as np
from io import StringIO, BytesIO
from PIL import Image
import os
from django.conf import settings


class NSFWClassifier(Filter):

    def __init__(self):

        Filter.__init__(self)
        self.name = "nsfw"
        self.net = caffe.Net(os.path.join(settings.BASE_DIR, 'Files/FilterModels/deploy.prototxt'),
                             # pylint: disable=invalid-name
                             os.path.join(settings.BASE_DIR, 'Files/FilterModels/resnet_50_1by2_nsfw.caffemodel'),
                             caffe.TEST)

        # Load transformer
        # Note that the parameters are hard-coded for best results
        self.caffe_transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
        self.caffe_transformer.set_mean('data',
                                        np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
        self.caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
        self.caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

    def resize_image(self, data, sz=(256, 256)):
        """
        Resize image. Please use this resize logic for best results instead of the
        caffe, since it was used to generate training dataset
        :param str data:
            The image data
        :param sz tuple:
            The resized image dimensions
        :returns bytearray:
            A byte array with the resized image
        """
        '''img_data = str(data)
        im = Image.open(StringIO(img_data))
        if im.mode != "RGB":
            im = im.convert('RGB')'''
        imr = data.resize(sz, resample=Image.BILINEAR)
        fh_im = BytesIO()
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)
        return bytearray(fh_im.read())

        # img_resized = data.resize(sz, resample=Image.BILINEAR)
        # img_bytes = BytesIO()
        # # Try
        # img_resized.save(img_bytes, format='JPEG')
        # img_bytes = img_bytes.getvalue()
        # return bytearray(img_bytes.read())



    def classify(self, pil_image):
        """
        Run a Caffe network on an input image after preprocessing it to prepare
        it for Caffe.
        :param PIL.Image pimg:
            PIL image to be input into Caffe.
        :param caffe.Net caffe_net:
            A Caffe network with which to process pimg afrer preprocessing.
        :param list output_layers:
            A list of the names of the layers from caffe_net whose outputs are to
            to be returned.  If this is None, the default outputs for the network
            are returned.
        :return:
            Returns the requested outputs from the Caffe net.
        """
        output_layers = ['prob']

        if self.net is not None:

            img_data_rs = self.resize_image(pil_image, sz=(256, 256))
            image = caffe.io.load_image(StringIO(img_data_rs))

            H, W, _ = image.shape
            _, _, h, w = self.net.blobs['data'].data.shape
            h_off = max((H - h) / 2, 0)
            w_off = max((W - w) / 2, 0)
            crop = image[h_off:h_off + h, w_off:w_off + w, :]
            transformed_image = self.caffe_transformer.preprocess('data', crop)
            transformed_image.shape = (1,) + transformed_image.shape

            input_name = self.net.inputs[0]
            all_outputs = self.net.forward_all(blobs=output_layers,
                                               **{input_name: transformed_image})

            outputs = all_outputs[output_layers[0]][0].astype(float)

            return outputs[1] < 0.2, (1 - outputs[1]), None
        else:
            return False, 0, None

