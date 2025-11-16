import pytest


def test_equal():
    assert 1 == 1
    # assert 1 == 2 fail

def test_bool():
    validated = True
    assert validated

def test_is_instance():
    assert isinstance("this is a str", str)

def test_object():
    class Student:
        def __init__(self, first_name: str, last_name: str, major: str, year: int):
            self.first_name = first_name
            self.last_name = last_name
            self.major = major
            self.year = year

    student = Student(first_name="John", last_name="Smith",major="CS", year=3)
    assert student.first_name == "John", "The first name should be John..."
    assert student.last_name == "Smith"
    assert student.major == "CS"
    assert student.year == 3
    assert isinstance(student.year, int)



class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year


@pytest.fixture
def reusable_test_object():
    return Student(first_name="Bob", last_name="Doe", major="Art", year=2)

def test_student(reusable_test_object):
    assert reusable_test_object.first_name == "Bob", "The reusable test has Bob for first name"
    assert reusable_test_object.last_name == "Doe"
