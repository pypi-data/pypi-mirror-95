# flake8: noqa
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("fatlib").version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0dev"


from vfi import VFI
from dagging import DaggingClassifier, DaggingRegressor
