## How CPython Compiler Works ?

##### What the CPython Compiler is ?

Compiler is basically a program that converts code from one language into a equivalent code of another language. Mostly from human readable code into machine code. 

![[Screenshot 2024-03-15 at 10.13.00 PM.png]]

The compiler architecture has 3 stage design as above. The frontend converts the code into a Intermediate Representation (IR) which gets passed to an optimizer which then passes the optimized IR to the backend to be converted into machine code.
The main advantage of this 3 stage design is if we choose a non language and non target machine specific IR , it can act as a plug play in which a frontend is need to convert code to IR and a backend to convert the IR to machine code. 

CPython does not need to support multiple languages just Python and CPython VM.

![[Screenshot 2024-03-15 at 10.55.21 PM.png]]

The above is the architecture of CPython compiler. Since 3.9 the need for parser to generate parse tree is also not there. Its directly generates the AST. 

##### Overview of Compiler's Architecture

The compiler of CPython consists of two parts - frontend and backend
The frontend parses the code and converts it into AST and the backend takes the AST and generates the code object.
While parsing if there are no syntax errors the parser organises the code as per some grammatical rules. 
The rules define how we can replace non-terminal symbols with terminal symbols. After that we will have a valid parser tree. 

##### Abstract Syntax tree

The ultimate goal of the parser is to produce the AST. The AST is basically a high level representation of what the code does hiding away all the syntaxes, punctuations etc
The AST is generated by ASDL, which is a declarative language to generate tree-like IRs.
The benefits of AST for compilers that it can easily generate the bytecodes from AST in a straightforward manner. Other tools like pytest uses AST to generate useful assertion messages on failure. Bandit uses AST to analyze for any vulnerabilities in code.
*See blog to see AST examples.*

Below we will see how parse generates AST from source code.
##### Old parser

Python's syntax is described using an EBNF notation, and it can be parsed using an LL(1) parser, which operates as a top-down Pushdown Automaton. Regular expressions are used to express syntax more naturally. The parsing process involves matching symbols on a stack with input symbols according to grammar rules.

A parse tree faithfully reflects the syntactic structure of the input as dictated by the grammar rules, an AST captures the essential meaning and structure of the input in a more abstract and language-independent form, suitable for further analysis or transformation.
The parse tree is converted to AST before giving it to compiler.

##### tokenizer

The Python grammar is complex. It looks simple because it gets represented in 200 lines thats because symbols are represented as tokens not as single characters. These tokens represent a group of characters making the whole set shorter. The tokens are represented by position in code and type as seen below.

![[Screenshot 2024-03-18 at 7.15.27 PM.png]]

The tokenizer play a crucial role in parsing the chars in token parser can understand. It relies on io module to identify the charset , if not provided with it defaults back to `utf-8` . It opens and reads its contents by calling the `readline()` function. This function returns a unicode string. The characters the tokenizer reads are just bytes in the UTF-8 representation of that string (or EOF). 
While defining numbers and names directly in the grammar is feasible but complex, expressing the significance of indentation without the tokenizer would require a context-sensitive grammar, making parsing more difficult. 
By treating numbers and names as tokens recognized by the tokenizer, we allow for more flexibility in how they are represented and interpreted. For example, numeric literals may include integers, floating-point numbers, scientific notation, hexadecimal notation, etc. Defining each possibility directly in the grammar could lead to a large number of rules and increased complexity.

A key feature of tokenizer is to maintain indentation via stacks. The current level is kept at the top , when level increases it gets pushed to the stack and when it decreases all higher levels get popped out.

*Refer above for example.*

##### New parser

PEG is Parsing Expression Grammar which is used in the New parser. PEG is different from the other grammar is that it maps nonterminals (like "noun" or "verb") with parsing expressions which could include sequences, choices etc instead of just sequence of symbols in the traditional grammar rules. 
In PEG parsers are based on recursive descent parsers. Each rule has its own parsing function. Whenever a text matches certain rule, it calls the function recursively in case of a nonterminal hit. 
The LL(k) parsers look ahead and predicts the type of rule for the next k steps. If it could not do that it uses backtracking on last attempts to predict that. It can be slow due to backtracking to memoization is used to fasten the process. Its called Packrat Parser. The new parser for CPython uses PEG and is based on Syntax-Directed Translation Scheme (SDTS).
SDTS enables the parser to build the AST in tandem with parsing the input text, leading to a more streamlined and efficient parsing process. 
##### AST to code object

We know CPython converts AST from source code but the CPython can only execute code object. The conversion of AST to code object is done by compiler. The Compiler also returns the code object of defined modules like functions and classes. 

While compiling , the compiler goes to the root node of AST and starts reading its statements. e.g. the first statement is `x = 1` , to convert the node in a code object, we store the const in the list of constants of the code object and emit `LOAD_CONST` and store the var x in a list of names of the code object and emit `STORE_NAME_INSTRUCTION` but the name could be a var inside a function, or a global var or a nested var, so it needs to be declared accordingly and emit instructions as per that. 
If `x` is a local variable, we should emit the `STORE_FAST` instruction. If `x` is a global variable, we should emit the `STORE_GLOBAL` instruction. Finally, if `x` is referenced by a nested function, we should emit the `STORE_DEREF` instruction. The problem to determine the variable type is solved by sample tables.

##### sample table



[Reference](https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/)

