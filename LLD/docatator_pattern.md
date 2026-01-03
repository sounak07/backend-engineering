### Decorator Pattern

A pattern that allows us to add new functionality to an object at runtime without modifying its structure.

Instead of creating subclasses for every new functionality, this pattern uses composition, a decorator wraps an object extending its behavior without updating its interface.


```python

class BasePizza:
    def get_cost(self):
        return 10

    def get_ingredients(self):
        return "Tomato, Cheese"


class Margherita(BasePizza):
    def get_cost(self):
        return 10

    def get_ingredients(self):
        return "Tomato, Cheese"


class ExtraCheese(BasePizza):
    def __init__(self, pizza):
        self.pizza = pizza

    def get_cost(self):
        return self.pizza.get_cost() + 2

    def get_ingredients(self):
        return self.pizza.get_ingredients() + ", Extra Cheese"


class ThickPanPizza(BasePizza):
    def __init__(self, pizza):
        self.pizza = pizza

    def get_cost(self):
        return self.pizza.get_cost() + 5

    def get_ingredients(self):
        return self.pizza.get_ingredients() + ", Thick Pan"

```

As we can from the example, we are able to decorate a base pizza with multiple toppings and modifiers at runtime.


