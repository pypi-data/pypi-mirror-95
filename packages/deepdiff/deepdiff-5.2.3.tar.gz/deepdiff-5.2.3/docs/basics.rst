:doc:`/index`

Basics
======


Importing
    >>> from deepdiff import DeepDiff
    >>> from pprint import pprint

Same object returns empty
    >>> t1 = {1:1, 2:2, 3:3}
    >>> t2 = t1
    >>> print(DeepDiff(t1, t2))
    {}

Type of an item has changed
    >>> t1 = {1:1, 2:2, 3:3}
    >>> t2 = {1:1, 2:"2", 3:3}
    >>> pprint(DeepDiff(t1, t2), indent=2)
    { 'type_changes': { 'root[2]': { 'new_type': <class 'str'>,
                                     'new_value': '2',
                                     'old_type': <class 'int'>,
                                     'old_value': 2}}}

Value of an item has changed
    >>> t1 = {1:1, 2:2, 3:3}
    >>> t2 = {1:1, 2:4, 3:3}
    >>> pprint(DeepDiff(t1, t2, verbose_level=0), indent=2)
    {'values_changed': {'root[2]': {'new_value': 4, 'old_value': 2}}}

Item added and/or removed
    >>> t1 = {1:1, 3:3, 4:4}
    >>> t2 = {1:1, 3:3, 5:5, 6:6}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint (ddiff)
    {'dictionary_item_added': [root[5], root[6]],
     'dictionary_item_removed': [root[4]]}

Set verbose level to 2 in order to see the added or removed items with their values
    >>> t1 = {1:1, 3:3, 4:4}
    >>> t2 = {1:1, 3:3, 5:5, 6:6}
    >>> ddiff = DeepDiff(t1, t2, verbose_level=2)
    >>> pprint(ddiff, indent=2)
    { 'dictionary_item_added': {'root[5]': 5, 'root[6]': 6},
      'dictionary_item_removed': {'root[4]': 4}}

String difference
    >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world"}}
    >>> t2 = {1:1, 2:4, 3:3, 4:{"a":"hello", "b":"world!"}}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint (ddiff, indent = 2)
    { 'values_changed': { 'root[2]': {'new_value': 4, 'old_value': 2},
                          "root[4]['b']": { 'new_value': 'world!',
                                            'old_value': 'world'}}}


String difference 2
    >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world!\nGoodbye!\n1\n2\nEnd"}}
    >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world\n1\n2\nEnd"}}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint (ddiff, indent = 2)
    { 'values_changed': { "root[4]['b']": { 'diff': '--- \n'
                                                    '+++ \n'
                                                    '@@ -1,5 +1,4 @@\n'
                                                    '-world!\n'
                                                    '-Goodbye!\n'
                                                    '+world\n'
                                                    ' 1\n'
                                                    ' 2\n'
                                                    ' End',
                                            'new_value': 'world\n1\n2\nEnd',
                                            'old_value': 'world!\n'
                                                         'Goodbye!\n'
                                                         '1\n'
                                                         '2\n'
                                                         'End'}}}

    >>>
    >>> print (ddiff['values_changed']["root[4]['b']"]["diff"])
    --- 
    +++ 
    @@ -1,5 +1,4 @@
    -world!
    -Goodbye!
    +world
     1
     2
     End

List difference
    >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3, 4]}}
    >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2]}}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint (ddiff, indent = 2)
    {'iterable_item_removed': {"root[4]['b'][2]": 3, "root[4]['b'][3]": 4}}

List that contains dictionary:
    >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:1, 2:2}]}}
    >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:3}]}}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint (ddiff, indent = 2)
    { 'dictionary_item_removed': [root[4]['b'][2][2]],
      'values_changed': {"root[4]['b'][2][1]": {'new_value': 3, 'old_value': 1}}}

Sets:
    >>> t1 = {1, 2, 8}
    >>> t2 = {1, 2, 3, 5}
    >>> ddiff = DeepDiff(t1, t2)
    >>> pprint(ddiff)
    {'set_item_added': [root[3], root[5]], 'set_item_removed': [root[8]]}

Named Tuples:
    >>> from collections import namedtuple
    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> t1 = Point(x=11, y=22)
    >>> t2 = Point(x=11, y=23)
    >>> pprint (DeepDiff(t1, t2))
    {'values_changed': {'root.y': {'new_value': 23, 'old_value': 22}}}

Custom objects:
    >>> class ClassA(object):
    ...     a = 1
    ...     def __init__(self, b):
    ...         self.b = b
    ...
    >>> t1 = ClassA(1)
    >>> t2 = ClassA(2)
    >>>
    >>> pprint(DeepDiff(t1, t2))
    {'values_changed': {'root.b': {'new_value': 2, 'old_value': 1}}}

Object attribute added:
    >>> t2.c = "new attribute"
    >>> pprint(DeepDiff(t1, t2))
    {'attribute_added': [root.c],
     'values_changed': {'root.b': {'new_value': 2, 'old_value': 1}}}


.. note::
    All the examples above use the default :ref:`text_view_label`.
    If you want traversing functionality in the results, use the :ref:`tree_view_label`.
    You just need to set view='tree' to get it in tree form.


.. _group_by_label:

Group By
--------

group_by can be used when dealing with list of dictionaries to convert them to group them by value defined in group_by. The common use case is when reading data from a flat CSV and primary key is one of the columns in the CSV. We want to use the primary key to group the rows instead of CSV row number.

Example:
    >>> from deepdiff import DeepDiff
    >>> t1 = [
    ...     {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
    ...     {'id': 'BB', 'name': 'James', 'last_name': 'Blue'},
    ...     {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
    ... ]
    >>>
    >>> t2 = [
    ...     {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
    ...     {'id': 'BB', 'name': 'James', 'last_name': 'Brown'},
    ...     {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
    ... ]
    >>>
    >>> DeepDiff(t1, t2)
    {'values_changed': {"root[1]['last_name']": {'new_value': 'Brown', 'old_value': 'Blue'}}}


Now we use group_by='id':
    >>> DeepDiff(t1, t2, group_by='id')
    {'values_changed': {"root['BB']['last_name']": {'new_value': 'Brown', 'old_value': 'Blue'}}}

.. note::
    group_by actually changes the structure of the t1 and t2. You can see this by using the tree view:

    >>> diff = DeepDiff(t1, t2, group_by='id', view='tree')
    >>> diff
    {'values_changed': [<root['BB']['last_name'] t1:'Blue', t2:'Brown'>]}
    >>> diff['values_changed'][0]
    <root['BB']['last_name'] t1:'Blue', t2:'Brown'>
    >>> diff['values_changed'][0].up
    <root['BB'] t1:{'name': 'Ja...}, t2:{'name': 'Ja...}>
    >>> diff['values_changed'][0].up.up
    <root t1:{'AA': {'nam...}, t2:{'AA': {'nam...}>
    >>> diff['values_changed'][0].up.up.t1
    {'AA': {'name': 'Joe', 'last_name': 'Nobody'}, 'BB': {'name': 'James', 'last_name': 'Blue'}, 'CC': {'name': 'Mike', 'last_name': 'Apple'}}


Back to :doc:`/index`
