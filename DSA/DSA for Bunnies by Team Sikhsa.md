
### Prefix-Suffix Sum
[All Division Highest Score](https://leetcode.com/problems/all-divisions-with-the-highest-score-of-a-binary-array/description/)
### Two pointers

[Closest pair from two arrays](https://www.geeksforgeeks.org/problems/find-the-closest-pair-from-two-arrays4215/1)
[Pair Sum closest to 0](https://www.geeksforgeeks.org/problems/two-numbers-with-sum-closest-to-zero1737/1)
[Find all pairs in a given sum](https://www.geeksforgeeks.org/problems/find-all-pairs-whose-sum-is-x5808/1)
[Count Pairs sum less than target](https://www.geeksforgeeks.org/problems/count-pairs-whose-sum-is-less-than-target/1)
[Union of arrays](https://www.geeksforgeeks.org/problems/union-of-two-sorted-arrays-1587115621/1)
[Merge two sorted arrays](https://leetcode.com/problems/merge-sorted-array/)
[Remove Duplicates from sorted list II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)
[Remove Element](https://leetcode.com/problems/remove-element/submissions/1888883252/)

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

### 3 Pointers

[3 Sum](https://leetcode.com/problems/3sum/description/)
[Sort Colors](https://leetcode.com/problems/sort-colors/description/)

### Sliding windows
[Maximum 1s](https://www.geeksforgeeks.org/problems/maximize-number-of-1s0905/1)
[Count Pairs less than target](https://www.geeksforgeeks.org/problems/count-pairs-whose-sum-is-less-than-target/1)

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

### Greedy
[Max number of 1s II](https://www.geeksforgeeks.org/dsa/max-number-of-one-ii/)

### Arrays
[Min and 2min](https://www.geeksforgeeks.org/problems/find-the-smallest-and-second-smallest-element-in-an-array3226/1#using-single-pass)