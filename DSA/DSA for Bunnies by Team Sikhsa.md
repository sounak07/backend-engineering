
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
[Version compare](https://leetcode.com/problems/compare-version-numbers/description/)
[Valid Palindrome](https://leetcode.com/problems/valid-palindrome/submissions/1896782577/)
[Reverse words in a string](https://leetcode.com/problems/reverse-words-in-a-string/description/)
[Next Permutation](https://leetcode.com/problems/next-permutation/)

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
[4 Sum](https://leetcode.com/problems/4sum/)

### Boyer-Moore Algo

Note: Everything depends on how many majority elements can there be.

[Majority Element](https://leetcode.com/problems/majority-element/description/)
[Majority Element II](https://leetcode.com/problems/majority-element-ii/description/)

### Sliding windows

[Maximum 1s](https://www.geeksforgeeks.org/problems/maximize-number-of-1s0905/1)
[Count Pairs less than target](https://www.geeksforgeeks.org/problems/count-pairs-whose-sum-is-less-than-target/1)
[Longest Substring without repeating characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/submissions/1903518498/)
[Longest Substring with At Least K Repeating Characters](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/)
[Count Complete Subarrays](https://leetcode.com/problems/count-complete-subarrays-in-an-array/)

```python
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

### Hashing

[Longest Subarray with Sum K](https://www.geeksforgeeks.org/problems/longest-sub-array-with-sum-k0809/1)

### Greedy
[Max number of 1s II](https://www.geeksforgeeks.org/dsa/max-number-of-one-ii/)

### Arrays
[Min and 2min](https://www.geeksforgeeks.org/problems/find-the-smallest-and-second-smallest-element-in-an-array3226/1#using-single-pass)

### Binary Search
[Sorted Insert Position](https://www.geeksforgeeks.org/problems/search-insert-position-of-k-in-a-sorted-array/1)
[Capacity to ship](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
[Search in 2d matrix](https://leetcode.com/problems/search-a-2d-matrix/)
[Search in 2d matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/)
[Aggressive cows](https://www.geeksforgeeks.org/problems/aggressive-cows/1)
[Search in rotated Sorted list](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)






