from PIL import Image
import numpy as np


from rdv.extractors import FeatureExtractor
from rdv.globals import DataException
from rdv.feature import IntFeature, FloatFeature, CategoricFeature


class ElementExtractor(FeatureExtractor):
    """
    Extract one element from a vector
    """

    def __init__(self, element):
        self.element = element

    """ELEMENT"""

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        if not (isinstance(value, str) or isinstance(value, int)):
            raise DataException("element ot extract must be int or str")
        self._element = value

    def extract_feature(self, data):
        return data[self.element]

    """Serializable interface """

    def to_jcr(self):
        data = {
            "element": self.element,
        }
        return data

    @classmethod
    def from_jcr(cls, jcr):
        return cls(**jcr)

    """Buildable interface"""

    def build(self, data):
        pass

    def is_built(self):
        return True

    def __str__(self):
        return f"{self.__class__.__name__}(element={self.element})"


def construct_features(dtypes):
    components = []
    for key in dtypes.index:
        # Check type: Numeric or categoric
        extractor = ElementExtractor(element=key)
        if np.issubdtype(dtypes[key], np.floating):
            component = FloatFeature(name=key, extractor=extractor)
        elif np.issubdtype(dtypes[key], np.integer):
            component = IntFeature(name=key, extractor=extractor)
        elif dtypes[key] == np.dtype("O"):
            component = CategoricFeature(name=key, extractor=extractor)
        else:
            raise ValueError(f"dtype {dtypes[key]} not supported.")

        components.append(component)

    return components
