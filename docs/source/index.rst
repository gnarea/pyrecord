=========================================================
**PyRecord**: *Record* Datatype Implementation for Python
=========================================================

.. module:: pyrecord
    :synopsis: Pythonic Record Data Type
.. moduleauthor:: Gustavo Narea

:Author: `Gustavo Narea <http://gustavonarea.net/>`_
:License: Apache License v2
:Latest version: |release|

.. topic:: Overview

    A `record <http://en.wikipedia.org/wiki/Record_(computer_science)>`_ (aka
    "struct" in C) is a pre-defined collection of values where each is accessed
    by a unique name. Depending on the nature of the data, records may be a
    superior alternative to dictionaries and instances of custom classes.
    
    PyRecord allows you to use records in Python v2.7 through v3.x and PyPy v2,
    and can be thought of as an improved :class:`~collections.namedtuple`.

In Python terms, a **record** is an instance of any class for which you define
some attributes but no methods. Such classes, which are known as **record
types**, can be easily written but require a lot of noisy boilerplate. This is
where PyRecord comes into play: It saves you the boilerplate so you can focus
on what really matters.

The following example demonstrates how you can define record types::

    >>> from pyrecord import Record
    >>> Person = Record.create_type("Person", "name", "email_address")
    >>> Student = Person.extend_type("Student", "courses_read", "graduation_date", graduation_date=None)
    >>> Professor = Person.extend_type("Professor", "course_taught")

And this is how you could create some records with those types:

    >>> john_student = Student("John Smith", "jsmith@example.org", ["Calculus", "Economics"])
    >>> john_professor = Professor("John Doe", "john.doe@example.com", "OOP")
    >>> john_professor2 = Professor(email_address="john.doe@example.com", name="John Doe", course_taught="OOP")
    >>> jane_student = Student("Jane Doe", "jane.doe@example.org", ["Calculus", "OOP"], datetime(1995, 10, 4))
    >>> jane_professor = Professor("Jane Doe", "jane.doe@example.org", "Calculus")
    >>> alice_student = Student("Alice Smith", "alice.smith@example.org")
    Traceback (most recent call last):
      (...)
    pyrecord.exceptions.RecordInstanceError: Field "courses_read" is undefined

Finally, this is how you would use the records above::

    >>> john_student
    Student(name='John Smith', email_address='jsmith@example.org', courses_read=['Calculus', 'Economics'], graduation_date=None)
    >>> john_student.name
    'John Smith'
    >>> john_student.name = "John Smith Jr."
    >>> john_student
    Student(name='John Smith Jr.', email_address='jsmith@example.org', courses_read=['Calculus', 'Economics'], graduation_date=None)
    >>> 
    >>> john_student == john_professor
    False
    >>> john_professor == john_professor2
    True
    >>> john_student == john_student.copy()
    True
    >>> jane_student == jane_professor
    False
    >>> 
    >>> jane_person1 = Person.init_from_specialization(jane_student)
    >>> jane_person2 = Person.init_from_specialization(jane_professor)
    >>> jane_person1 == jane_person2
    True

Do you like what you've seen? Read on to learn more.

Common Usage
============

Refer to the API documentation below for a comprehensive description of the
interfaces for record types and records.


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

API
===

.. autoclass:: Record
    :members:

.. automodule:: pyrecord.exceptions
    :members:


Best Practices
==============

Use the right data type for the job
-----------------------------------

You're right, records are awesome. But that doesn't mean that you should
use them for everything from now on. Depending on the nature of your data,
other data types may be better suited for the job:

- *Records* are great at holding data with a static structure.
- *Dictionaries* should be used when the structure of the data is dynamic (i.e.,
  it's only known at runtime).
- Like records, *named tuples* are meant to hold data with a static structure.
  Unlike records, name tuples are immutable and therefore hashable. Once this
  library offers immutable records, you will be able to forget about
  namedtuple once and for all.
- Stick to good old *classes* when you need to add methods to your objects.
- *SimpleNamespace* in Python 3.3+ is the Frankenstein of the block and should
  only be used when drunk.


Do not define more than 7 fields
--------------------------------

As with any other data type with a static set of elements (e.g., your
custom classes, named tuples), if you have more than `7 elements
<http://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two>`_,
you should consider that to be a smell.

Most of the time, the solution could be as simple as moving some of those
fields to a new record type. For instance, if you have a record type for a
person and a bunch of fields, of which some relate to the person's address, it
could be tempting to define all those fields in the same record type -- But
how about creating a separate record type for an address?


Only use immutable values as default field values
-------------------------------------------------

For the same reason why you wouldn't have mutable default arguments: They could
be changed inadvertently.

So, the following is fine::

    Person = Record.create_type("Person", "pet_names", pet_names=())

But this is not::

    Person = Record.create_type("Person", "pet_names", pet_names=[])


Refer to any one record type by a single name
---------------------------------------------

Yes, it is annoying to have to specify the record type name twice when you
create it, but you should stick to it and consistently refer to any one
record type by its sole name. Otherwise, your code will be harder to maintain.


Good Real-World Examples
========================

`hubspot-contacts <http://pythonhosted.org/hubspot-contacts/>`_ is the first
Free Software project to use this library. It's co-authored by the author of
this library and could therefore be considered a good example on how to use
records.


Support
=======

TODO

Questions about modelling should be raised on StackOverflow, for example.


Development
===========

TODO


Credits
=======

This implementation of records is inspired by (tagged) records in the Ada
programming language. As a consequence, good support for inheritance at the
type and instance levels was an important requirement in the design of this
library.
