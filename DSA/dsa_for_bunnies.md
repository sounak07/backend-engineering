## DSA for Bunnies by Team Sikhsa

### Prefix-Suffix Sum

[All Division Highest Score](https://leetcode.com/problems/all-divisions-with-the-highest-score-of-a-binary-array/description/)

### Two pointers

[Closest pair from two arrays](https://www.geeksforgeeks.org/problems/find-the-closest-pair-from-two-arrays4215/1)

### Sliding windows

[Maximum 1s](https://www.geeksforgeeks.org/problems/maximize-number-of-1s0905/1)

Template for Sliding window Problems

```python
left = 0
state = 0        # tracks "badness" (zeros, distinct chars, etc.)
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

### Greedy

[Max number of 1s II](https://www.geeksforgeeks.org/dsa/max-number-of-one-ii/)

### Arrays

[Min and 2min](https://www.geeksforgeeks.org/problems/find-the-smallest-and-second-smallest-element-in-an-array3226/1#using-single-pass)
