## Behavioural Patterns

### Strategy Pattern

The Strategy Pattern is a behavioral design pattern that allows an application to select and switch between different algorithms at runtime without changing the code that uses them.

It is particularly useful when a system needs to execute different business logic based on runtime conditions, such as user input, configuration, or environment.

For example, in a payment system, the user may choose between Credit Card, UPI, or Net Banking. Each payment method has its own processing logic, but the client interacts with a common interface. The strategy pattern enables the system to dynamically select the appropriate payment algorithm at runtime while keeping the client code clean and decoupled.

It’s important to note that design patterns are not strict rules. They serve as guidelines and proven solutions to recurring problems. The goal is not to force patterns everywhere, but to apply them when they simplify code, improve maintainability, and reduce coupling.

```python

class PaymentStrategy:
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using Credit Card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using PayPal")

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item['price'] for item in self.items)

    def pay(self, payment_strategy: PaymentStrategy):
        total = self.calculate_total()
        payment_strategy.pay(total)

# Usage
cart = ShoppingCart()
cart.add_item({'name': 'Item 1', 'price': 100})
cart.add_item({'name': 'Item 2', 'price': 200})

# Payment using Credit Card

if user_input == "credit_card":
    credit_card = CreditCardPayment()
    cart.pay(credit_card)
elif user_input == "paypal":
    paypal = PayPalPayment()
cart.pay(paypal)
```

### Observer Pattern

A type of pattern that create a one-to-many relationship between its observers and subjects such that any changes in state of the subject gets notified to its observers.

This creates a loose coupling between the subject and observers without having the observers to poll the observee for updates, kinda reverse of what happens in Pub/Sub architecture.

```python

class Observer:
    def update(self, message):
        pass

class Observable:
    def add(self, observer):
        pass

    def remove(self, observer):
        pass

    def notify(self, message):
        pass


class Phone(Observer):
    def update(self, message):
        print(f"Phone: {message}")

class Email(Observer):
    def update(self, message):
        print(f"Email: {message}")

class SMS(Observer):
    def update(self, message):
        print(f"SMS: {message}")


class ProductInventory(Observable):
    def __init__(self):
        self.observers = []
        self.product_count = 0

    def set_product_count(self, count):
        self.product_count = count
        if self.product_count > 0:
            self.notify("Product is available")

    def get_product_count(self):
        return self.product_count

    def add(self, observer):
        self.observers.append(observer)

    def remove(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


pp = Phone()
em = Email()
sms = SMS()

inventory = ProductInventory()
inventory.add(pp)
inventory.add(em)
inventory.add(sms)

inventory.set_product_count(1)
inventory.set_product_count(0)

```

### State machine

State machine is used when an object's behaviour is driven by its internal state. This pattern handles state transitions in a very explicit and clean manner.

```python

from abc import ABC, abstractmethod

class VendingMachineState(ABC):
    @abstractmethod
    def insert_coin(self, machine):
        pass

    @abstractmethod
    def select_product(self, machine):
        pass

    @abstractmethod
    def dispence_product(self, machine):
        pass


class NoCoinState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine'):
        print("Coin inserted")
        machine.state.select_product(HasCoinState())

    def select_product(self, machine: 'VendingMachine'):
        print("Please insert a coin")

    def dispence_product(self, machine: 'VendingMachine'):
        print("Please insert a coin")


class HasCoinState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine'):
        print("Coin inserted, select product")

    def select_product(self, machine: 'VendingMachine'):
        return machine.dispense_product(DispenseProductState())

    def dispence_product(self, machine: 'VendingMachine'):
        print("Coin inserted, select product")


class DispenseProductState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine'):
        print("Product dispensing, please wait")

    def select_product(self, machine: 'VendingMachine'):
        print("product selected")

    def dispence_product(self, machine: 'VendingMachine'):
        print("product delivered")
        machine.set_state*(NoCoinState())


class VendingMachine:
    def __init__(self):
        self.state = NoCoinState()

    def insert_coin(self):
        return self.state.insert_coin(self)

    def select_product(self):
        return self.state.select_product(self)

    def dispense_product(self):
        return self.state.dispence_product(self)

    def set_state(self, state: VendingMachineState):
        self.state = state

machine = VendingMachine()

machine.select_product()
machine.insert_coin()
machine.select_product()
machine.dispense_product()


```

## Structural Patterns

### Facade Pattern

A facade is just a coordinator class which hides all the complex implementations behind it. You probably use it most of time whithout actually naming it. Any orchestrator that hides multiple components behind an interface can be called a facade

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

## Creational Patterns

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

### Build Pattern

A builder is a helper that lets you create a complex object step by step without worrying about the order or messy construction details. It's used when an object has many optional parts or configuration choices.

```python

from typing import Optional

# NOTE: Builder is less common in Python. Python has better alternatives like
# dataclasses with default values, keyword arguments, or simple dictionaries.
# This pattern adds unnecessary complexity for most Python use cases.

class HttpRequest:
    def __init__(self):
        self.url: Optional[str] = None
        self.method: Optional[str] = None
        self.headers: dict[str, str] = {}
        self.body: Optional[str] = None

    class Builder:
        def __init__(self):
            self._request = HttpRequest()

        def url(self, url: str) -> 'HttpRequest.Builder':
            self._request.url = url
            return self

        def method(self, method: str) -> 'HttpRequest.Builder':
            self._request.method = method
            return self

        def header(self, key: str, value: str) -> 'HttpRequest.Builder':
            self._request.headers[key] = value
            return self

        def body(self, body: str) -> 'HttpRequest.Builder':
            self._request.body = body
            return self

        def build(self) -> 'HttpRequest':
            # Validate required fields
            if self._request.url is None:
                raise ValueError("URL is required")
            return self._request

# Usage
request = (HttpRequest.Builder()
    .url("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .body('{"key": "value"}')
    .build())


```

### Singleton Pattern

Singleton Pattern ensures that an instance is created only once; the instance then can be used as a shared resource like config manager, db connections etc.

```python

class StorageConnection:
    def __init__(self, info):
        self.info = info
        self.conn = None

    def _get_conn(self):
        if not self.conn:
            self.conn = Conn(self.info)
        return self.conn

```

`_get_conn` is what makes the Singleton.
