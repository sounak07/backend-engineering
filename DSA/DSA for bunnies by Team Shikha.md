[DSA Sheet](https://docs.google.com/spreadsheets/d/1BPhFrtg12IjpmLc78feoffDbD-dgAwYlQ1YM9gdVBIY/edit?usp=sharing)
### Two pointers

- Always Skip Duplicates before inserting.

```python

# Pattern for duplicate counting

  

val1 = arr1[i]

val2 = arr2[j]

  

c1 = 0

while i < l1 and arr1[i] == val1:

c1 += 1

i += 1

c2 = 0

while j >= 0 and arr2[j] == val2:

c2 += 1

j -= 1

  

# Cartesian product of duplicates

for _ in range(c1 * c2):

res.append([val1, val2])

```


  

### Boyer-Moore Algo
Note: Everything depends on how many majority elements can there be.


### Sliding windows
  

```python
# Important formula

AT_MOST(K) = EXACT(1) + EXACT(2) + ... + EXACT(K)

Exactly(K) = Atmost(k) - Atmost(k-1)

```

  
```python

# Template for Sliding window Problems

left = 0

state = 0 # tracks "badness" (zeros, distinct chars, etc.)

answer = 0

for right in range(len(arr)):

# 1️⃣ Expand window

if is_bad(arr[right]):

state += 1

# 2️⃣ Shrink window until valid

while state > K:

if is_bad(arr[left]):

state -= 1

left += 1

# 3️⃣ Window is valid → update answer

answer = max(answer, right - left + 1)

  

```

### Recursion/Backtracking

***Backtracking tip*** - Always check solution condition first and then termination condition