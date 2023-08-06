# encoding: utf-8

import importlib
from future.builtins import str
import logging_helper
from future.utils import iteritems
from collections import MutableMapping
from ..config.constants import HandlerConstant
from ..config.intercept_handlers import Handlers

logging = logging_helper.setup_logging()


class InterceptHandlers(MutableMapping):

    def __init__(self):
        self.cfg = Handlers()
        self._handlers = {}

    def load_all_handlers(self):
        for handler in self.cfg:
            self.load_handler(handler=self.cfg[handler])

    def load_handler(self,
                     handler):

        # Load configured handlers
        logging.debug(u'Loading handler: {h}'.format(h=handler.name))

        # Check whether this handler has already been loaded, then either load/reload it.
        if handler.name not in self._handlers:
            self.__import_handler_module(handler=handler)

        else:
            logging.debug(u'Handler {n} is already loaded, Reloading!'.format(n=handler.name))

            h = self._handlers[handler.name]

            try:
                reload
            except NameError:
                importlib.reload(h[HandlerConstant.module])
            else:
                reload(h[HandlerConstant.module])
            self.__instantiate_handler_class(handler=handler,
                                             handler_module=h[HandlerConstant.module],
                                             handler_module_path=h[HandlerConstant.module_path])

    def __import_handler_module(self,
                                handler):

        try:
            # Attempt to import the handler module
            module_path = (u'{root}.{module}'.format(root=handler.module_root,
                                                     module=handler.module))

            handler_module = importlib.import_module(module_path)

        except ImportError:
            # Import failed so initialise module path with default readable values
            try:
                module_path
            except:
                module_path = u'<undefined module_path>'

            logging.warning(u'Could not load handler "{h}" from "{pth}"'.format(h=handler.name,
                                                                                pth=module_path))

        else:
            # Handler module imported to lets instantiate the handler!
            self.__instantiate_handler_class(handler=handler,
                                             handler_module=handler_module,
                                             handler_module_path=module_path)

    def __instantiate_handler_class(self,
                                    handler,
                                    handler_module,
                                    handler_module_path):
        try:
            # Attempt to instantiate handler instance
            handler_instance = handler_module.InterceptHandler()
        except AttributeError as e:
            logging.exception(e)
            error_message = u'handler module contains:\n'
            for k, v in iteritems(handler_module.__dict__):
                if k in (u'__builtins__'):
                    continue
                val = str(v).splitlines()
                indent = u'    \n' + u' ' * (len(k) + 2)
                val = indent.join(val)
                error_message += u'    {k}: {v}\n\n'.format(k=k,
                                                            v=val)
            logging.error(error_message)

        else:
            # Handler instance created so register the handler
            self._handlers[handler.name] = {
                HandlerConstant.name:        handler.name,
                HandlerConstant.api:         handler.api,
                HandlerConstant.module_root: handler.module_root,
                HandlerConstant.module:      handler_module,
                HandlerConstant.module_path: handler_module_path,
                HandlerConstant.instance:    handler_instance
            }

    def __getitem__(self, item):
        return self._handlers[item]

    def __setitem__(self, item, value):
        self._handlers[item] = value

    def __delitem__(self, item):
        del self._handlers[item]

    def __iter__(self):
        return iter(self._handlers)

    def __len__(self):
        return len(self._handlers)
