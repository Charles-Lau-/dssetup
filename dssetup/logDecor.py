#coding=utf-8
import logging
from django.core.handlers.wsgi import WSGIRequest
logger = logging.getLogger(__name__)

def logDecor(func):
    def _logDecor(*args,**kwargs):
        info = "The called function is "+func.__name__+" and args are "
  
        for arg in args:
            if(isinstance(arg,WSGIRequest)):
                pass
            else:
                info +=" "+unicode(arg)
        
        info += unicode(kwargs)
        logger.info(info)
        return func(*args,**kwargs)
    return _logDecor