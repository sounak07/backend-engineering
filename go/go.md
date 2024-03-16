### Go Debunked

Go is a compiled time language but with auto memory management. So it kinda sits in the middle of Purely compiled languages like C, Rust etc and Interpreted Languages like Python , Javascript. 

In Interpreted languages like Python , code is read and compiled at runtime while in Go code is compiled into a executable binary first and then that executable is run to execute the program. 

One of the major advantages of Go being compiled time is its ability to run on any machine without the runtime dependencies since idea we are just running a executable binary.

```go
package main

// package to use print function
import "fmt"

func main() {
	// single-line comments start with "//"
	// comments are just for documentation - they don't execute
	fmt.Println("starting Textio server")
}

```

1. `package main` lets the Go compiler know that we want this code to compile and run as a standalone program, as opposed to being a library that's imported by other programs.
2. `import fmt` imports the `fmt` (formatting) package. The formatting package exists in Go's standard library and lets us do things like print text to the console.
3. `func main()` defines the `main` function. `main` is the name of the function that acts as the entry point for a Go program.

One of the major things about Go is that its strongly typed. 

```go
package main

import "fmt"

func main() {
	var username string = "wagslane"
	var password string = "20947382822"

	// don't edit below this line
	fmt.Println("Authorization: Basic", username+":"+password)
}

```

Go programs are easy on memory as compared to Java since java requires a lot of memory to spin up JVM to compile the code.

In case of Go the memory management is automated like java but its usually managed by a small amount of "extra" code that's included in the executable binary. This extra code is called the [Go Runtime](https://go.dev/doc/faq#runtime). One of the purposes of the Go runtime is to cleanup unused memory at runtime.

### Types in Go

```go
bool

string

// intX/uintX , X here represents the number of bits we can store
// so int16 can store upto biggest number which is of 16 bits

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

// alias for uint8 
// Size of 1 byte is 8 bits so uint8
byte 

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128
```


#### Short Assignment Operator

```go
:=
```

```go
var name string = "Sounak"

name := "Sounak"
```

#### Type Casting in Go

```go
accountAge := 2.6
accountAgeInt := int(accountAge)
```

#### IF ELSE in Go

```go
if INITIAL_STATEMENT; CONDITION {
}
```

```go
if length := getLength(email); length < 1 {
    fmt.Println("Email is invalid")
}
```

Not only is this code a bit shorter, but it also removes `length` from the parent scope, which is convenient because we don't need it there - we only need access to it while checking a condition.


### Functions In Go

```go
func sub(x int, y int) int {
  return x-y
}
```

Accepts two integer parameters and returns another integer.

Here, `func sub(x int, y int) int` is known as the "function signature".

#### Declaration Syntax 

Go's declarations are clear, you just read them left to right, just like you would in English.

```go
x int
p *int
a [3]int
```

#### Ignoring return values

```go
func getPoint() (x int, y int) {
  return 3, 4
}

// ignore y value
x, _ := getPoint()
```

#### Named Return values

```go
func getCoords() (x, y int){
  // x and y are initialized with zero values

  return // automatically returns x and y
}
```

```
A return statement without arguments returns the named return values. This is known as a "naked" return. Naked return statements should be used only in short functions. They can harm readability in longer functions.
```

### Structs in Go

A collection type. A type that contains other types. 

```go
type car struct {
  Make string
  Model string
  Height int
  Width int
  FrontWheel Wheel
  BackWheel Wheel
}

type Wheel struct {
  Radius int
  Material string
}
```

#### Anonymous Structs

```go
myCar := struct {
  Make string
  Model string
} {
  Make: "tesla",
  Model: "model 3"
}
```


```go
type car struct {
  Make string
  Model string
  Height int
  Width int
  // Wheel is a field containing an anonymous struct
  Wheel struct {
    Radius int
    Material string
  }
}
```

***Note: Use name structs unless there is a very particular case.*** 

#### Nested Structs 

```go
type car struct {
  Make string
  Model string
  Height int
  Width int
  FrontWheel Wheel
  BackWheel Wheel
}

type Wheel struct {
  Radius int
  Material string
}
```

```go
myCar := car{}
myCar.FrontWheel.Radius = 5
```

#### Embedded Structs

```go
type car struct {
  make string
  model string
}

type truck struct {
  // "car" is embedded, so the definition of a
  // "truck" now also additionally contains all
  // of the fields of the car struct
  car
  bedSize int
}
```

- Access a property of car , we can just truck.model and not truck.car.model since its embedded and not nested.
- Since Go is not Object oriented embedding kinda works like inheriting the parent class in a child class.  
- An embedded struct's fields are accessed at the top level, unlike nested structs.
- Promoted fields can be accessed like normal fields except that they can't be used in [composite literals](https://golang.org/ref/spec#Composite_literals)

```go
lanesTruck := truck{
  bedSize: 10,
  car: car{
    make: "toyota",
    model: "camry",
  },
}

fmt.Println(lanesTruck.bedSize)

// embedded fields promoted to the top-level
// instead of lanesTruck.car.make
fmt.Println(lanesTruck.make)
fmt.Println(lanesTruck.model)
```

#### Nested vs Embedded 

- In we are specifying the type with a name but in embedded we are directly putting the struct as a member and not just the type. ***(Refer above sections for examples)***

#### Struct methods in Go

```go
type rect struct {
  width int
  height int
}

// area has a receiver of (r rect)
func (r rect) area() int {
  return r.width * r.height
}

// initialize struct
r := rect{
  width: 5,
  height: 10,
}

fmt.Println(r.area())
// prints 50
```


### Interfaces





