#### Concurrency vs Parallelism

Machines run programs sequentially, but if we run a task while we wait for another to finish , we can achieve concurrency. **Concurrency** doesn't mean we need to run tasks at the same physical time, it means the ability to run in an interleaved manner, to suspend current task in the middle and start another one, hoping it would get more time later to execute. 
This way OS can execute thousands of tasks with limited cores and much faster.

For example - Suppose a cheese Grand master player playing with multi players at different tables where he is making moves on another player while he waits for the first player to make his move.

Tasks can also be run at the same physical time , in that case it would be called **parallelism** , a special form of concurrency.

![alt text](/resources/Screenshot%202024-02-09%20at%202.05.01 PM.png)

#### Sequential Server

```python
import socket


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = sock.accept()
        print('Connection from', addr)
        handle_client(client_sock)


def handle_client(sock):
    while True:
        received_data = sock.recv(4096)
        if not received_data:
            break
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    run_server()
```

#### OS threads for server serving concurrent Tasks

OS threads can be a easy way to implement concurrent tasks but spawning one thread for each task is not a scalable approach. So we need to a more efficient method where instead of creating one thread for each task we assign the tasks to a task queue and use a pool of threads called **thread pools** to assign the tasks to them from the queue based on availability.  

We can assign a number threads allowed to be used so that the server can't use too many of them. Below is the implementation in python using python standard ***concurrent.futures*** module.

```python
import socket
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(max_workers=20)


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = sock.accept()
        print('Connection from', addr)
        pool.submit(handle_client, client_sock)


def handle_client(sock):
    while True:
        received_data = sock.recv(4096)
        if not received_data:
            break
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    run_server()

```

Thread pool approach is quite simple but we still need to think about the long running clients. We either need to drop long running processes, have the clients maintain a certain throughput or return the task back to the queue. 

#### I/O Multiplexing and event loops

In a sequential server, when a client is connected it waits for the client to send data. But to work concurrently , it should accept connection while it waits for other connections to close.
How can we achieve that?
Most of the socket methods like` recv(), accept(), sendall()` are blocking. We can either try to add a timeout or introduce non-blocking into them as `sock.setblocking()`. But this might not be a great approach since server can end up handling too many requests which would consume a lot CPU. If timeouts are long it can end up being slow.

A better approach is to allow the OS to notify when the socket is available. OS has that info since when a packet comes it decodes it and assigns it to the socket it belongs and wakes up the process to do the blocking read on the socket since typically when a process wants to communicate via network it blocks and waits for data to arrive. 
But a process doesn't need to read from the socket to get notified, Instead of that process can register its interest of reading from multiple sockets using I/O multiplexing and its functions like  `select()`, `poll()`, or `epoll()`.
Whenever data arrives in any of the registered sockets , the OS wakes up the process and the process can do its due read or write. 

Python standard I/O Multiplexing functions are usually exposed via high level API called selector. Exposed methods are -
- `select()` as `SelectSelector`
- `epoll()` as `EpollSelector`
- most efficient mechanism available on the system as `DefaultSelector`.

So how do a process registers a socket

```python
sel = selectors.DefaultSelector()

# telling OS I want to read from this socket 
# params : socket, Types of Events interested , auxillary data
sel.register(sock, selectors.EVENT_READ, my_data)

# call the select() method
key_events = sel.select()
```

`key_events` stores a list of key and events (tuples).
- key stores socket (key.fileObj) and auxiliary data associated with socket (key.data)
- events socket bitmask of events ready in the socket (READ or WRITE or BOTH)

If there is a socket that is ready , calling `select()` returns immediately , if its blocked, it blocks itself until some socket is ready. The OS notifies the `select()` when a socket is available as it notifies functions like` recv()`. 
We can use `unregister()` to unregister a socket when no longer needed.

Now how we use a ready socket. We use a callback to register each socket, thats what the auxiliary data is for.

Below is the implementation of single concurrent server using I/O multiplexing. 

```python

import socket
import selectors

sel = selector.DefaultSelector()

def setup_listening_socket(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    sel.register(sock, selectors.EVENT_READ, accept)


def accept(sock):
	# new client socket created
    client_sock, addr = sock.accept()
    print('Connection from', addr)
    sel.register(client_sock, selectors.EVENT_READ, recv_and_send)


def recv_and_send(sock):
    received_data = sock.recv(4096)
    if received_data:
        # assume sendall won't block
        sock.sendall(received_data)
    else:
        print('Client disconnected:', sock.getpeername())
        sel.unregister(sock)
        sock.close()


def run_event_loop():
    while True:
	    # select() here will keep selecting empty sockets
        for key, _ in sel.select():
            callback = key.data
            sock = key.fileobj
            callback(sock)


if __name__ == '__main__':
    setup_listening_socket()
    run_event_loop()
	
```

When a client connects to a server, the server socket (`sock` in this case) accepts the connection, creating a new socket (commonly referred to as the client socket) through which the server can communicate with the client. This new socket (`client_sock` in the code) represents the communication channel specific to that particular client.

The above code is a very simple implementation of event loop in a single thread. But there are some flaws to it. 
The socket needs to check if its ready to write before doing `sendall()` so there needs to be another registered socket at some appropriate part of server and needs to checked first before right. 

But how do threads do it without callback style functionality ?
They use functions which can be called and stopped in the middle and called again. 
We can write such functions in python. 

#### Generator Functions and generators in Python

A **generator function** is a function that has one or more [`yield`](https://docs.python.org/3/reference/expressions.html#yield-expressions) expressions in its body, like this one:

```python
def gen():
	yield 1
	yield 2
	return 3

```

Generator functions cannot be invoked just by calling them, they are called using built-in `next()`.
Whenever a generator is called using `next()` , it runs the function to first yield expression, after that it stops the execution at this point and it returns the arguments of the first yield.
If the `gen()` is called again it resumes its execution from the point it stopped and runs the function to the next yield expression and returns its arguments. 

```python

next(gen)
>> 1

next(gen)
>> 2

next(gen)
>> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: 3
```

We are going to use these generator functions for its ability to stop and start its execution.

#### Generators as Coroutines

```python
import socket
from event_loop_01_no_io import EventLoopNoIO
from collections import deque


class EventLoopNoIO:
    def __init__(self):
        self.tasks_to_run = deque([])

    def create_task(self, coro):
        self.tasks_to_run.append(coro)

    def run(self):
        while self.tasks_to_run:
            task = self.tasks_to_run.popleft()
            try:
                next(task)
            except StopIteration:
                continue
            self.create_task(task)


loop = EventLoopNoIO()


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        yield
        client_sock, addr = sock.accept()
        print('Connection from', addr)
        loop.create_task(handle_client(client_sock))


def handle_client(sock):
    while True:
        yield
        received_data = sock.recv(4096)
        if not received_data:
            break
        yield
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    loop.create_task(run_server())
    loop.run()


```

So there are some flaws here, suppose the first task is to accept new connections, all tasks will be stuck until it connects to a client.
	So to improve this Event loop can actually assign tasks when a socket is ready using I/O multiplexing. Instead of rescheduling a task just after running the task, the Event loop only reschedules when a socket that the task is waiting on to read is ready to read or write. 
A task can register its interest by calling functions of event loop or can yield this info to event loop.

```python

import socket
import selectors

from event_loop_01_no_io import EventLoopNoIO
from collections import deque


class EventLoopNoIO:
    def __init__(self):
        self.tasks_to_run = deque([])
        self.sel = selectors.DefaultSelector()

    def create_task(self, coro):
        self.tasks_to_run.append(coro)

    def run(self):
        while True:
            task = self.tasks_to_run.popleft()
	        if self.tasks_to_run:
			    try:
	                op,arg  = next(task)
	            except StopIteration:
	                continue
		        if op == 'WAIT_READ':
			        self.sel.register(arg, selectors.EVENT_READ, task)
			    elif op == 'WAIT_WRITE':
				    self.sel.register(arg, selectors.EVENT_READ, task)
				else:
					raise ValueError("")
			else:
				for key, event in self.sel.select():
					task = key.data
					sock = key.fileObj
					self.sel.unregister()
					self.create_task(task)

loop = EventLoopNoIO()


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        yield 'WAIT_READ', sock
        client_sock, addr = sock.accept()
        print('Connection from', addr)
        loop.create_task(handle_client(client_sock))


def handle_client(sock):
    while True:
        yield 'WAIT_READ', sock 
        received_data = sock.recv(4096)
        if not received_data:
            break
        yield 'WAIT_WRITE', sock
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    loop.create_task(run_server())
    loop.run()

```

When generators are doing multiple tasks we can call them coroutines. So coroutines are functions that can run in an interleaved manners by suspending the execution by yielding the control. 
So generators with multiple yields can be a coroutines.
A true coroutine however should be able to handle control to other functions as well but its not the case. That can be however done by sub-generators. 

```python
def async_rev(sock):
	yield 'WAIT_READ', sock 
    received_data = sock.recv(4096)

received_data = yield from async_recv(sock)
```

Generators also have got the `send()` which works same as `_next()_` but you can also send a value. The value becomes the value of the `yield` expression that the generator is suspended on.

```python

def consumer():
	val = yield 1
	print('Got', val)
	val = yield
	print('Got', val)

c = consumer()
next(c) # 1

c.send(2) #Got 2
c.send(3) #Got 3

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```
#### yield from

`yield from` makes a subgenerator code work as if its a part of the generator function. 
So we can break up a generator into sub generators making it behave like a true coroutine. 

When we use `yield from` within a generator, it effectively passes control to another generator, allowing it to yield values directly to the caller of the main generator. This mechanism enables you to create composite generators, where one generator delegates part of its work to one or more sub-generators.

Main generator can send value to sub generator using `send()` as we mentioned above.
Any Exception raised will propagate back to main generator.
`StopIteration` is called to exit the sub generator returning the value back to main generator.

```python
from event_loop_01_no_io import EventLoopNoIO
from collections import deque


class EventLoopNoIO:
    def __init__(self):
        self.tasks_to_run = deque([])
        self.sel = selectors.DefaultSelector()

    def create_task(self, coro):
        self.tasks_to_run.append(coro)

	def sock_sendall(self, sock, received_data):
		yield 'WAIT_WRITE', sock
        sock.sendall(received_data)

	def sock_accept(self, sock):
		yield 'WAIT_READ', sock
        client_sock, addr = sock.accept()

	def sock_recv(self, sock, byts):
		yield 'WAIT_READ', sock 
        received_data = sock.recv(byts)

    def run(self):
        while True:
            task = self.tasks_to_run.popleft()
	        if self.tasks_to_run:
			    try:
	                op,arg  = next(task)
	            except StopIteration:
	                continue
		        if op == 'WAIT_READ':
			        self.sel.register(arg, selectors.EVENT_READ, task)
			    elif op == 'WAIT_WRITE':
				    self.sel.register(arg, selectors.EVENT_READ, task)
				else:
					raise ValueError("")
			else:
				for key, event in self.sel.select():
					task = key.data
					sock = key.fileObj
					self.sel.unregister()
					self.create_task(task)

loop = EventLoopNoIO()


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = yield from loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(handle_client(client_sock))


def handle_client(sock):
    while True:
        received_data = yield from loop.sock_recv(sock ,4096)
        if not received_data:
            break
        yield from loop.sock_sendall(sock, received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    loop.create_task(run_server())
    loop.run()

```


#### async/await

How do we know if a generator function is a regular generator or a coroutine ?
Native coroutines are declared with async keyword 

```python
async def coroutine():
	return 1
```

When such a function is called we return a native coroutine not a regular generator function. It is exactly like a regular generator, the difference is it doesn't implement `next()` and Event loop calls a native coroutine with send(None).

```python
coroutine.send(None)

StopIteration
```

Native coroutines call each other with `await` keyword 

```python
async def coroutine():
	return 1

async def routine2():
	res = await coroutine()
	return res

>> routine2.send(None)
StopIteration
1
```

`await` keyword does exactly what `yield from` does, its just implemented with a certain checks to ensure that the awaitable function is not a generator or other iterator.
When using generators we must end the chain of `yield from/awaits` same as we need to end the generators with `yield` expression.

Suppose there is a async def function with yield expression
```python

async def coroutine():
	yield 1

```
 Such a function will not return a native coroutine but a async generator, these generators are not awaitable. So how do we end the chain of `yield from` in this case.

We have two options:

1. To decorate a regular generator.
```python
import types

@types.coroutine
def A():
	yield 1


async def coroutine():
	res = await A()
	return res

coroutine.send(None)
```

`@types.coroutine`  makes a generator function behave like a native coroutine. These functions are called generator-based coroutines. We need these coroutines to avoid the ambiguity on generators and coroutines

2. To make an object awaitable with  `__await()_`
```python
class A:
	def _await_(self):
		yield 1

async def coroutine():
	res = await A()
	return res

coroutine.send(None)
```

When we await it checks whether the function is a coroutine or a generator-based coroutine. Based on that it `yield from` a coroutine or a awaitable generator. 

```python
import types
from event_loop_01_no_io import EventLoopNoIO
from collections import deque


class EventLoopNoIO:
    def __init__(self):
        self.tasks_to_run = deque([])
        self.sel = selectors.DefaultSelector()
	
    def create_task(self, coro):
        self.tasks_to_run.append(coro)

	@types.coroutine
	def sock_sendall(self, sock, received_data):
		yield 'WAIT_WRITE', sock
        sock.sendall(received_data)

	@types.coroutine
	def sock_accept(self, sock):
		yield 'WAIT_READ', sock
        client_sock, addr = sock.accept()

	@types.coroutine
	def sock_recv(self, sock, byts):
		yield 'WAIT_READ', sock 
        received_data = sock.recv(byts)

    def run(self):
        while True:
            task = self.tasks_to_run.popleft()
	        if self.tasks_to_run:
			    try:
	                op,arg  = next(task)
	            except StopIteration:
	                continue
		        if op == 'WAIT_READ':
			        self.sel.register(arg, selectors.EVENT_READ, task)
			    elif op == 'WAIT_WRITE':
				    self.sel.register(arg, selectors.EVENT_READ, task)
				else:
					raise ValueError("")
			else:
				for key, event in self.sel.select():
					task = key.data
					sock = key.fileObj
					self.sel.unregister()
					self.create_task(task)

loop = EventLoopNoIO()


async def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(handle_client(client_sock))


async def handle_client(sock):
    while True:
        received_data = await loop.sock_recv(sock ,4096)
        if not received_data:
            break
        await loop.sock_sendall(sock, received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


if __name__ == '__main__':
    loop.create_task(run_server())
    loop.run()

```

Here all the functions with yields are changed to generator based with `@types.coroutine` and wherever we are awaiting , changed the function to async.

#### How generators and coroutines are implemented ?

In python the compiler creates a code object which can be a module, a function or a class. The code object describes the code about what needs to be done, stores the variables, bytecodes, constants. 

A generator function is an ordinary function with `CO_GENERATOR` flag and a native coroutine is a function with `CO_COROUTINE`. So whenever these flags are detected python returns a generator object instead of executing the function, and incase of coroutine, python returns a native coroutine if the later flag is found.

In python , for a function a frame is created which stores the code object , the local variables , the global references etc. It also tracks the state of execution of the function.
In case of generator , a frame is created which stores the name of generator , whether the generator is running or not. When the `send()` is called the frame is executed. 
The only difference is case of function python creates a new frame every time while in case of generator same frame is re-used while keeping track of the state.

#### asyncio

Asyncio schedules coroutines and invokes callbacks.It provides `loop.create_task()` to schedule and run coroutines. 

It has 3 types of registered callbacks.
- The ready callbacks. They are stored in `loop._ready()` queue and can be scheduled by calling `loop.call_soon()` and `loop.call_soon_threadsafe()`.
- The callbacks that becomes ready a future time. `loop.call_later` and `loop.at()` can be used to schedule them.
- The callbacks that gets scheduled on file descriptor becomes ready to read or write.

`handle.cancel()` can be used to cancel a scheduled callback. Its a wrapper on the callback methods.
The `loop.run_once()` method runs once to perform certain tasks. 
*Refer article for more info*.

How does the `loop.create_task()` work ?

To schedule a coroutine its wrapped in a task instance, the `task._init()_` schedules `task.__step()` as a callback by calling `loop.call_soon()` . Then `task._step()` runs the coroutine. 

`task.__step()` runs the coroutine by calling `coro.send(None)`  and it either returns None or a future.

A future is a instance that represents a operation that isn't yet completed and may be take some time to complete. The event loop is basically waiting for its value.
None represents that its yielding its control , and the `task.__step()` reschedules itself.

For a future `task.__step()` calls `future.add_done_callback()` to add to the future a callback that schedules `task.__step()` again. If the result is available `future.add_done_callback()` callback is invoked immediately otherwise its invoked when someone calls `future.set_result()` 

So when a task awaits for its future , it yields `task.__step()` which will reschedule itself and wait until some calls `future.set_result()`  and t`task.__step()` calls `future.add_done_callback()` to return the value. 

*Refer to article for an example* 

[Reference](https://tenthousandmeters.com/blog/python-behind-the-scenes-12-how-asyncawait-works-in-python/)