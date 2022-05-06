from .dict_matcher import Dict
from .dict_matcher import DictOf
from .dict_matcher import Optional
from .error import ValidateError
from .internal import BelieveBase
from .internal import validate
from .list_matcher import AnyOrder
from .list_matcher import ListOf
from .list_matcher import OneOf
from .number_matcher import Almost
from .number_matcher import AnyFloat
from .number_matcher import AnyInt
from .other_matcher import Any
from .other_matcher import Not
from .other_matcher import Nullable
from .str_matcher import AnyIntStr
from .str_matcher import AnyIPV4
from .str_matcher import AnyJsonStr
from .str_matcher import AnySHA1
from .str_matcher import AnyStr
from .str_matcher import AnyUrl
from .str_matcher import AnyUUID


# Put all Matcher into BelieveMixin
class BelieveMixin(object):
    pass


for c, cls in dict(locals()).items():
    try:
        if issubclass(cls, BelieveBase) and cls != BelieveBase:
            setattr(BelieveMixin, c, cls)
    except TypeError:
        pass

__version__ = "1.0.13"
