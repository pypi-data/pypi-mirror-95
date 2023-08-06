:doc:`/index`

.. _serialization_label:

Serialization
=============

.. _to_dict_label:

To Dict
-------

In order to convert the DeepDiff object into a normal Python dictionary, use the to_dict() method.

Example:
    >>> t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3]}}
    >>> t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n\n\nEnd"}}
    >>> ddiff = DeepDiff(t1, t2)
    >>> ddiff.to_dict()
    {'type_changes': {"root[4]['b']": {'old_type': <class 'list'>, 'new_type': <class 'str'>, 'old_value': [1, 2, 3], 'new_value': 'world\n\n\nEnd'}}}


Note that you can override the :ref:`view_label` that was originally used to generate the diff here.

Example:
    >>> t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3]}}
    >>> t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n\n\nEnd"}}
    >>> ddiff = DeepDiff(t1, t2, view='tree')
    >>> ddiff.to_dict(view_override='text')
    {'type_changes': {"root[4]['b']": {'old_type': <class 'list'>, 'new_type': <class 'str'>, 'old_value': [1, 2, 3], 'new_value': 'world\n\n\nEnd'}}}

.. _to_json_label:

To Json
-------

In order to do safe json serialization, use the to_json() method.

Example:
    >>> t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3]}}
    >>> t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n\n\nEnd"}}
    >>> ddiff = DeepDiff(t1, t2, view='tree')
    >>> ddiff.to_json()
    '{"type_changes": {"root[4][\'b\']": {"old_type": "list", "new_type": "str", "old_value": [1, 2, 3], "new_value": "world\\n\\n\\nEnd"}}}'

.. _to_json_pickle_label:

To Json Pickle
--------------

If you want the original DeepDiff object to be serialized with all the bells and whistles, you can use the to_json_pickle() and from_json_pickle() in order to serialize and deserialize its results into json. Note that json_pickle is unsafe and json pickle dumps from untrusted sources should never be loaded. It is recommended not to use this serialization unless you have to.

.. note::
    You need to install the `jsonpickle <https://github.com/jsonpickle/jsonpickle>`_ package to use the to_json_pickle() method.

Serialize and then deserialize back to deepdiff
    >>> t1 = {1: 1, 2: 2, 3: 3}
    >>> t2 = {1: 1, 2: "2", 3: 3}
    >>> ddiff = DeepDiff(t1, t2)
    >>> jsoned = ddiff.to_json_pickle()
    >>> jsoned
    '{"type_changes": {"root[2]": {"new_type": {"py/type": "builtins.str"}, "new_value": "2", "old_type": {"py/type": "builtins.int"}, "old_value": 2}}}'
    >>> ddiff_new = DeepDiff.from_json_pickle(jsoned)
    >>> ddiff == ddiff_new
    True


.. _from_json_pickle_label:

From Json Pickle
----------------

Load the diff object from the json pickle dump.
Take a look at the above :ref:`to_json_pickle_label` for an example.

Back to :doc:`/index`
