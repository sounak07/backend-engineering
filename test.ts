// Polymorphism - Poly means many and morph means forms -> many forms
//  Its a way of representing the object in a different form

class Person {
    name: string;
    constructor() {
        this.name = "";
    }
}

class Emp extends Person {
    id: string;
    constructor() {
        super()
        this.id = "";
    }
}

// const e : Emp = new Person() // wrong -> cannot use parent class to create a child class obj
const p : Person = new Emp() // right -> can use child class create parent class obj