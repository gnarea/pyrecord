Typical Usage
=============

.. currentmodule:: pyrecord

For a comprehensive description of the interfaces for record types and records,
please refer to the :doc:`API documentation <api>`.


Type creation
-------------

To create a record type, just call :meth:`Record.create_type` with the
names of the field in your records. For example, to create a ``Person``
type with two fields (name and email address), you could do::

    Person = Record.create_type("Person", "name", "email_address")

.. note::

    Because of the way Python works, we cannot infer the name of the new record
    type by just looking at the name of the variable that will get the result
    of :meth:`~Record.create_type`. Unfortunately, this means that you have to
    specify the record type name twice as in the example above.

To make some fields optional and give them default values, pass such values as
keyword arguments::

    Person = Record.create_type("Person", "name", "email_address", email_address=None)


Subtype creation
----------------

To extend a record type, you just need to specify the additional fields
(if any) in a call to the :meth:`~Record.extend_type` method of the type that
you're inheriting from; for example::

    Student = Person.extend_type("Student", "courses_read", "graduation_date")

Fields in the subtypes can also have default values::

    Student = Person.extend_type("Student", "courses_read", "graduation_date", graduation_date=None)

You can also further extend sub-types if you want to.


Initialization
--------------

Records are initialized by passing the field values in the constructor, which
can be done by position and/or by name::

    john_student = Student("John Smith", "jsmith@example.org", courses_read=["Calculus", "Economics"])

All the fields with no default values must be specified in the constructor,
otherwise an exception will be raised.


Generalization
~~~~~~~~~~~~~~

If ``Person`` is the super-type of ``Student``, we can *generalize*
a ``Student`` record to a ``Person`` record with
:meth:`~Record.init_from_specialization`::

    >>> jane_student = Student("Jane Doe", "jane.doe@example.org", ["Calculus", "OOP"])
    >>> jane_person = Person.init_from_specialization(jane_student)
    >>> jane_person
    Person(name='Jane Doe', email_address='jane.doe@example.org')


Specialization
~~~~~~~~~~~~~~

Likewise, if ``Student`` is a sub-type of ``Person``, we can *specialize*
a ``Person`` record to a ``Student`` record with
:meth:`~Record.init_from_generalization`::

    >>> jane_person = Person("Jane Doe", "jane.doe@example.org")
    >>> jane_student = Student.init_from_generalization(jane_person, courses_read=["OOP"])
    >>> jane_student
    Student(name='Jane Doe', email_address='jane.doe@example.org', courses_read=['OOP'], graduation_date=None)

Note that to specialize a record you have to complement the generalization
(``jane_person`` in the example above) with values for all the additional
fields defined in the sub-type.
