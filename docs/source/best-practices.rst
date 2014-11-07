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
person with a bunch of fields, of which some relate to the person's address, it
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
