import os
from django.conf import settings
import numpy as np
import sys

from Filter.Filters.Filter import Filter

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#
# # Keras outputs warnings using `print` to stderr so let's direct that to devnull temporarily
# stderr = sys.stderr
# sys.stderr = open(os.devnull, 'w')



# import keras
# from keras.applications import VGG19
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Activation


# sys.stderr = stderr


class MemeDetector(Filter):

    def __init__(self):

        Filter.__init__(self)
        self.name = "meme"

        # creating an object of vgg19 model and discarding the top layer
        model_vgg19 = VGG19(include_top=False,
                            weights=os.path.join(settings.BASE_DIR,
                                                 "Files/FilterModels/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5"),
                            input_shape=(150, 150, 3))
        # copy vgg19 layers into our model
        self.model = Sequential()
        for layer in model_vgg19.layers:
            self.model.add(layer)

        # freezing vgg19 layers (saving its original weights)
        for i in self.model.layers:
            i.trainable = False

        self.model.add(Flatten())
        self.model.add(Dense(10))
        self.model.add(Activation('relu'))
        self.model.add(Dense(2, activation='softmax'))

        self.model.load_weights(os.path.join(settings.BASE_DIR, "Files/FilterModels/ImgMemeWeights.h5"))

    def classify(self, pil_image):
        pil_image = pil_image.resize((150, 150))
        img_array = np.array(pil_image)
        img_array = np.expand_dims(img_array, 0)
        img_array = img_array / 255.

        predictions = self.model.predict(img_array)[0]
        is_image = predictions[0]
        is_meme = predictions[1]

        # Returns true (prediction < 0.5 ) if image is not a Meme
        return is_image > is_meme, np.max([is_image, is_meme]), None
