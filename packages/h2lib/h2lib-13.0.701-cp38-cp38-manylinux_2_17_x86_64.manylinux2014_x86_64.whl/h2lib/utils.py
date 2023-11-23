import multiprocessing
import atexit
import numpy as np
from threading import Thread
from functools import wraps
import traceback
from _queue import Empty
import os
from contextlib import contextmanager


@contextmanager
def set_LD_LIBRARY_PATH():
    _file__ = np.__file__

    old = os.environ.get('LD_LIBRARY_PATH', "")

    if '/lib/' in _file__:  # pragma: no cover  (only on linux)
        lib_path = _file__[:_file__.index("/lib/") + 5]
        os.environ['LD_LIBRARY_PATH'] = f'{lib_path}:{old}'

    try:
        yield
    finally:
        os.environ['LD_LIBRARY_PATH'] = old


def run(cls, inputQueue, outputQueue, cls_args, **kwargs):
    o = cls(*cls_args, **kwargs)
    while True:
        method, args, kwargs = inputQueue.get()
        # if method == "Sentinel":
        #     outputQueue.put(method)
        # else:
        # print(method, args, kwargs)
        att = getattr(o, method)
        if hasattr(att, '__call__'):
            outputQueue.put(att(*args, **kwargs))
        else:
            outputQueue.put(att)
        if method == 'close':
            outputQueue.put('Exit process')
            return


class ProcessClass():
    cls = None

    def __init__(self, cls, cls_attrs={}):
        self.cls_attrs = cls_attrs
        self.cls = cls
        self.ctx = multiprocessing.get_context('spawn')
        self.inputQueue = self.ctx.Queue()
        self.outputQueue = self.ctx.Queue()
        atexit.register(self.close)
        self.closed = False

    def __call__(self, *args, **kwargs):
        kwargs.update({'cls': self.cls, 'inputQueue': self.inputQueue, 'outputQueue': self.outputQueue,
                       'cls_args': args})
        s = 'vs_debug.py'
        if s in "".join(traceback.format_stack()):  # pragma: no cover
            self.process = Thread(target=run, kwargs=kwargs)  # use this to debug from Visual studio
        else:
            self.process = self.ctx.Process(target=run, kwargs=kwargs, daemon=True)

        self.process.start()
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattribute__(self, name):
        try:
            if name != 'cls_attrs' and name in self.cls_attrs:
                raise AttributeError()
            return object.__getattribute__(self, name)
        except AttributeError:
            if hasattr(self.cls, name):
                if hasattr(getattr(self.cls, name), '__call__'):
                    @wraps(getattr(self.cls, name))
                    def wrap(*args, wait_for_result=True, **kwargs):
                        self.inputQueue.put((name, args, kwargs))
                        if wait_for_result:
                            return self.get_result()
                    return wrap
                else:
                    self.inputQueue.put((name, (), {}))
                    return self.get_result()
            else:
                raise AttributeError(f"'{self.cls.__name__}' object has no attribute '{name}'")

    def get_result(self):
        while True:
            if self.process.is_alive() or self.closed:
                try:
                    return self.outputQueue.get(timeout=5)
                except Empty:
                    pass  # time out. Check process is alive and try again
            # self.inputQueue.put(('Sentinel', (), {}))
            # res_lst = []
            # print('get result')
            # while True:
            #     print('get')
            #     r = self.outputQueue.get()
            #     print(' got')
            #
            #     if isinstance(r, str):
            #         if r == 'Exit process':
            #             return r
            #         elif r == 'Sentinel':
            #             return res_lst[0]
            #         else:
            #             res_lst.append(r)
            #     else:
            #         res_lst.append(r)
            else:
                raise Exception(f'{self.cls.__name__} process died')

    def close(self, wait_for_result=False):
        self.inputQueue.put(('close', [], {}))
        self.process.join()
        self.closed = True


class MultiProcessInterface():
    def __init__(self, cls, args_lst):
        self.cls = cls
        self.obj_lst = [ProcessClass(cls)(*args) for args in args_lst]

    def __getattribute__(self, name):
        if name in ['obj_lst', '__class__']:
            return object.__getattribute__(self, name)

        a_lst = self.obj_lst
        if hasattr(getattr(self.obj_lst[0], name), '__call__'):
            def wrap(*args, **kwargs):
                for i, o in enumerate(self.obj_lst):
                    def get_arg(arg):
                        if isinstance(arg, list) and len(arg) == len(a_lst):
                            return arg[i]
                        else:
                            return arg
                    a_args = [get_arg(arg) for arg in args]
                    a_kwargs = {k: get_arg(v) for k, v in kwargs.items()}
                    getattr(o, name)(*a_args, wait_for_result=False, **a_kwargs)
                if isinstance(self, SubsetProcessWrapper) and len(self.obj_lst) == 1:
                    return self.obj_lst[0].get_result()
                return [o.get_result() for o in self.obj_lst]
            return wrap
        else:
            if isinstance(self, SubsetProcessWrapper) and len(self.obj_lst) == 1:
                return getattr(self.obj_lst[0], name)
            return [getattr(o, name) for o in self.obj_lst]

    def __getitem__(self, slice):
        lst = np.atleast_1d(np.array(self.obj_lst)[slice]).tolist()
        return SubsetProcessWrapper(lst)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SubsetProcessWrapper(MultiProcessInterface):
    def __init__(self, obj_lst):
        self.obj_lst = obj_lst

    def __getitem__(self, slice):
        raise Exception('Cannot make subset of SubsetProcessWrapper')

    def __getattribute__(self, name):
        if name == 'close':
            raise Exception("Cannot close SubsetProcessWrapper. Please close all instances at once")

        return MultiProcessInterface.__getattribute__(self, name)
