from .internal import MatcherBase
from . import number_matcher
from . import str_matcher
from . import list_matcher
from . import dict_matcher
from . import other_matcher


class BelieveMixin(object):
    pass


# Put all Matcher into BelieveMixin
for m in [number_matcher, str_matcher, list_matcher, dict_matcher, other_matcher]:
    for c in dir(m):
        cls = getattr(m, c)
        try:
            if issubclass(cls, MatcherBase) and cls != MatcherBase:
                setattr(BelieveMixin, c, cls)
        except TypeError:
            pass
