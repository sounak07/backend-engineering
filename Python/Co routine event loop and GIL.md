### Offloading blocking code to a thread (asyncio + GIL)


**A coroutine**

A coroutine is a function defined with async def. Calling it doesn't run it but returns a **coroutine object**, a _pausable_ computation. It runs only when something drives it, and crucially it can **suspend itself** at every await and hand control back, then resume later from exactly that point.

  

```python
async def handler(event):
x = await fetch_from_db(event.id) _# ← can pause HERE, give the loop control_

y = await call_gcp(x) _# ← can pause HERE too_

return y
```


At each await, the coroutine says "I'm waiting on I/O, wake me when it's ready" and yields. While it's paused, the program is free to do other things.

  
**The event loop**


The event loop is a single-threaded scheduler that runs in **one OS thread**. It keeps a queue of coroutines that are ready to make progress and runs them **one at a time**:

1. Pick a ready coroutine, run it until it hits an await that isn't ready.

2. The coroutine suspends; the loop parks it against whatever it's waiting on (a socket, a timer, a DB response).

3. The loop picks the next ready coroutine and runs _it_.

4. When a parked coroutine's I/O completes, the loop marks it ready and resumes it later from where it paused.

So it's not parallel execution — it's **rapid interleaving**. Only one coroutine's code runs at any instant, but many can be _in flight_ (paused, waiting on I/O) simultaneously. This is "concurrency without parallelism."

  **The analogy**


A chef (one thread = one person) cooking many dishes. They put a pot on to boil (await), and instead of standing there staring at it, they start chopping vegetables for another dish. When the pot boils, they come back to it. One cook, many dishes progressing — by never standing idle during a wait.


#### The problem
- One event loop runs on **one thread**. Coroutines are cooperative: they only hand back control at `await`.
- A **blocking** call (sync I/O, e.g. `blob.download_to_filename(...)`) has no `await` inside it.
- Call it directly in an `async def` → the loop thread is stuck inside it → **nothing else on the loop runs** until it finishes. The whole app stalls.
#### The fix

  

```python

path = await asyncio.to_thread(_blocking_fn) # runs _blocking_fn on a worker thread

```

  

- `to_thread` schedules the sync function on asyncio's default `ThreadPoolExecutor` and returns an awaitable.
- The `await` **suspends this coroutine and yields to the loop** → loop is free to run other tasks while the blocking work happens on another OS thread.
- When the thread finishes, the coroutine is **resumed on the loop thread** with the return value (or the exception re-raised at the `await`).

#### Why the GIL doesn't ruin this

- GIL = only one thread runs **Python bytecode** at a time.
- But blocking **I/O** (sockets, disk, C libs) **releases the GIL** while it waits.
- So while the worker thread is parked in the OS-level read/write, the loop thread can grab the GIL and run.
- Net: real overlap for **I/O-bound** work.

#### Key caveat

- This trick only helps **I/O-bound** blocking. For **CPU-bound** Python work the GIL is NOT released → threads don't overlap → use a **process pool** (`ProcessPoolExecutor` / `run_in_executor` with processes) instead.
#### Other things to remember

- Exceptions cross the thread boundary: they re-raise at the `await`, so normal `try/except` around the `await` works.

- Bundle ALL the sync work (client setup, the call, cleanup) into the function you offload — keep the loop side clean.

- Default thread pool is bounded (~`min(32, cpu+4)`). Many concurrent offloads queue on those threads.

#### One-liner to remember


> Blocking I/O in async = loop killer. `await asyncio.to_thread(...)` moves it off the loop thread; the GIL is released during I/O so it actually overlaps. (I/O only — not CPU.)

  

---

###  Generators & streaming large files


**What a generator is**


A function that contains `yield` is a generator. Calling it does **not** run the body — it returns a **generator object**. The body runs only when you iterate it (`for`, `next()`, `list()`), and each `yield`:

1. produces a value to the caller, and

2. **pauses** the function, keeping all its local variables alive.

The next iteration **resumes right after the `yield`**. (Same pause/resume idea as a coroutine, but driven by iteration instead of `await`.)


```python

def batches(rows, n):

batch = []

for row in rows:

batch.append(row)

if len(batch) >= n:

yield batch # ← hand one batch back, then pause here

batch = []

if batch:

yield batch # leftover partial batch
```

  
**Why this is the key to parsing large files**

- **Lazy = bounded memory.** A generator computes one item at a time, on demand. You never build the whole result in memory. Parsing a huge file into a `list` = O(file) memory (OOM risk); a generator yielding row-batches = ~O(one batch).

- **Pull-based pipeline.** The consumer pulls the next chunk only when ready, so producer and consumer stay in lockstep. Read a batch → process/insert it → drop it → read the next. Peak memory ≈ one batch, regardless of file size.

- **Composable with other lazy iterators.** e.g. `openpyxl.load_workbook(path, read_only=True)` + `sheet.iter_rows()` stream rows off disk one at a time; wrapping them in a batching generator keeps the whole chain lazy end-to-end.

  
**Cleanup: `try/finally` in a generator**

Put resource cleanup (closing the workbook/file) in a `finally`. It runs when the generator is **exhausted** OR **closed early** (consumer `break`s, calls `.close()`, or it's GC'd — this fires `GeneratorExit` at the paused `yield`, unwinding the `finally`). So the file handle is never leaked even if the consumer stops midway.

  

```python

def iter_batches(path, n):

wb = openpyxl.load_workbook(path, read_only=True, data_only=True)

try:

	rows = wb.worksheets[0].iter_rows(values_only=True)

	...

	yield batch

finally:

	wb.close() # runs on exhaustion, break, .close(), or GC

```


**Gotchas to remember**

- **Single-use.** Once consumed, a generator is exhausted — you can't rewind it. Need a second pass? Call the generator function again to get a **fresh** generator (it re-reads the source). Requires the source to be stable/seekable (e.g. a temp file on disk, not a one-shot stream).

- Nothing runs until you iterate — so exceptions in the body surface **during** iteration, not at call time.

- Great for I/O-bound streaming; doesn't add parallelism (it's still one thread pulling items).

  

#### One-liner to remember

  

> A generator is a pausable, pull-based stream: it yields one chunk at a time and forgets the rest, so you can parse an arbitrarily large file in ~one-chunk memory. Put cleanup in `finally`; it's single-use, so re-call the function for a second pass.