## Strategy Pattern

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
