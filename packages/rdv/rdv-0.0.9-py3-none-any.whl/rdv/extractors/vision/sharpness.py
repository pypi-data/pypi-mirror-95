from PIL import ImageFilter
import numpy as np

from rdv.extractors import FeatureExtractor


class Sharpness(FeatureExtractor):
    """Measures the blurryness or sharpness of an iamge. Based on
    https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
    """

    def __init__(self):
        pass

    def extract_feature(self, data):
        img = data
        img = img.convert("L")
        filtered = img.filter(ImageFilter.Kernel((3, 3), (0, 1, 0, 1, -4, 1, 0, 1, 0), scale=1, offset=0))
        return float(np.array(filtered).mean())  # .var())

    """Serializable inteface """

    def to_jcr(self):
        return {}

    @classmethod
    def from_jcr(cls, jcr):
        return cls()

    """Buildable interface"""

    def build(self, data):
        pass

    def is_built(self):
        return True
