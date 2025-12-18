What happens when we do ?

```shell
python script.py
```

Lets dive deep into CPython. CPython is a Python interpreter written in C. There are others as well but CPython is the most maintained , original one.

Python doesn't have a formal specification like C, meaning there is no formal documentation defining the syntax , semantics, behaviour of the language like ANSI C standard or ISO C standard. 
There is Python Reference documentation but it does not constitute to formal specification. It can't also be defined as Python Reference implementation as well because there are other implementations of interpreters where the behaviour might differ from Cpython. 
So it can be called a combination of Cpython and Python Ref Documentation. 

#### The big picture 

Execution of Python code happens in 3 stages.
- Initialisation
- Interpretation
- Compilation 


In the ***Initialisation*** phase , Cpython Initialises the data structures required to execute the program, prepare built-in types, then configure and load them. Setup import systems etc.

During ***compilation*** Cpython creates AST(Abstract Syntax Tree) out of the source code , generates Bytecode from AST and performs some optimizations. Bytecode is a series of instructions represented in bytes, mostly 2 bytes, one for OPCODE and one for argument.

CPython is a VM that executes bytecodes and is stack based so if we see an example. 

```python
def add(x):
	return x+3
```

*See article to understand how this code is represented in bytecode*

If we do `python -m dis script.py`, we can see whats happening.

Here the  instructions would be 
- add x to the stack via `LOAD_FAST`. 
- Add 3 to the stack via `LOAD_CONST`
- Pop x and 3 from stack , add them and put back in stack the result with `BINARY_ADD`
- Pop the result with `RETURN_VALUE`

#### Code objects, function objects and frames

**code object**
When a block of code is executed as a single unit, say a function or a module, we call that a code block. The data structure that stores the instructions and information, list of local vars as per that code block is called a code object. So to run a code block we need to fetch and execute/evaluate a code object. 

**function object**
Function objects are a bit different then code objects. Function objects store function name, default arguments, doc strings, enclosed closed variables along with the code object reference in a function object. MAKE_FUNCTION flag is used to create it.
If we define multiple functions with similar implementations , code objects are shared.

```python
def add(a, b):
    return a + b

def subtract(x, y):
    return x - y

# Both add and subtract functions reference the same code object
print(add.__code__ is subtract.__code__)  # True
```

Here, the function references the same code object since the underlying code bytecode is same. 

```python
# make_add_x function
def make_add_x(x):
    def add_x(y):
        return x + y
    return add_x

# Create add_4 and add_5 function objects
add_4 = make_add_x(4)  # add_4 references code object 1
add_5 = make_add_x(5)  # add_5 references code object 2
```

Here the function `make_add_x` references different code object since the argument value is different if they were same code object could have been same.

#### frame object

Python needs a way to track where the code execution is, the changing values of variables, where the execution stopped to perform another module and where to return etc. This is what the frame object helps cpython with. It provides the state of the current execution of the code object. 
Whenever CPython needs to execute a code object, it creates a new frame. If another code object needs to be executed , it creates another frame with the reference of the previous frame. So it kind of creates a stack of frames which gets executed one after another. Also it provides a state in which order the code objects of different instructions should be executed. 

#### Threads, interpreters, runtime

A `thread state` is a data structure that stores thread specific data including call stack

Interpreter state is a group of threads and stores data specific to this group

Runtime is a global variable and stores data of the process including the GIL mechanism. 

After the creation of frames in Python, threads, the interpreter, and the runtime environment work together to execute the code represented by these frames. Threads enable concurrent execution, the interpreter interprets and executes bytecode instructions within frames, and the runtime environment provides the necessary infrastructure for code execution and resource management.

#### Conclusion 

The Cpython architecture has 
- Initialization of CPython
- Compilation and creation of code objects, function objects and frames
- Execution of Bytecode 

The CPython VM executes the bytecode. 