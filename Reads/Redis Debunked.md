### Why is Redis so fast ?

- Its a in-memory database.
	- So better read and write speeds. 
	- Low latency. 
	- Much easier to implement
	- Drawback is that its limited to memory 

 - It uses IO Multiplexing and Single Threaded read/write, quite similar to how **nodejs** does I/O. 
	 - Drawback is its not leveraging multi cores of a CPU
 
 - Efficient Data structures 
	 - Being an in-memory db it can leverage low level data structures without worrying about how to persist them in disk efficiently like Linked list, Hash Tables etc