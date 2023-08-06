Utilities to define security checkers
*************************************

LAZR provides utility functions to make it easy to define security
checkers for content class.

protect_schema()
================

The protect_schema() function will define a checker for a class based on
the schema passed in as parameter.

    >>> from lazr.restful.security import protect_schema
    >>> from zope.interface import Attribute, Interface, implementer
    >>> from zope.schema import TextLine

    >>> class MySchema(Interface):
    ...     an_attr = Attribute(u'An attribute.')
    ...
    ...     a_field = TextLine(title=u'A property that can be set.')
    ...
    ...     a_read_only_field = TextLine(
    ...         title=u'A read only property', readonly=True)
    ...
    ...     def aMethod():
    ...         "A simple method."

    >>> @implementer(MySchema)
    ... class MyContent(object):
    ...     def __init__(self, an_attr, a_field, a_read_only_field):
    ...         self.an_attr = an_attr
    ...         self.a_field = a_field
    ...         self.a_read_only_field = a_read_only_field
    ...
    ...     def aMethod(self):
    ...         pass
    ...
    >>> protect_schema(MyContent, MySchema)

By default, the defined checker will grant public access to all
attributes defined in the schema.

    >>> from lazr.restful.debug import debug_proxy
    >>> from zope.security.checker import undefineChecker, ProxyFactory
    >>> content = MyContent(1, u'Mutable Field', u'RO Field')

ProxyFactory wraps the content using the defined checker.

    >>> print(debug_proxy(ProxyFactory(content)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: aMethod, a_field, a_read_only_field, an_attr

The permission required can be specified using the read_permission
parameter:

    >>> undefineChecker(MyContent)
    >>> protect_schema(MyContent, MySchema, read_permission='lazr.View')
    >>> print(debug_proxy(ProxyFactory(content)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        lazr.View: aMethod, a_field, a_read_only_field, an_attr

If you specify a write_permission parameter, set permission will be
granted for Attribute and non-readonly fields defined in the schema.

    >>> undefineChecker(MyContent)
    >>> protect_schema(MyContent, MySchema, write_permission='lazr.Edit')
    >>> print(debug_proxy(ProxyFactory(content)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        lazr.Edit (set): a_field, an_attr
        public: aMethod, a_field, a_read_only_field, an_attr

