### Abstract Factory Pattern

In simple terms, it is a factory of factories. You must be wondering what a factory pattern is? 

A factory pattern is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.


```python

class Car:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class Alto(Car):
    def __init__(self):
        super().__init__("Alto")

class Swift(Car):
    def __init__(self):
        super().__init__("Swift")

class Mercedes(Car):
    def __init__(self):
        super().__init__("Mercedes")

class BMW(Car):
    def __init__(self):
        super().__init__("BMW")


class CarFactory:
    def create_car(self, name):
        if name == "Alto":
            return Alto()
        elif name == "Swift":
            return Swift()


class LuxuryCarFactory:
    def create_car(self, name):
        if name == "Mercedes":
            return Mercedes()
        elif name == "BMW":
            return BMW()


car_type = "LUXURY"
if car_type == "LUXURY":
    car_factory = LuxuryCarFactory()
else:
    car_factory = CarFactory()


car_factory.create_car("Alto")

```



