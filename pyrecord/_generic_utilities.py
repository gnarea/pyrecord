__all__ = [
    "get_duplicated_iterable_items",
    "is_valid_python_identifier",
    ]


def get_duplicated_iterable_items(iterable):
    unique_items = []
    duplicated_items = []
    for item in iterable:
        if item in duplicated_items:
            continue
        
        if item in unique_items:
            duplicated_items.append(item)
        else:
            unique_items.append(item)
    
    return duplicated_items


def is_valid_python_identifier(identifier):
    """
    Report whether ``identifier`` is a valid string for an identifier in Python.
    
    The syntax for a valid Python identifier is officially described on the
    following URL:
    http://docs.python.org/2/reference/lexical_analysis.html#identifiers
    
    """
    raise NotImplementedError
