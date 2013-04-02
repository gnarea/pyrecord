__all__ = [
    "get_duplicated_iterable_items",
    ]


def get_duplicated_iterable_items(iterable):
    iterable_with_unique_items = []
    iterable_with_duplicated_items = []
    for item in iterable:
        if item in iterable_with_unique_items:
            iterable_with_duplicated_items.append(item)
        else:
            iterable_with_unique_items.append(item)
    return iterable_with_duplicated_items
