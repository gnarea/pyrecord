*********************************************************
**PyRecord**: *Record* Datatype Implementation for Python
*********************************************************

This library allows you to use `records
<http://en.wikipedia.org/wiki/Record_(computer_science)>`_ (aka "structs" in C)
in Python.

A record is a composite datatype with a pre-defined collection of values (each
with a unique name) and no operations. In Python terms, that'd be an instance
of a class for which you don't write methods because you're only intested in
using it to hold data. The following example demonstrates how this datatype
can be used::

    >>> from datetime import datetime
    >>> from pyrecord import Record
    >>> 
    >>> # Define the record types
    ... Person = Record.create_type("Person", "name", "email_address")
    >>> Student = Person.extend_type("Student", "courses_read", "graduation_date", graduation_date=None)
    >>> Professor = Person.extend_type("Professor", "course_taught")
    >>> 
    >>> # Define the records for the types above
    ... john_student = Student("John Smith", "jsmith@example.org", ["Calculus", "Economics"])
    >>> john_professor = Professor("John Doe", "john.doe@example.com", "OOP")
    >>> john_professor2 = Professor(email_address="john.doe@example.com", name="John Doe", course_taught="OOP")
    >>> jane_student = Student("Jane Doe", "jane.doe@example.org", ["Calculus", "OOP"], datetime(1995, 10, 4))
    >>> jane_professor = Professor("Jane Doe", "jane.doe@example.org", "Calculus")
    >>> 
    >>> john_student
    Student(name='John Smith', email_address='jsmith@example.org', courses_read=['Calculus', 'Economics'], graduation_date=None)
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

Records are similar to dictionaries and namedtuples in Python, 


Alternatives
============

- Dictionary
- namedtuple
- Custom classes.


When to use each of those, and when to use a record.

Type creation
=============


Subtype creation
================


Initialization
==============


Generalization
==============


Specialization
==============


API
===



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

