#!/usr/bin/env python
import datetime
import pytest
import logging
from decimal import Decimal
from deepdiff import DeepDiff
from deepdiff.helper import pypy3
from tests import CustomClass

logging.disable(logging.CRITICAL)


class TestDeepDiffText:
    """DeepDiff Tests."""

    def test_same_objects(self):
        t1 = {1: 1, 2: 2, 3: 3}
        t2 = t1
        assert {} == DeepDiff(t1, t2)

    def test_item_type_change(self):
        t1 = {1: 1, 2: 2, 3: 3}
        t2 = {1: 1, 2: "2", 3: 3}
        ddiff = DeepDiff(t1, t2)
        assert {
            'type_changes': {
                "root[2]": {
                    "old_value": 2,
                    "old_type": int,
                    "new_value": "2",
                    "new_type": str
                }
            }
        } == ddiff

    def test_item_type_change_less_verbose(self):
        t1 = {1: 1, 2: 2, 3: 3}
        t2 = {1: 1, 2: "2", 3: 3}
        assert {'type_changes': {
                "root[2]": {
                    "old_type": int,
                    "new_type": str
                }
                }} == DeepDiff(t1, t2, verbose_level=0)

    def test_item_type_change_for_strings_ignored_by_default(self):
        """ ignore_string_type_changes = True by default """

        t1 = 'hello'
        t2 = b'hello'
        ddiff = DeepDiff(t1, t2, ignore_string_type_changes=True)
        assert not ddiff

    def test_item_type_change_for_strings_override(self):
        t1 = 'hello'
        t2 = b'hello'
        ddiff = DeepDiff(t1, t2, ignore_string_type_changes=False)
        assert {
            'type_changes': {
                'root': {
                    'old_type': str,
                    'new_type': bytes,
                    'old_value': 'hello',
                    'new_value': b'hello'
                }
            }
        } == ddiff

    def test_value_change(self):
        t1 = {1: 1, 2: 2, 3: 3}
        t2 = {1: 1, 2: 4, 3: 3}
        result = {
            'values_changed': {
                'root[2]': {
                    "old_value": 2,
                    "new_value": 4
                }
            }
        }
        assert result == DeepDiff(t1, t2)

    def test_item_added_and_removed(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: 4}
        t2 = {1: 1, 2: 4, 3: 3, 5: 5, 6: 6}
        ddiff = DeepDiff(t1, t2)
        result = {
            'dictionary_item_added': {'root[5]', 'root[6]'},
            'dictionary_item_removed': {'root[4]'},
            'values_changed': {
                'root[2]': {
                    "old_value": 2,
                    "new_value": 4
                }
            }
        }
        assert result == ddiff

    def test_item_added_and_removed_verbose(self):
        t1 = {1: 1, 3: 3, 4: 4}
        t2 = {1: 1, 3: 3, 5: 5, 6: 6}
        ddiff = DeepDiff(t1, t2, verbose_level=2)
        result = {
            'dictionary_item_removed': {
                'root[4]': 4
            },
            'dictionary_item_added': {
                'root[6]': 6,
                'root[5]': 5
            }
        }
        assert result == ddiff

    def test_diffs_dates(self):
        t1 = datetime.date(2016, 8, 8)
        t2 = datetime.date(2016, 8, 7)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root': {
                    'new_value': t2,
                    'old_value': t1
                }
            }
        }
        assert result == ddiff

    def test_diffs_timedeltas(self):
        t1 = datetime.timedelta(days=1, seconds=12)
        t2 = datetime.timedelta(days=1, seconds=10)
        t3 = datetime.timedelta(seconds=(60*60*24) + 12)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root': {
                    'new_value': t2,
                    'old_value': t1
                }
            }
        }
        assert result == ddiff
        ddiff = DeepDiff(t1, t3)
        result = {}
        assert result == ddiff

    def test_diffs_times(self):
        t1 = datetime.time(1, 1)
        t2 = datetime.time(1, 2)
        t3 = datetime.time(1, 1)
        expected_result = {
            'values_changed': {
                'root': {
                    'new_value': t2,
                    'old_value': t1
                }
            }
        }
        assert DeepDiff(t1, t2) == expected_result
        assert DeepDiff(t1, t3) == {}

    def test_string_difference(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world"}}
        t2 = {1: 1, 2: 4, 3: 3, 4: {"a": "hello", "b": "world!"}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[2]': {
                    'old_value': 2,
                    'new_value': 4
                },
                "root[4]['b']": {
                    'old_value': 'world',
                    'new_value': 'world!'
                }
            }
        }
        assert result == ddiff

    def test_diffs_equal_strings_when_not_identical(self):
        t1 = 'hello'
        t2 = 'hel'
        t2 += 'lo'
        assert t1 is not t2
        ddiff = DeepDiff(t1, t2)
        assert {} == ddiff

    def test_string_difference2(self):
        t1 = {
            1: 1,
            2: 2,
            3: 3,
            4: {
                "a": "hello",
                "b": "world!\nGoodbye!\n1\n2\nEnd"
            }
        }
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n1\n2\nEnd"}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                "root[4]['b']": {
                    'diff':
                    '--- \n+++ \n@@ -1,5 +1,4 @@\n-world!\n-Goodbye!\n+world\n 1\n 2\n End',
                    'new_value': 'world\n1\n2\nEnd',
                    'old_value': 'world!\nGoodbye!\n1\n2\nEnd'
                }
            }
        }
        assert result == ddiff

    def test_string_difference_ignore_case(self):
        t1 = "Hello"
        t2 = "hello"

        ddiff = DeepDiff(t1, t2)
        result = {'values_changed': {'root': {'new_value': 'hello', 'old_value': 'Hello'}}}
        assert result == ddiff

        ddiff = DeepDiff(t1, t2, ignore_string_case=True)
        result = {}
        assert result == ddiff

    def test_bytes(self):
        t1 = {
            1: 1,
            2: 2,
            3: 3,
            4: {
                "a": b"hello",
                "b": b"world!\nGoodbye!\n1\n2\nEnd",
                "c": b"\x80",
            }
        }
        t2 = {
            1: 1,
            2: 2,
            3: 3,
            4: {
                "a": b"hello",
                "b": b"world\n1\n2\nEnd",
                "c": b'\x81',
            }
        }

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                "root[4]['b']": {
                    'diff':
                    '--- \n+++ \n@@ -1,5 +1,4 @@\n-world!\n-Goodbye!\n+world\n 1\n 2\n End',
                    'new_value': b'world\n1\n2\nEnd',
                    'old_value': b'world!\nGoodbye!\n1\n2\nEnd'
                },
                "root[4]['c']": {
                    'new_value': b'\x81',
                    'old_value': b'\x80'
                }
            }
        }
        assert result == ddiff

    def test_unicode(self):
        t1 = {
            1: 1,
            2: 2,
            3: 3,
            4: {
                "a": "hello",
                "b": "world!\nGoodbye!\n1\n2\nEnd"
            }
        }
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n1\n2\nEnd"}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                "root[4]['b']": {
                    'diff':
                    '--- \n+++ \n@@ -1,5 +1,4 @@\n-world!\n-Goodbye!\n+world\n 1\n 2\n End',
                    'new_value': 'world\n1\n2\nEnd',
                    'old_value': 'world!\nGoodbye!\n1\n2\nEnd'
                }
            }
        }
        assert result == ddiff

    def test_type_change(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3]}}
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": "world\n\n\nEnd"}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'type_changes': {
                "root[4]['b']": {
                    'old_type': list,
                    'new_value': 'world\n\n\nEnd',
                    'old_value': [1, 2, 3],
                    'new_type': str
                }
            }
        }
        assert result == ddiff

    def test_list_difference(self):
        t1 = {
            1: 1,
            2: 2,
            3: 3,
            4: {
                "a": "hello",
                "b": [1, 2, 'to_be_removed', 'to_be_removed2']
            }
        }
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2]}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'iterable_item_removed': {
                "root[4]['b'][2]": "to_be_removed",
                "root[4]['b'][3]": 'to_be_removed2'
            }
        }
        assert result == ddiff

    def test_list_difference_add(self):
        t1 = [1, 2]
        t2 = [1, 2, 3, 5]
        ddiff = DeepDiff(t1, t2)
        result = {'iterable_item_added': {'root[2]': 3, 'root[3]': 5}}
        assert result == ddiff

    def test_list_difference2(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3, 10, 12]}}
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 3, 2]}}
        result = {
            'values_changed': {
                "root[4]['b'][2]": {
                    'new_value': 2,
                    'old_value': 3
                },
                "root[4]['b'][1]": {
                    'new_value': 3,
                    'old_value': 2
                }
            },
            'iterable_item_removed': {
                "root[4]['b'][3]": 10,
                "root[4]['b'][4]": 12
            }
        }
        ddiff = DeepDiff(t1, t2)
        assert result == ddiff

    def test_list_difference3(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 5]}}
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 3, 2, 5]}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                "root[4]['b'][2]": {
                    'new_value': 2,
                    'old_value': 5
                },
                "root[4]['b'][1]": {
                    'new_value': 3,
                    'old_value': 2
                }
            },
            'iterable_item_added': {
                "root[4]['b'][3]": 5
            }
        }
        assert result == ddiff

    def test_list_difference4(self):
        # TODO: Look into Levenshtein algorithm
        # So that the result is just insertion of "c" in this test.
        t1 = ["a", "b", "d", "e"]
        t2 = ["a", "b", "c", "d", "e"]
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[2]': {
                    'new_value': 'c',
                    'old_value': 'd'
                },
                'root[3]': {
                    'new_value': 'd',
                    'old_value': 'e'
                }
            },
            'iterable_item_added': {
                'root[4]': 'e'
            }
        }
        assert result == ddiff

    def test_list_of_booleans(self):
        t1 = [False, False, True, True]
        t2 = [False, False, False, True]
        ddiff = DeepDiff(t1, t2)
        assert {'values_changed': {'root[2]': {'new_value': False, 'old_value': True}}} == ddiff

    def test_set_of_none(self):
        """
        https://github.com/seperman/deepdiff/issues/64
        """
        ddiff = DeepDiff(set(), {None})
        assert {'set_item_added': {'root[None]'}} == ddiff

    def test_list_that_contains_dictionary(self):
        t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, {1: 1, 2: 2}]}}
        t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, {1: 3}]}}
        ddiff = DeepDiff(t1, t2)
        result = {
            'dictionary_item_removed': {"root[4]['b'][2][2]"},
            'values_changed': {
                "root[4]['b'][2][1]": {
                    'old_value': 1,
                    'new_value': 3
                }
            }
        }
        assert result == ddiff

    def test_set(self):
        t1 = {1, 2, 8}
        t2 = {1, 2, 3, 5}
        ddiff = DeepDiff(t1, t2)
        result = {
            'set_item_added': {'root[3]', 'root[5]'},
            'set_item_removed': {'root[8]'}
        }
        assert result == ddiff

    def test_set_strings(self):
        t1 = {"veggies", "tofu"}
        t2 = {"veggies", "tofu", "seitan"}
        ddiff = DeepDiff(t1, t2)
        result = {'set_item_added': {"root['seitan']"}}
        assert result == ddiff

    def test_frozenset(self):
        t1 = frozenset([1, 2, 'B'])
        t2 = frozenset([1, 2, 3, 5])
        ddiff = DeepDiff(t1, t2)
        result = {
            'set_item_added': {'root[3]', 'root[5]'},
            'set_item_removed': {"root['B']"}
        }
        assert result == ddiff

    def test_tuple(self):
        t1 = (1, 2, 8)
        t2 = (1, 2, 3, 5)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[2]': {
                    'old_value': 8,
                    'new_value': 3
                }
            },
            'iterable_item_added': {
                'root[3]': 5
            }
        }
        assert result == ddiff

    def test_named_tuples(self):
        from collections import namedtuple
        Point = namedtuple('Point', ['x', 'y'])
        t1 = Point(x=11, y=22)
        t2 = Point(x=11, y=23)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.y': {
                    'old_value': 22,
                    'new_value': 23
                }
            }
        }
        assert result == ddiff

    def test_enums(self):
        from enum import Enum

        class MyEnum(Enum):
            A = 1
            B = 2

        ddiff = DeepDiff(MyEnum.A, MyEnum(1))
        result = {}
        assert ddiff == result

        ddiff = DeepDiff(MyEnum.A, MyEnum.B)
        result = {
            'values_changed': {
                'root._name_': {
                    'old_value': 'A',
                    'new_value': 'B'
                },
                'root._value_': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert ddiff == result

    def test_custom_objects_change(self):
        t1 = CustomClass(1)
        t2 = CustomClass(2)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.a': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_custom_objects_slot_change(self):
        class ClassA:
            __slots__ = ('x', 'y')

            def __init__(self, x, y):
                self.x = x
                self.y = y

        t1 = ClassA(1, 1)
        t2 = ClassA(1, 2)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.y': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_custom_class_changes_with_slot_changes(self):
        class ClassA:
            __slots__ = ['x', 'y']

            def __init__(self, x, y):
                self.x = x
                self.y = y

        class ClassB:
            __slots__ = ['x']

        ddiff = DeepDiff(ClassA, ClassB)
        result = {'type_changes': {'root': {'old_type': ClassA, 'new_type': ClassB}}}
        assert result == ddiff

    def test_custom_class_changes_with_slot_change_when_ignore_type(self):
        class ClassA:
            __slots__ = ['x', 'y']

            def __init__(self, x, y):
                self.x = x
                self.y = y

        class ClassB:
            __slots__ = ['x']

        ddiff = DeepDiff(ClassA, ClassB, ignore_type_in_groups=[(ClassA, ClassB)])
        result = {'attribute_removed': ['root.y']}
        assert result == ddiff

    def test_custom_class_changes_none_when_ignore_type(self):
        ddiff1 = DeepDiff({'a': None}, {'a': 1}, ignore_type_subclasses=True, ignore_type_in_groups=[(int, float)])
        result = {
            'type_changes': {
                "root['a']": {
                    'old_type': type(None),
                    'new_type': int,
                    'old_value': None,
                    'new_value': 1
                }
            }
        }
        assert result == ddiff1

        ddiff2 = DeepDiff({'a': None}, {'a': '1'}, ignore_type_subclasses=True, ignore_type_in_groups=[(str, int, float, None)])
        assert {'values_changed': {"root['a']": {'new_value': '1', 'old_value': None}}} == ddiff2

        ddiff3 = DeepDiff({'a': '1'}, {'a': None}, ignore_type_subclasses=True, ignore_type_in_groups=[(str, int, float, None)])
        assert {'values_changed': {"root['a']": {'new_value': None, 'old_value': '1'}}} == ddiff3

        ddiff4 = DeepDiff({'a': {'b': None}}, {'a': {'b': '1'}}, ignore_type_subclasses=True, ignore_type_in_groups=[(str, int, float, None)])
        assert {'values_changed': {"root['a']['b']": {'new_value': '1', 'old_value': None}}} == ddiff4

        ddiff5 = DeepDiff({'a': {'b': '1'}}, {'a': {'b': None}}, ignore_type_subclasses=True, ignore_type_in_groups=[(str, int, float, None)])
        assert {'values_changed': {"root['a']['b']": {'new_value': None, 'old_value': '1'}}} == ddiff5

    def test_custom_object_changes_when_ignore_type_in_groups(self):
        class ClassA:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        class ClassB:
            def __init__(self, x):
                self.x = x

        class ClassC(ClassB):
            def __repr__(self):
                return "obj c"

        obj_a = ClassA(1, 2)
        obj_c = ClassC(3)
        ddiff = DeepDiff(obj_a, obj_c, ignore_type_in_groups=[(ClassA, ClassB)], ignore_type_subclasses=False)
        result = {'type_changes': {'root': {'old_type': ClassA, 'new_type': ClassC, 'old_value': obj_a, 'new_value': obj_c}}}
        assert result == ddiff

        ddiff = DeepDiff(obj_a, obj_c, ignore_type_in_groups=[(ClassA, ClassB)], ignore_type_subclasses=True)
        result = {'values_changed': {'root.x': {'new_value': 3, 'old_value': 1}}, 'attribute_removed': ['root.y']}
        assert result == ddiff

    def test_custom_objects_slot_in_parent_class_change(self):
        class ClassA:
            __slots__ = ['x']

        class ClassB(ClassA):
            __slots__ = ['y']

            def __init__(self, x, y):
                self.x = x
                self.y = y

        t1 = ClassB(1, 1)
        t2 = ClassB(2, 1)
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.x': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_custom_objects_with_single_protected_slot(self):
        class ClassA:
            __slots__ = '__a'

            def __init__(self):
                self.__a = 1

            def __str__(self):
                return str(self.__a)

        t1 = ClassA()
        t2 = ClassA()
        ddiff = DeepDiff(t1, t2)
        assert {} == ddiff

    def test_custom_objects_with_weakref_in_slots(self):
        class ClassA:
            __slots__ = ['a', '__weakref__']

            def __init__(self, a):
                self.a = a

        t1 = ClassA(1)
        t2 = ClassA(2)
        diff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.a': {
                    'new_value': 2,
                    'old_value': 1
                }
            },
        }
        assert result == diff

    def get_custom_objects_add_and_remove(self):
        class ClassA:
            a = 1

            def __init__(self, b):
                self.b = b
                self.d = 10

        t1 = ClassA(1)
        t2 = ClassA(2)
        t2.c = "new attribute"
        del t2.d
        return t1, t2

    def test_custom_objects_add_and_remove(self):
        t1, t2 = self.get_custom_objects_add_and_remove()
        ddiff = DeepDiff(t1, t2)
        result = {
            'attribute_added': {'root.c'},
            'values_changed': {
                'root.b': {
                    'new_value': 2,
                    'old_value': 1
                }
            },
            'attribute_removed': {'root.d'}
        }
        assert result == ddiff

    def test_custom_objects_add_and_remove_verbose(self):
        t1, t2 = self.get_custom_objects_add_and_remove()
        ddiff = DeepDiff(t1, t2, verbose_level=2)
        result = {
            'attribute_added': {
                'root.c': 'new attribute'
            },
            'attribute_removed': {
                'root.d': 10
            },
            'values_changed': {
                'root.b': {
                    'new_value': 2,
                    'old_value': 1
                }
            }
        }
        assert result == ddiff

    def get_custom_object_with_added_removed_methods(self):
        class ClassA:
            def method_a(self):
                pass

        t1 = ClassA()
        t2 = ClassA()

        def method_b(self):
            pass

        def method_c(self):
            return "hello"

        t2.method_b = method_b
        t2.method_a = method_c
        # Note that we are comparing ClassA instances. method_a originally was in ClassA
        # But we also added another version of it to t2. So it comes up as
        # added attribute.
        return t1, t2

    def test_custom_objects_add_and_remove_method(self):
        t1, t2 = self.get_custom_object_with_added_removed_methods()
        ddiff = DeepDiff(t1, t2)

        result = {'attribute_added': {'root.method_a', 'root.method_b'}}
        assert result == ddiff

    def test_custom_objects_add_and_remove_method_verbose(self):
        t1, t2 = self.get_custom_object_with_added_removed_methods()
        ddiff = DeepDiff(t1, t2, verbose_level=2)
        assert 'root.method_a' in ddiff['attribute_added']
        assert 'root.method_b' in ddiff['attribute_added']

    def test_set_of_custom_objects(self):
        member1 = CustomClass(13, 37)
        member2 = CustomClass(13, 37)
        t1 = {member1}
        t2 = {member2}
        ddiff = DeepDiff(t1, t2)
        result = {}
        assert result == ddiff

    def test_dictionary_of_custom_objects(self):
        member1 = CustomClass(13, 37)
        member2 = CustomClass(13, 37)
        t1 = {1: member1}
        t2 = {1: member2}
        ddiff = DeepDiff(t1, t2)
        result = {}
        assert result == ddiff

    def test_dictionary_with_string_keys(self):
        t1 = {"veggie": "carrots"}
        t2 = {"meat": "carrots"}

        diff = DeepDiff(t1, t2)
        assert {'dictionary_item_added': ["root['meat']"],
                'dictionary_item_removed': ["root['veggie']"]} == diff

    def test_dictionary_with_numeric_keys(self):
        t1 = {Decimal('10.01'): "carrots"}
        t2 = {10.01: "carrots"}
        diff = DeepDiff(t1, t2)
        assert {'dictionary_item_added': ["root[10.01]"], 'dictionary_item_removed': ["root[Decimal('10.01')]"]} == diff

    def test_loop(self):
        class LoopTest:
            def __init__(self, a):
                self.loop = self
                self.a = a

        t1 = LoopTest(1)
        t2 = LoopTest(2)

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.a': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_loop2(self):
        class LoopTestA:
            def __init__(self, a):
                self.loop = LoopTestB
                self.a = a

        class LoopTestB:
            def __init__(self, a):
                self.loop = LoopTestA
                self.a = a

        t1 = LoopTestA(1)
        t2 = LoopTestA(2)

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.a': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_loop3(self):
        class LoopTest:
            def __init__(self, a):
                self.loop = LoopTest
                self.a = a

        t1 = LoopTest(1)
        t2 = LoopTest(2)

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root.a': {
                    'old_value': 1,
                    'new_value': 2
                }
            }
        }
        assert result == ddiff

    def test_loop_in_lists(self):
        t1 = [1, 2, 3]
        t1.append(t1)

        t2 = [1, 2, 4]
        t2.append(t2)

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[2]': {
                    'new_value': 4,
                    'old_value': 3
                }
            }
        }
        assert result == ddiff

    def test_loop_in_lists2(self):
        t1 = [1, 2, [3]]
        t1[2].append(t1)
        t2 = [1, 2, [4]]
        t2[2].append(t2)

        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[2][0]': {
                    'old_value': 3,
                    'new_value': 4
                }
            }
        }
        assert result == ddiff

    def test_decimal(self):
        t1 = {1: Decimal('10.1')}
        t2 = {1: Decimal('2.2')}
        ddiff = DeepDiff(t1, t2)
        result = {
            'values_changed': {
                'root[1]': {
                    'new_value': Decimal('2.2'),
                    'old_value': Decimal('10.1')
                }
            }
        }
        assert result == ddiff

    def test_unicode_string_type_changes(self):
        """
        These tests were written when DeepDiff was in Python 2.
        Writing b"你好" throws an exception in Python 3 so can't be used for testing.
        These tests are currently useless till they are rewritten properly.
        """
        unicode_string = {"hello": "你好"}
        ascii_string = {"hello": "你好"}
        ddiff = DeepDiff(unicode_string, ascii_string)
        result = {}
        assert result == ddiff

    def test_unicode_string_value_changes(self):
        unicode_string = {"hello": "你好"}
        ascii_string = {"hello": "你好hello"}
        ddiff = DeepDiff(unicode_string, ascii_string)
        result = {
            'values_changed': {
                "root['hello']": {
                    'old_value': '你好',
                    'new_value': '你好hello'
                }
            }
        }
        assert result == ddiff

    def test_unicode_string_value_and_type_changes(self):
        unicode_string = {"hello": "你好"}
        ascii_string = {"hello": "你好hello"}
        ddiff = DeepDiff(unicode_string, ascii_string)
        # In python3, all string is unicode, so these 2 strings only diff
        # in values
        result = {
            'values_changed': {
                "root['hello']": {
                    'new_value': '你好hello',
                    'old_value': '你好'
                }
            }
        }
        assert result == ddiff

    def test_int_to_unicode_string(self):
        t1 = 1
        ascii_string = "你好"
        ddiff = DeepDiff(t1, ascii_string)
        # In python3, all string is unicode, so these 2 strings only diff
        # in values
        result = {
            'type_changes': {
                'root': {
                    'old_type': int,
                    'new_type': str,
                    'old_value': 1,
                    'new_value': '你好'
                }
            }
        }
        assert result == ddiff

    def test_int_to_unicode(self):
        t1 = 1
        unicode_string = "你好"
        ddiff = DeepDiff(t1, unicode_string)
        # In python3, all string is unicode, so these 2 strings only diff
        # in values
        result = {
            'type_changes': {
                'root': {
                    'old_type': int,
                    'new_type': str,
                    'old_value': 1,
                    'new_value': '你好'
                }
            }
        }
        assert result == ddiff

    @pytest.mark.parametrize("t1, t2, ignore_numeric_type_changes, significant_digits, number_format_notation, result", [
        (43.265798602382986, 43.71677762295505, False, 0, "f", {'values_changed': {'root': {'new_value': 43.71677762295505, 'old_value': 43.265798602382986}}}),  # Note that it rounds the number so one becomes 43 and the other one is 44
        (Decimal('2.5'), Decimal('1.5'), False, 0, "f", {}),
        (Decimal('2.5'), Decimal('1.5'), False, 1, "f", {'values_changed': {'root': {'new_value': Decimal('1.5'), 'old_value': Decimal('2.5')}}}),
        (Decimal('2.5'), Decimal(2.5), False, 3, "f", {}),
        (1024, 1022, False, 2, "e", {}),
        ({"key": [Decimal('2.0001'), Decimal('20000.0001')]}, {"key": [2.0002, 20000.0002]}, True, 4, "e", {'values_changed': {"root['key'][0]": {'new_value': 2.0002, 'old_value': Decimal('2.0001')}}})
    ])
    def test_significant_digits_and_notation(self, t1, t2, ignore_numeric_type_changes, significant_digits, number_format_notation, result):
        ddiff = DeepDiff(t1, t2, significant_digits=significant_digits, number_format_notation=number_format_notation,
                         ignore_numeric_type_changes=ignore_numeric_type_changes)
        assert result == ddiff

    def test_significant_digits_for_complex_imaginary_part(self):
        t1 = 1.23 + 1.222254j
        t2 = 1.23 + 1.222256j
        ddiff = DeepDiff(t1, t2, significant_digits=4)
        assert {} == ddiff
        result = {
            'values_changed': {
                'root': {
                    'new_value': (1.23 + 1.222256j),
                    'old_value': (1.23 + 1.222254j)
                }
            }
        }
        ddiff = DeepDiff(t1, t2, significant_digits=5)
        assert result == ddiff

    def test_significant_digits_for_complex_real_part(self):
        t1 = 1.23446879 + 1.22225j
        t2 = 1.23446764 + 1.22225j
        ddiff = DeepDiff(t1, t2, significant_digits=5)
        assert {} == ddiff

    def test_significant_digits_for_list_of_floats(self):
        t1 = [1.2344, 5.67881, 6.778879]
        t2 = [1.2343, 5.67882, 6.778878]
        ddiff = DeepDiff(t1, t2, significant_digits=3)
        assert {} == ddiff
        ddiff = DeepDiff(t1, t2, significant_digits=4)
        result = {
            'values_changed': {
                'root[0]': {
                    'new_value': 1.2343,
                    'old_value': 1.2344
                }
            }
        }
        assert result == ddiff
        ddiff = DeepDiff(t1, t2, significant_digits=5)
        result = {
            'values_changed': {
                'root[0]': {
                    'new_value': 1.2343,
                    'old_value': 1.2344
                },
                'root[1]': {
                    'new_value': 5.67882,
                    'old_value': 5.67881
                }
            }
        }
        assert result == ddiff
        ddiff = DeepDiff(t1, t2)
        ddiff2 = DeepDiff(t1, t2, significant_digits=6)
        assert ddiff2 == ddiff

    def test_negative_significant_digits(self):
        with pytest.raises(ValueError):
            DeepDiff(1, 1, significant_digits=-1)

    @pytest.mark.parametrize("t1, t2, significant_digits, expected_result",
                             [
                                 (10, 10.0, 5, {}),
                                 (10, 10.2, 5, {'values_changed': {'root': {'new_value': 10.2, 'old_value': 10}}}),
                                 (10, 10.2, 0, {}),
                                 (Decimal(10), 10, 0, {}),
                                 (Decimal(10), 10, 10, {}),
                                 (Decimal(10), 10.0, 0, {}),
                                 (Decimal(10), 10.0, 10, {}),
                                 (Decimal('10.0'), 10.0, 5, {}),
                                 (Decimal('10.01'), 10.01, 1, {}),
                                 (Decimal('10.01'), 10.01, 2, {}),
                                 (Decimal('10.01'), 10.01, 5, {}),
                                 (Decimal('10.01'), 10.01, 8, {}),
                                 (Decimal('10.010'), 10.01, 3, {}),
                                 (Decimal('100000.1'), 100000.1, 0, {}),
                                 (Decimal('100000.1'), 100000.1, 1, {}),
                                 (Decimal('100000.1'), 100000.1, 5, {}),
                                 (Decimal('100000'), 100000.1, 0, {}),
                                 (Decimal('100000'), 100000.1, 1, {'values_changed': {'root': {'new_value': 100000.1, 'old_value': Decimal('100000')}}}),
                             ])
    def test_decimal_digits(self, t1, t2, significant_digits, expected_result):
        ddiff = DeepDiff(t1, t2, ignore_numeric_type_changes=True, ignore_string_type_changes=True, significant_digits=significant_digits)
        assert expected_result == ddiff

    def test_ignore_type_in_groups(self):
        t1 = [1, 2, 3]
        t2 = [1.0, 2.0, 3.0]
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=DeepDiff.numbers)
        assert not ddiff

    def test_ignore_type_in_groups2(self):
        t1 = [1, 2, 3]
        t2 = [1.0, 2.0, 3.3]
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=DeepDiff.numbers)
        result = {'values_changed': {'root[2]': {'new_value': 3.3, 'old_value': 3}}}
        assert result == ddiff

    def test_ignore_type_in_groups3(self):
        t1 = {Decimal('10.01'): "carrots"}
        t2 = {10.01: "carrots"}

        diff1 = DeepDiff(t1, t2)

        diff2 = DeepDiff(t1, t2, ignore_numeric_type_changes=True)

        diff3 = DeepDiff(t1, t2, ignore_type_in_groups=DeepDiff.numbers)
        assert {'dictionary_item_added': ["root[10.01]"], 'dictionary_item_removed': ["root[Decimal('10.01')]"]} == diff1
        assert {} == diff2 == diff3

    def test_ignore_type_in_groups_just_numbers(self):
        t1 = [1, 2, 3, 'a']
        t2 = [1.0, 2.0, 3.3, b'a']
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=[DeepDiff.numbers])
        result = {'values_changed': {'root[2]': {'new_value': 3.3, 'old_value': 3}},
                  'type_changes': {'root[3]': {'new_type': bytes,
                                               'new_value': b'a',
                                               'old_type': str,
                                               'old_value': 'a'}}
                  }
        assert result == ddiff

    def test_ignore_type_in_groups_numbers_and_strings(self):
        t1 = [1, 2, 3, 'a']
        t2 = [1.0, 2.0, 3.3, b'a']
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=[DeepDiff.numbers, DeepDiff.strings])
        result = {'values_changed': {'root[2]': {'new_value': 3.3, 'old_value': 3}}}
        assert result == ddiff

    def test_ignore_type_in_groups_none_and_objects(self):
        t1 = [1, 2, 3, 'a', None]
        t2 = [1.0, 2.0, 3.3, b'a', 'hello']
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=[(1, 1.0), (None, str, bytes)])
        result = {
            'values_changed': {
                'root[2]': {
                    'new_value': 3.3,
                    'old_value': 3
                },
                'root[4]': {
                    'new_value': 'hello',
                    'old_value': None
                }
            }
        }
        assert result == ddiff

    def test_ignore_type_in_groups_str_and_datetime(self):
        now = datetime.datetime.utcnow()
        t1 = [1, 2, 3, 'a', now]
        t2 = [1, 2, 3, 'a', 'now']
        ddiff = DeepDiff(t1, t2, ignore_type_in_groups=[(str, bytes, datetime.datetime)])
        result = {'values_changed': {'root[4]': {'new_value': 'now', 'old_value': now}}}
        assert result == ddiff

    @pytest.mark.parametrize("t1, t2, significant_digits, result", [
        ([0.1], [Decimal('0.10')], 55,
            {'values_changed': {'root[0]': {'new_value': Decimal('0.10'), 'old_value': 0.1}}}),  # Due to floating point arithmetics with high significant digits.
        ([0.1], [Decimal('0.10')], 5, {}),  # Same inputs as above but with significant digits that is low.
        ([-0.1], [-Decimal('0.10')], 5, {}),
        ([-Decimal('0.102')], [-Decimal('0.10')], 2, {}),
        ([1], [Decimal('1.00000002')], 3, {}),
    ])
    def test_ignore_numeric_type_changes_numbers_when_decimal(self, t1, t2, significant_digits, result):
        ddiff = DeepDiff(t1, t2, ignore_numeric_type_changes=True, significant_digits=significant_digits)
        assert result == ddiff

    @pytest.mark.skip(reason="REMAPPING DISABLED UNTIL KEY NAMES CHANGE AGAIN IN FUTURE")
    def test_base_level_dictionary_remapping(self):
        """
        Since subclassed dictionaries that override __getitem__ treat newdict.get(key)
        differently than newdict['key'], we are unable to create a unittest with
        self.assertIn() and have to resort to fetching the values of two keys and making
        sure they are the same value.
        """
        t1 = {1: 1, 2: 2}
        t2 = {2: 2, 3: 3}
        ddiff = DeepDiff(t1, t2)
        assert ddiff['dic_item_added'] == ddiff['dictionary_item_added']
        assert ddiff['dic_item_removed'] == ddiff['dictionary_item_removed']

    @pytest.mark.skip(reason="REMAPPING DISABLED UNTIL KEY NAMES CHANGE AGAIN IN FUTURE")
    def test_index_and_repeat_dictionary_remapping(self):
        t1 = [1, 3, 1, 4]
        t2 = [4, 4, 1]
        ddiff = DeepDiff(t1, t2, ignore_order=True, report_repetition=True)
        assert ddiff['repetition_change']['root[0]']['newindexes'] == ddiff['repetition_change']['root[0]']['new_indexes']
        assert ddiff['repetition_change']['root[0]']['newrepeat'] == ddiff['repetition_change']['root[0]']['new_repeat']
        assert ddiff['repetition_change']['root[0]']['oldindexes'] == ddiff['repetition_change']['root[0]']['old_indexes']
        assert ddiff['repetition_change']['root[0]']['oldrepeat'] == ddiff['repetition_change']['root[0]']['old_repeat']

    @pytest.mark.skip(reason="REMAPPING DISABLED UNTIL KEY NAMES CHANGE AGAIN IN FUTURE")
    def test_value_and_type_dictionary_remapping(self):
        t1 = {1: 1, 2: 2}
        t2 = {1: 1, 2: '2'}
        ddiff = DeepDiff(t1, t2)
        assert ddiff['type_changes']['root[2]']['newtype'] == ddiff['type_changes']['root[2]']['new_type']
        assert ddiff['type_changes']['root[2]']['newvalue'] == ddiff['type_changes']['root[2]']['new_value']
        assert ddiff['type_changes']['root[2]']['oldtype'] == ddiff['type_changes']['root[2]']['old_type']
        assert ddiff['type_changes']['root[2]']['oldvalue'] == ddiff['type_changes']['root[2]']['old_value']

    def test_skip_type(self):
        l1 = logging.getLogger("test")
        l2 = logging.getLogger("test2")
        t1 = {"log": l1, 2: 1337}
        t2 = {"log": l2, 2: 1337}
        ddiff = DeepDiff(t1, t2, exclude_types={logging.Logger})
        assert {} == ddiff

        t1 = {"log": "book", 2: 1337}
        t2 = {"log": l2, 2: 1337}
        ddiff = DeepDiff(t1, t2, exclude_types={logging.Logger})
        assert {} == ddiff

    def test_skip_path1(self):
        t1 = {
            "for life": "vegan",
            "ingredients": ["no meat", "no eggs", "no dairy"]
        }
        t2 = {
            "for life": "vegan",
            "ingredients": ["veggies", "tofu", "soy sauce"]
        }
        ddiff = DeepDiff(t1, t2, exclude_paths={"root['ingredients']"})
        assert {} == ddiff

    def test_skip_path2(self):
        t1 = {
            "for life": "vegan",
            "ingredients": ["no meat", "no eggs", "no dairy"]
        }
        t2 = {"for life": "vegan"}
        ddiff = DeepDiff(t1, t2, exclude_paths={"root['ingredients']"})
        assert {} == ddiff

    def test_skip_path2_reverse(self):
        t1 = {
            "for life": "vegan",
            "ingredients": ["no meat", "no eggs", "no dairy"]
        }
        t2 = {"for life": "vegan"}
        ddiff = DeepDiff(t2, t1, exclude_paths={"root['ingredients']"})
        assert {} == ddiff

    def test_skip_path4(self):
        t1 = {
            "for life": "vegan",
            "ingredients": ["no meat", "no eggs", "no dairy"]
        }
        t2 = {"for life": "vegan", "zutaten": ["veggies", "tofu", "soy sauce"]}
        ddiff = DeepDiff(t1, t2, exclude_paths={"root['ingredients']"})
        assert 'dictionary_item_added' in ddiff, {}
        assert 'dictionary_item_removed' not in ddiff, {}

    def test_skip_path5(self):
        t1 = [{'cn': 'tuser', 'first_name': 'Test', 'last_name': 'User', 'name': 'Test User', 'email': 'tuser@example.com'}]
        t2 = [{'name': 'Test User', 'email': 'tuser@example.com'}]

        diff = DeepDiff(
            t1,
            t2,
            ignore_order=True,
            exclude_paths={
                "root[0]['cn']",
                "root[0]['first_name']",
                "root[0]['last_name']"
            })

        assert not diff

    def test_skip_custom_object_path(self):
        t1 = CustomClass(1)
        t2 = CustomClass(2)
        ddiff = DeepDiff(t1, t2, exclude_paths=['root.a'])
        result = {}
        assert result == ddiff

    def test_skip_list_path(self):
        t1 = ['a', 'b']
        t2 = ['a']
        ddiff = DeepDiff(t1, t2, exclude_paths=['root[1]'])
        result = {}
        assert result == ddiff

    def test_skip_dictionary_path(self):
        t1 = {1: {2: "a"}}
        t2 = {1: {}}
        ddiff = DeepDiff(t1, t2, exclude_paths=['root[1][2]'])
        result = {}
        assert result == ddiff

    def test_skip_dictionary_path_with_custom_object(self):
        obj1 = CustomClass(1)
        obj2 = CustomClass(2)

        t1 = {1: {2: obj1}}
        t2 = {1: {2: obj2}}
        ddiff = DeepDiff(t1, t2, exclude_paths=['root[1][2].a'])
        result = {}
        assert result == ddiff

    # TODO: fix it for python 3.5, 3.6 and pypy3
    def test_skip_regexp(self):
        t1 = [{'a': 1, 'b': 2}, {'c': 4, 'b': 5}]
        t2 = [{'a': 1, 'b': 3}, {'c': 4, 'b': 5}]
        ddiff = DeepDiff(t1, t2, exclude_regex_paths=[r"root\[\d+\]\['b'\]"])
        result = {}
        assert result == ddiff

    def test_skip_exclude_obj_callback(self):
        def exclude_obj_callback(obj, path):
            return True if "skip" in path or isinstance(obj, int) else False

        t1 = {"x": 10, "y": "b", "z": "c", "skip_1": 0}
        t2 = {"x": 12, "y": "b", "z": "c", "skip_2": 0}
        ddiff = DeepDiff(t1, t2, exclude_obj_callback=exclude_obj_callback)
        result = {}
        assert result == ddiff

    def test_skip_str_type_in_dictionary(self):
        t1 = {1: {2: "a"}}
        t2 = {1: {}}
        ddiff = DeepDiff(t1, t2, exclude_types=[str])
        result = {}
        assert result == ddiff

    def test_skip_str_type_in_dict_on_list(self):
        t1 = [{1: "a"}]
        t2 = [{}]
        ddiff = DeepDiff(t1, t2, exclude_types=[str])
        result = {}
        assert result == ddiff

    def test_unknown_parameters(self):
        with pytest.raises(ValueError):
            DeepDiff(1, 1, wrong_param=2)

    def test_bad_attribute(self):
        class Bad:
            __slots__ = ['x', 'y']

            def __getattr__(self, key):
                raise AttributeError("Bad item")

            def __str__(self):
                return "Bad Object"

        t1 = Bad()
        t2 = Bad()

        ddiff = DeepDiff(t1, t2)
        result = {'unprocessed': ['root: Bad Object and Bad Object']}
        assert result == ddiff

    def test_dict_none_item_removed(self):
        t1 = {1: None, 2: 2}
        t2 = {2: 2}
        ddiff = DeepDiff(t1, t2)
        result = {
            'dictionary_item_removed': {'root[1]'}
        }
        assert result == ddiff

    def test_list_none_item_removed(self):
        t1 = [1, 2, None]
        t2 = [1, 2]
        ddiff = DeepDiff(t1, t2)
        result = {
            'iterable_item_removed': {'root[2]': None}
        }
        assert result == ddiff

    def test_non_subscriptable_iterable(self):
        def gen1():
            yield 42
            yield 1337
            yield 31337

        def gen2():
            yield 42
            yield 1337

        t1 = gen1()
        t2 = gen2()
        ddiff = DeepDiff(t1, t2)

        result = {'iterable_item_removed': {'root[2]': 31337}}
        # Note: In text-style results, we currently pretend this stuff is subscriptable for readability

        assert result == ddiff

    @pytest.mark.parametrize('t1, t2, params, expected_result', [
        (float('nan'), float('nan'), {}, ['values_changed']),
        (float('nan'), float('nan'), {'ignore_nan_inequality': True}, []),
        ([1, float('nan')], [1, float('nan')], {'ignore_nan_inequality': True}, []),
    ])
    @pytest.mark.skipif(pypy3, reason="some versions of pypy3 have nan==nan")
    def test_ignore_nan_inequality(self, t1, t2, params, expected_result):
        assert expected_result == list(DeepDiff(t1, t2, **params).keys())

    @pytest.mark.parametrize('ignore_order, ignore_private_variables, expected', [
        (True, True, {}),
        (False, True, {}),
        (True, False, {'values_changed': {"root[0]['schema']['items']['__ref']": {'new_value': 2, 'old_value': 1}}}),
        (False, False, {'values_changed': {"root[0]['schema']['items']['__ref']": {'new_value': 2, 'old_value': 1}}}),
    ])
    def test_private_variables(self, ignore_order, ignore_private_variables, expected):
        t1 = [{'in': 'body', 'name': 'params', 'description': 'params', 'required': True, 'schema': {'type': 'array', 'items': {'__ref': 1}}}]
        t2 = [{'in': 'body', 'name': 'params', 'description': 'params', 'required': True, 'schema': {'type': 'array', 'items': {'__ref': 2}}}]
        diff = DeepDiff(t1, t2, ignore_order=ignore_order, ignore_private_variables=ignore_private_variables)
        assert expected == diff

    def test_group_by1(self):
        t1 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB', 'name': 'James', 'last_name': 'Blue'},
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        t2 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB', 'name': 'James', 'last_name': 'Brown'},
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        diff = DeepDiff(t1, t2)
        expected = {'values_changed': {"root[1]['last_name']": {
            'new_value': 'Brown',
            'old_value': 'Blue'}}}
        assert expected == diff

        diff = DeepDiff(t1, t2, group_by='id')
        expected_grouped = {'values_changed': {"root['BB']['last_name']": {
            'new_value': 'Brown',
            'old_value': 'Blue'}}}
        assert expected_grouped == diff

    def test_group_by_key_missing(self):
        t1 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB', 'name': 'James', 'last_name': 'Blue'},
            {'name': 'Mike', 'last_name': 'Apple'},
        ]

        t2 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB', 'name': 'James', 'last_name': 'Blue'},
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        diff = DeepDiff(t1, t2, group_by='id')
        expected = {'dictionary_item_added': ["root[2]['id']"]}
        assert expected == diff

    def test_group_by_not_dict1(self):
        t1 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            None,
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        t2 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB'},
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        diff = DeepDiff(t1, t2, group_by='id')
        expected = {
            'type_changes': {
                'root[1]': {
                    'old_type': None.__class__,
                    'new_type': dict,
                    'old_value': None,
                    'new_value': {
                        'id': 'BB'
                    }
                }
            },
        }
        assert expected == diff

    def test_group_by_not_dict2(self):
        t1 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            {'id': 'BB'},
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        t2 = [
            {'id': 'AA', 'name': 'Joe', 'last_name': 'Nobody'},
            None,
            {'id': 'CC', 'name': 'Mike', 'last_name': 'Apple'},
        ]

        diff = DeepDiff(t1, t2, group_by='id')
        expected = {
            'type_changes': {
                'root[1]': {
                    'old_type': dict,
                    'new_type': None.__class__,
                    'new_value': None,
                    'old_value': {
                        'id': 'BB'
                    }
                }
            },
        }
        assert expected == diff

    def test_group_by_not_list_of_dicts(self):
        t1 = {1: 2}

        t2 = {1: 3}

        diff = DeepDiff(t1, t2, group_by='id')
        expected = {'values_changed': {'root[1]': {'new_value': 3, 'old_value': 2}}}
        assert expected == diff
