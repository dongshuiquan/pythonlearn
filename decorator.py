# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time

def sleep(arg):
    if not callable(arg):
        def decorator(func):
            def wrapper(*args, **kw):
                result = func(*args, **kw)
                time.sleep(arg)
                #print 'sleep ' + str(arg)
                return result
            return wrapper
        return decorator
    else:
        def wrapper(*args, **kw):
            result = arg(*args, **kw)
            time.sleep(1)
            #print 'sleep 1'
            return result
        return wrapper


@sleep(3)
def foo():
    print 'foo'
    
@sleep
def bar():
    print 'bar'
    
@sleep(0.5)
def com():
    print 'com'
 
com()
foo()
bar()


