LAZR Interface Helpers
**********************

==============
use_template()
==============

Sometime it is convenient to create an interface by copying another one,
without creating a typed relationship between the two. A good use-case
for that is for a UI form. The model and form schema are related but not
identical. For examples, the labels/descriptions should probably be
different since the model doc is intended to the developers, while the
UI ones are for the user. The model may have additional fields that are
not relevant for the UI model and/or vice versa. And there is no reason
to say that an object providing the UI schema *is a* model. (Like the
extension relationship would allow us to claim.) In the end, the
relationship between the two schemas is one of convenience: we want to
share the data validation constraint specified by the model. For these
cases, there is lazr.restful.interface.use_template.

Let's define a "model" schema:

    >>> from zope.interface import Attribute, Interface
    >>> from zope.schema import Int, Choice, Text

    >>> class MyModel(Interface):
    ...     """A very simple model."""
    ...
    ...     age = Int(title=u"Number of years since birth")
    ...     name = Text(title=u"Identifier")

    >>> class Initiated(MyModel):
    ...     illuminated = Choice(
    ...         title=u"Has seen the fnords?", values=('yes', 'no', 'maybe'))
    ...     fancy_value = Attribute(u"Some other fancy value.")

The use_template() helper takes as first parameter the interface to use
as a template and either a 'include' or 'exclude' parameter taking the
list of the fields to include/exclude.

So to create a form for UI with more appropriate labels you would use:

    >>> from lazr.restful.interface import use_template
    >>> class MyForm1(Interface):
    ...     "Form schema for a MyModel."
    ...     use_template(MyModel, include=['age', 'name'])
    ...     age.title = u'Your age:'
    ...     name.title = u'Your name:'

The MyForm1 interface now has an age and name fields that have a
distinct titles than their original:

    >>> sorted(MyForm1.names())
    ['age', 'name']
    >>> print(MyForm1.get('age').title)
    Your age:
    >>> print(MyForm1.get('name').title)
    Your name:

The interface attribute points to the correct interface:

    >>> MyForm1.get('age').interface is MyForm1
    True

And the original field wasn't updated:

    >>> print(MyModel.get('age').title)
    Number of years since birth
    >>> MyModel.get('name').interface is MyModel
    True

Using the exclude form of the directive, you could get an equivalent to
MyForm1 using the following:

    >>> class MyForm2(Interface):
    ...     use_template(Initiated, exclude=['illuminated', 'fancy_value'])

    >>> sorted(MyForm2.names())
    ['age', 'name']

It is an error to use both arguments:

    >>> class MyForm3(Interface):
    ...     use_template(MyModel, include=['age'], exclude=['name'])
    Traceback (most recent call last):
      ...
    ValueError: you cannot use 'include' and 'exclude' at the same time.

If neither include, nor exclude are used. The new interface is an exact
copy of the template:

    >>> class MyForm4(Interface):
    ...     use_template(Initiated)
    >>> sorted(MyForm4.names())
    ['age', 'fancy_value', 'illuminated', 'name']

The order of the field in the new interface is based on the order of the
declaration in the use_template() directive.

    >>> class MyForm5(Interface):
    ...     use_template(Initiated, include=['name', 'illuminated', 'age'])

    >>> from zope.schema import getFieldNamesInOrder
    >>> getFieldNamesInOrder(MyForm5)
    ['name', 'illuminated', 'age']

The directive can only be used from within a class scope:

    >>> use_template(MyModel)
    Traceback (most recent call last):
      ...
    TypeError: use_template() can only be used from within a class
    definition.

================
copy_attribute()
================

use_template() uses the copy_attribute() function to copy attributes from
the original interface. It can also be used on its own to make a copy of
an interface attribute or schema field.

    >>> from lazr.restful.interface import copy_attribute

    >>> illuminated = copy_attribute(Initiated['illuminated'])
    >>> illuminated
    <...Choice...>
    >>> illuminated.__name__
    'illuminated'
    >>> print(illuminated.title)
    Has seen the fnords?

The interface attribute is cleared:

    >>> print(illuminated.interface)
    None

It also supports the Field ordering (the copied field will have an
higher order than its original.)

    >>> Initiated['illuminated'].order < illuminated.order
    True

The parameter to the function must provide IAttribute:

    >>> copy_attribute(MyModel)
    Traceback (most recent call last):
      ...
    TypeError: <...MyModel...> doesn't provide IAttribute.

============
copy_field()
============

There is also a copy_field() field function that can be used to copy a
schema field and override some of the copy attributes at the same time.

    >>> from lazr.restful.interface import copy_field
    >>> age = copy_field(
    ...     MyModel['age'], title=u'The age.', required=False,
    ...     arbitrary=1)
    >>> age.__class__.__name__
    'Int'
    >>> print(age.title)
    The age.
    >>> age.arbitrary
    1
    >>> age.required
    False
    >>> MyModel['age'].required
    True

If the value for an overridden field is invalid, an exception will be
raised:

    >>> copy_field(MyModel['age'], title=b'This should be unicode')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.schema._bootstrapinterfaces.WrongType: ...

That function can only be called on an IField:

    >>> copy_field(Initiated['fancy_value'])
    Traceback (most recent call last):
      ...
    TypeError: <...Attribute...> doesn't provide IField.

