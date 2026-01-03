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