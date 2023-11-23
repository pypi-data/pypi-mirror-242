import logging

from .mixin.search import SearchMixin

__VERSION__ = "0.0.1"

from ytvs.mixin.search import SearchMixin

DEFAULT_LOGGER = logging.getLogger("yuoutubeapi")


class Client(
    SearchMixin
):
    pass
