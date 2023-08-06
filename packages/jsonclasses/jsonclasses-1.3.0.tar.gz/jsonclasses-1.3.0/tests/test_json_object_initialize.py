import unittest
from typing import Optional
from jsonclasses import jsonclass, JSONObject, ValidationException, types
from datetime import datetime, date


class TestJSONObjectInitialize(unittest.TestCase):

    def test_initialize_without_arguments(self):
        @jsonclass(class_graph='test_initialize_1')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact()
        self.assertEqual(contact.__fdict__, {'name': None, 'address': None})

    def test_initialize_with_keyed_arguments(self):
        @jsonclass(class_graph='test_initialize_2')
        class BusinessCard(JSONObject):
            name: str
            phone_no: str
        card = BusinessCard(name='John', phone_no='012345678')
        self.assertEqual(card.__fdict__, {'name': 'John', 'phone_no': '012345678'})

    def test_initialize_with_keyed_arguments_fill_none_on_blank_keys(self):
        @jsonclass(class_graph='test_initialize_3')
        class Point(JSONObject):
            x: int
            y: int
        point = Point(x=50)
        self.assertEqual(point.__fdict__, {'x': 50, 'y': None})

    def test_initialize_with_keyed_arguments_remove_redundant_keys(self):
        @jsonclass(class_graph='test_initialize_4', strict_input=False)
        class Size(JSONObject):
            width: float
            height: float
        size = Size(width=10.5, height=7.5, depth=2.5)
        self.assertEqual(size.__fdict__, {'width': 10.5, 'height': 7.5})

    def test_initialize_with_a_dict(self):
        @jsonclass(class_graph='test_initialize_5')
        class Location(JSONObject):
            longitude: float
            latitude: float
        location = Location(**{'longitude': 0, 'latitude': 30})
        self.assertEqual(location.__fdict__, {'longitude': 0, 'latitude': 30})

    def test_initialize_with_dict_fill_none_on_blank_keys(self):
        @jsonclass(class_graph='test_initialize_6')
        class Point(JSONObject):
            x: int
            y: int
        input = {'x': 50}
        point = Point(**input)
        self.assertEqual(point.__fdict__, {'x': 50, 'y': None})

    def test_initialize_with_dict_remove_redundant_keys(self):
        @jsonclass(class_graph='test_initialize_7', strict_input=False)
        class Size(JSONObject):
            width: float
            height: float
        input = {'width': 10.5, 'height': 7.5, 'depth': 2.5}
        size = Size(**input)
        self.assertEqual(size.__fdict__, {'width': 10.5, 'height': 7.5})

    def test_initialize_fill_default_values_for_blank_keys(self):
        @jsonclass(class_graph='test_initialize_8')
        class Student(JSONObject):
            student_id: int = 5
            name: str = 'Student X'
        student = Student()
        self.assertEqual(student.__fdict__, {'student_id': 5, 'name': 'Student X'})

    def test_initialize_with_value_passed_in_rather_than_default_value(self):
        @jsonclass(class_graph='test_initialize_9')
        class Employee(JSONObject):
            no: int = 3
            name: str = 'Employee D'
        employee = Employee(no=20, name='John Larryson')
        self.assertEqual(employee.__fdict__, {'no': 20, 'name': 'John Larryson'})

    def test_initialize_auto_convert_camelcase_keys_into_snakecase(self):
        @jsonclass(class_graph='test_initialize_10')
        class Coupon(JSONObject):
            minimum_purchase_value: int
            discount_rate: float
        coupon = Coupon(**{'minimumPurchaseValue': 1000, 'discountRate': 0.5})
        self.assertEqual(coupon.minimum_purchase_value, 1000)
        self.assertEqual(coupon.discount_rate, 0.5)

    def test_initialize_auto_convert_json_date_string_to_date(self):
        @jsonclass(class_graph='test_initialize_11')
        class Semester(JSONObject):
            start: date
            end: date
        semester = Semester(**{'start': '2020-02-20', 'end': '2020-06-30'})
        self.assertEqual(
            semester.__fdict__,
            {
                'start': date.fromisoformat('2020-02-20'),
                'end': date.fromisoformat('2020-06-30')
            }
        )

    def test_initialize_auto_convert_json_datetime_string_to_date(self):
        @jsonclass(class_graph='test_initialize_12')
        class Semester(JSONObject):
            start: date
            end: date
        semester = Semester(**{'start': '2020-02-20T00:00:00.000Z', 'end': '2020-06-30T03:03:03.333Z'})
        self.assertEqual(
            semester.__fdict__,
            {
                'start': date.fromisoformat('2020-02-20'),
                'end': date.fromisoformat('2020-06-30')
            }
        )

    def test_initialize_auto_convert_json_datetime_string_to_datetime(self):
        @jsonclass(class_graph='test_initialize_13')
        class Timer(JSONObject):
            expired_at: datetime
        timer = Timer(**{'expiredAt': '2020-08-29T06:38:34.242Z'})
        self.assertEqual(
            timer.__fdict__,
            {
                'expired_at': datetime.fromisoformat('2020-08-29T06:38:34.242000')
            }
        )

    def test_initialize_date_with_date(self):
        @jsonclass(class_graph='test_initialize_14')
        class Semester(JSONObject):
            start: date
            end: date
        start = date.fromisoformat('2020-10-10')
        end = date.fromisoformat('2020-12-12')
        semester = Semester(start=start, end=end)
        self.assertEqual(semester.start, start)
        self.assertEqual(semester.end, end)

    def test_initialize_datetime_with_datetime(self):
        @jsonclass(class_graph='test_initialize_15')
        class Timer(JSONObject):
            expired_at: datetime
        expired_at = datetime.fromisoformat('2020-10-10T05:03:02.999888')
        timer = Timer(**{'expiredAt': expired_at})
        self.assertEqual(timer.expired_at, expired_at)

    def test_initialize_strict_raises_on_unallowed_keys(self):
        @jsonclass(class_graph='test_initialize_16', strict_input=True)
        class Timer(JSONObject):
            expired_at: datetime
        expired_at = datetime.fromisoformat('2020-10-10T05:03:02.999888')
        with self.assertRaisesRegex(ValidationException, "'boom': Key 'boom' is not allowed."):
            Timer(**{'expiredAt': expired_at, 'boom': True})

    def test_initialize_strict_raises_on_nested_unallowed_keys(self):
        @jsonclass(class_graph='test_initialize_16', strict_input=True)
        class Friend(JSONObject):
            name: str

        @jsonclass(class_graph='test_initialize_16', strict_input=True)
        class User(JSONObject):
            friends: list[Friend]

        with self.assertRaisesRegex(ValidationException, "'friends.0.age': Key 'age' at 'friends.0' is not allowed."):
            User(**{'friends': [{'name': 'John', 'age': 15}]})

    def test_initialize_strict_handle_correctly_for_multiple_inheritance(self):
        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class BaseObject(JSONObject):
            pass

        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class DBObject(BaseObject):
            id: str = (types.str.readonly.primary.default(lambda: str())
                       .required)
            created_at: datetime = (types.datetime.readonly.timestamp('created')
                                    .default(datetime.now).required)
            updated_at: datetime = (types.datetime.readonly.timestamp('updated')
                                    .default(datetime.now).setonsave(datetime.now)
                                    .required)
            deleted_at: Optional[datetime] = (types.datetime.readonly
                                              .timestamp('deleted'))

        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class MyObject(DBObject):
            name: str
            age: int

        input = {'name': 'John', 'age': 27}
        MyObject(**input)
