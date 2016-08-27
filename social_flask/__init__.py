__version__ = '0.0.1'

from social_core.utils import set_current_strategy_getter
from .utils import load_strategy


set_current_strategy_getter(load_strategy)
