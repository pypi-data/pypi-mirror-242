if (__debug__):
    try:
        from .scraper import Scrape
        from .handlers import RequestHandler, UserHandler
        from .core import __version__, __package__, __qualname__, __doc__
        from .exceptions import UserHasNoLocationException, NonePublicArchiveRepositoryException, NoneFilledPropertyException
    
    except ModuleNotFoundError.__doc__ as mnfe:
        raise mnfe