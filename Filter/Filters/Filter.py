from Filter.Filters import *


class Filter:

    def __init__(self):
        pass

    def __call__(self, name):
        if name == 'PeopleDetector':
            f = PeopleDetector()
        # elif name == 'PublicPrivateClassifier':
        #     f = PublicPrivateClassifier()
        # elif name == 'NSFWClassifier':
        #     f = NSFWClassifier()
        elif name == "MemeDetector":
            f = MemeDetector()
        return f

    def classify(self, pil_image):
        """
        This is an abstract method to be implemented by a filter class.
        According to the implemented filter, it returns True if the image passes the filter, False otherwise.
        :param img: PIL Image to filter
        :return: True if the image passes the filter, false otherwise
        """
        pass
