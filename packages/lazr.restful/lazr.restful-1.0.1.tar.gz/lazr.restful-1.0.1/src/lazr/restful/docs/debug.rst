LAZR Debugging Helpers
**********************

LAZR offers a variety of debug helpers to help diagnose problems in your
application.

===============
``debug_proxy``
===============

There is a ``debug_proxy()`` function that can be used to print information
about the layers of proxy around the object.

    >>> from lazr.restful.debug import debug_proxy

In the simple case, where no proxy is used, as simple message is output:

    >>> print(debug_proxy(1))
    1 doesn't have any proxies.

Otherwise, it prints the proxy type for each proxy used:

    >>> from zope.proxy import ProxyBase

    >>> print(debug_proxy(ProxyBase(1)))
    zope.proxy.ProxyBase

If more than one proxy is used, information about the proxies will be
output from the most outer proxy to the most inner ones:

    >>> class SimpleProxy(ProxyBase):
    ...     """A very simple proxy."""

    >>> print(debug_proxy(SimpleProxy(ProxyBase(1))))
    SimpleProxy
    zope.proxy.ProxyBase

If the object is wrapped into a security proxy, additional information
about the checker used will be output:

    >>> from zope.security.checker import ProxyFactory, CheckerPublic, Checker
    >>> checker = Checker({'__str__': 'lazr.View',
    ...                    '__repr__': 'lazr.View',
    ...                    '__add__': 'lazr.Edit'},
    ...                   {'value': CheckerPublic,
    ...                    'some_other_value': 'lazr.Edit'})
    >>> p = ProxyFactory(1, checker)
    >>> print(debug_proxy(p))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        lazr.Edit: __add__
        lazr.Edit (set): some_other_value
        lazr.View: __repr__, __str__
        public (set): value
