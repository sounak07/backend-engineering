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
