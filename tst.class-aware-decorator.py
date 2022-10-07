from pprint import pprint


def decorate(func):
    print("decorate", func)
    print(dir(func))
    pprint({k: getattr(func, k) for k in dir(func)})

    return func


class MyClass:
    @decorate
    @staticmethod
    def foo(name):
        return name


class TestClass:
    def method(self, name):
        return name

    @classmethod
    def class_method(self, name):
        return name

    @staticmethod
    def static_method(self, name):
        return name


tc = TestClass()
