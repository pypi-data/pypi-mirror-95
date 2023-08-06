import evalcache
import evalcache.lazy

from evalcache.lazy import expand, hashfuncs, updatehash_LazyObject, LazyObject, Lazy
from evalcache.dircache import DirCache

from evalcache.funcarg import arg_with_name

import hashlib
import inspect
import shutil

import os


class LazyFile(Lazy):
    """Декоратор функций создания ленивых файлов."""

    def __init__(self, cache, **kwargs):
        Lazy.__init__(self, cache, **kwargs)

    def __call__(self, field="path"):
        """Параметр указывает, в каком поле передаётся путь к создаваемому файлу"""

        def decorator(func, hint=None):
            return LazyFileMaker(self, func, field, hint)

        return decorator


class LazyFileMaker(LazyObject):
    """Обёртка - фабрика. Создаёт и тут же расскрывает объект ленивого файла"""

    def __init__(self, lazyfier, value, field, hint=None, prevent_unwrap_in_child=None):
        LazyObject.__init__(self, lazyfier, value=value, hint=hint, prevent_unwrap_in_child=prevent_unwrap_in_child)
        self.field = field
        self.rawfunc = value

    def __call__(self, *args, **kwargs):
        lobj = LazyFileObject(
            self.__lazybase__, 
            self, args, kwargs, prevent_unwrap=self.__lazy_unwrap_prevent_list_in_child__)
        lobj.unlazy()
        return lobj


class LazyFileObject(LazyObject):
    """Объект ленивого файла наследует логику построения хэша от предка, но переопределяет
	логику раскрытия."""

    def __init__(self, *args, **kwargs):
        LazyObject.__init__(self, *args, **kwargs, prevent_fastdo=True)

    def unlazy(self):
        func = self.generic.rawfunc
        path = arg_with_name(self.generic.field, func, self.args, self.kwargs)
        path = os.path.expanduser(path)

        if os.path.exists(path):
            os.remove(path)

        path_of_copy = self.__lazybase__.cache.makePathTo(self.__lazyhexhash__)

        if self.__lazyhexhash__ in self.__lazybase__.cache:
            if self.__lazybase__.diag:
                print("rest {}...".format(self.__lazyhexhash__[:20]))
            try:
                os.link(path_of_copy, path)
            except OSError as err:
                if err.errno == 18:
                    os.symlink(path_of_copy, path)
                else:
                    raise err
        else:
            if self.__lazybase__.diag:
                print("stor {}...".format(self.__lazyhexhash__[:20]))
            
            args, kwargs = evalcache.lazy.expand_args_kwargs(self, func)
            ret = func(*args, **kwargs)
            
            try:
                os.link(path, path_of_copy)
            except OSError as err:
                if err.errno == 18:
                    shutil.copyfile(path, path_of_copy)
                else:
                    raise err


hashfuncs[LazyFileMaker] = updatehash_LazyObject
hashfuncs[LazyFileObject] = updatehash_LazyObject
