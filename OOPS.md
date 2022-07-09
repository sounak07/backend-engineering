# OOPS

## Pillers of OOPS

### Inheritance

- Deriving the properties of a parent class to extend to a new class.

### Polymorphism 
- Poly means many and morph means forms -> many forms
- Its a way of representing the object in a different form

```ts

class Person {
    name: string;
    constructor(name) {
        this.name = name;
    }

    show():void{
        console.log(this.name)
    }
}

class Emp extends Person {
    id: string;
    constructor(name, id) {
        super(name)
        this.id = id;
    }

    // child class overriding the parent class method
    show(): void {
        super.show(); // do everything you do in parent show and then do additional stuff
        console.log(this.name + this.id)
    }
}

// const e : Emp = new Person() // wrong -> cannot use parent class to create a child class obj
const p : Person = new Emp('Sounak', 1) // right -> can use child class create parent class obj


```

### Encapsulation 
- Binding data members and its operating functions together in a single entity/class.It is the mechanism that binds together code and the data it manipulates. 
- Another way to think about encapsulation is, that it is a protective shield that prevents the data from being accessed by the code outside this shield


## ABSTRACT CLASS VS INTERFACES

- When you leave 1 or 2 methods to derived class while providing default implementation for most of the other methods, use abstract class.
- When you want a class to implement a "contract", use interfaces.
- When you want a class with existing base class to have additional functionality (without having to implement all methods of an interface), use a mixin (or interfaces with default methods in C#, Java etc)