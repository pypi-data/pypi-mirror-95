# Multimethod-dispatcher

![Tests and Release](https://github.com/sanjP10/multimethod/workflows/Tests%20and%20Release/badge.svg?branch=master)
![CodeQL](https://github.com/sanjP10/multimethod/workflows/CodeQL/badge.svg)
![Build and Publish](https://github.com/sanjP10/multimethod/workflows/Build%20and%20Publish/badge.svg)

This module that enables the use of the same function name but with variable dispatch keys.
This allows different object types or values to execute different functions but with the same name.
Similar to Object Orientation where objects can have their own implementation of a function, this is 
the functional response to this. Similar to [Clojure's Multimethod](https://clojure.org/reference/multimethods#_isa_based_dispatch)

This originates from Alex Bard's [blog post](https://adambard.com/blog/implementing-multimethods-in-python/)

There are two annotations:
* `@multi` evaluates the arguments to return a unique key which determines which method is called.
* `@method` is used to declare how that unique key is handled


The following code is an example of having multiple dictionaries with common elements, but handling
the equation differently.
```python
from multimethod import method, multi

@multi
def area(shape):
    """Multimethod dispatch key"""
    return shape.get('type')


@method(area, 'rectangle')
def area(rectangle):
    """Get area of a rectangle"""
    return rectangle.get('width') * rectangle.get('height')


@method(area, 'circle')
def area(circle):
    """Get area of a circle"""
    return circle.get('radius') ** 2 * 3.14159

area({'type': 'circle', 'radius': 0.5}) # => 0.7853975
area({'type': 'rectangle', 'width': 5, 'height': 8}) # => 40

```

This example is a more complicated version, evaluating on type and has a optional parameter for date of birth
```python
from datetime import datetime
from multimethod import method, multi


class Person:
    """Person object to hold name and dob"""
    def __init__(self, name, dob):
        self.name = name
        self.dob = datetime.strptime(dob, '%Y-%m-%d')

    def get_name(self):
        """Return name"""
        return self.name

    def get_dob_as_str(self):
        """Return dob as string"""
        return self.dob.strftime('%Y-%m-%d')

@multi
def get_name(obj, _=None):
    """Multimethod dispatch key"""
    return obj.__class__


@method(get_name, dict)
def get_name(obj, _=None):
    """Dictionary function for getting name and dob from dict"""
    return "{} is born on {}".format(obj.get('name'), obj.get('dob'))


@method(get_name, str)
def get_name(obj, dob):
    """Dictionary function for getting name and dob from string"""
    return "{} is born on {}".format(obj, dob)


@method(get_name, Person)
def get_name(obj, _=None):
    """Person object type for getting name and dob"""
    return "{} is born on {}".format(obj.get_name(), obj.get_dob_as_str())


@method(get_name)  # Default
def get_name(*args, **kwargs):  # pylint: disable=W0613
    """Default response for any other object type"""
    return "No name"


person = Person('Steve', '2019-06-01')
get_name(person) # => 'Steve is born on 2019-06-01'
get_name({'name': 'Tom', 'dob': '2019-06-01'}) # => 'Tom is born on 2019-06-01'
get_name('George', '2019-06-01') # => 'George is born on 2019-06-01'
get_name(2) # => "No name"
```
