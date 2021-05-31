import pickle
import numpy as np
from Filter.Filters.Filter import Filter
import os
from django.conf import settings
import caffe


class PublicPrivateClassifier(Filter):
    PRIVATE_SCENES = ['balcony', 'bathroom', 'beach_house', 'bedroom', 'car_interior', 'chalet', 'clean_room', 'close',
                      'computer_room',
                      'corridor', 'conference_room', 'dining_room', 'dressing_room', 'elevator_shaft', 'entrance_hall',
                      'home_office',
                      'hotel_room', 'house', 'jacuzzi', 'kitchen', 'laundromat', 'living_room', 'mansion',
                      'manufactured_home', 'mezzanine',
                      'nursery', 'office', 'patio', 'playroom', 'porch', 'recreation_room', 'sauna', 'shed', 'shower',
                      'storage_room',
                      'television_room', 'throne_room', 'tree_house', 'underwater', 'utility_room']

    def __init__(self):

        Filter.__init__(self)
        self.name = "public_private"
        self.net = caffe.Net(os.path.join(settings.BASE_DIR, 'Files/FilterModels/deploy_alexnet_places365.prototxt'),
                             os.path.join(settings.BASE_DIR, 'Files/FilterModels/alexnet_places365.caffemodel'),
                             caffe.TEST)

        # load input and configure preprocessing
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_mean('data', np.load(
            os.path.join(settings.BASE_DIR, 'Files/FilterModels/ilsvrc_2012_mean.npy')).mean(1).mean(1))  # TODO - remove hardcoded path
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_channel_swap('data', (2, 1, 0))
        self.transformer.set_raw_scale('data', 255.0)

        # since we classify only one image, we change batch size from 10 to 1
        self.net.blobs['data'].reshape(1, 3, 227, 227)

        self.detailed_output = False

    def classify(self, pil_image):

        img = np.array(pil_image) / 255.

        # initialize net

        # load the image in the data layer
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', img)

        # compute
        out = self.net.forward()

        private_scenes = 0
        scene = ''

        # print top 5 predictions - TODO return as bytearray?
        with open(os.path.join(settings.BASE_DIR, 'Files/FilterModels/labels.pkl'), 'rb') as f:

            labels = pickle.load(f)
            top_k = self.net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
            # print self.net.blobs['prob']
            # print self.net.blobs['prob'].shape

            scene = str(labels[top_k[0]])

            for i, k in enumerate(top_k):
                if str(labels[k]) in self.PRIVATE_SCENES:
                    private_scenes += (k - i)

        if private_scenes >= k:
            return False, 0, scene
        else:
            return True, 1, scene
