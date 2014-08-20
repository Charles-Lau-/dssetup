#coding=utf-8
import logging
from django.core.handlers.wsgi import WSGIRequest

def logDecor(func):
    def _logDecor(*args,**kwargs):
        info = "The called function is "+func.__name__+" and args are "
        
        for arg in args:
            if(isinstance(arg,WSGIRequest)):
                pass
            else:
                info +=" "+unicode(arg)
        
        info += unicode(kwargs)
        logger = logging.getLogger(func.__name__)
        logger.info(info)
        return func(*args,**kwargs)
    return _logDecor