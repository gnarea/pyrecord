=================================
PyRecord: Pythonic *Record* Types
=================================

:Author: `Gustavo Narea <http://gustavonarea.net/>`_
:License: Apache License v2
:Latest version: |release|

.. topic:: Overview

    A `record <http://en.wikipedia.org/wiki/Record_(computer_science)>`_ (aka
    "struct" in C) is a pre-defined collection of values where each is accessed
    by a unique name. Depending on the nature of the data, records may be a
    superior alternative to dictionaries and instances of custom classes.
    
    **PyRecord** allows you to use records in Python v2.7 to v3.x and
    PyPy v2, and can be thought of as an improved
    :class:`~collections.namedtuple`.

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

PyRecord doesn't have external dependencies and you can `get it from
PYPI <https://pypi.python.org/pypi/pyrecord/>`_ or install it with pip:

.. code-block:: bash

    pip install pyrecord

Do you like what you've seen? Read on to learn more!


Contents
========

.. toctree::
    :maxdepth: 2
    
    usage
    best-practices
    api
    support
    development
    changelog
