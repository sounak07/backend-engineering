
# DSA Patterns Notebook  
  
A structured notebook for **interview preparation**.  
  
Use each problem section to add:  
- Observations  
- Edge cases  
- Tricks discovered  
- Mistakes made  
  
---  
  
# Pattern Index  
  
| Pattern | Problems |  
|------|------|  
| [#Prefix Suffix Sum](./#Prefix_Suffix_Sum.md) | All Division Highest Score |  
| [#Two Pointers](./#Two_Pointers.md) | Pair problems, Merge arrays |  
| [#Three Pointers](./#Three_Pointers.md) | 3Sum, Sort Colors |  
| [#Boyer Moore Voting](./#Boyer_Moore_Voting.md) | Majority Element |  
| [#Sliding Window](./#Sliding_Window.md) | Longest substring |  
| [#Hashing](./#Hashing.md) | Longest subarray sum K |  
| [#Greedy](./#Greedy.md) | Max number of 1s II |  
| [#Binary Search](./#Binary_Search.md) | Aggressive cows, Capacity to ship |  
| [#Backtracking](./#Backtracking.md) | Subsets, Combination sum |  
  
---  
  
# Templates  
  
---  
  
## Two Pointer Template  
  
```python  
i = 0  
j = len(arr) - 1  
  
while i < j:  
  
    if condition:  
        i += 1  
  
    elif condition:  
        j -= 1  
  
    else:  
        process(i, j)

---

## Sliding Window Template

left = 0  
state = 0  
answer = 0  
  
for right in range(len(arr)):  
  
    if is_bad(arr[right]):  
        state += 1  
  
    while state > K:  
        if is_bad(arr[left]):  
            state -= 1  
        left += 1  
  
    answer = max(answer, right - left + 1)

---

## Binary Search Template

l = 0  
r = len(arr) - 1  
  
while l <= r:  
  
    mid = (l + r) // 2  
  
    if arr[mid] == target:  
        return mid  
  
    elif arr[mid] < target:  
        l = mid + 1  
  
    else:  
        r = mid - 1

---

## Binary Search on Answer

def valid(x):  
    pass  
  
l = min_possible  
r = max_possible  
  
while l <= r:  
  
    mid = (l + r) // 2  
  
    if valid(mid):  
        ans = mid  
        r = mid - 1  
  
    else:  
        l = mid + 1

---

## Backtracking Template

def dfs(i):  
  
    if solution_condition:  
        res.append(path.copy())  
        return  
  
    if termination_condition:  
        return  
  
    for choice in choices:  
  
        path.append(choice)  
  
        dfs(next_state)  
  
        path.pop()
```

# Prefix Suffix Sum

## All Division Highest Score

Link  
[https://leetcode.com/problems/all-divisions-with-the-highest-score-of-a-binary-array/description/](https://leetcode.com/problems/all-divisions-with-the-highest-score-of-a-binary-array/description/)

### Pattern

Prefix Sum + Suffix Sum

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

# Two Pointers

---

## Closest Pair from Two Arrays

[https://www.geeksforgeeks.org/problems/find-the-closest-pair-from-two-arrays4215/1](https://www.geeksforgeeks.org/problems/find-the-closest-pair-from-two-arrays4215/1)

### Pattern

Two Pointers (Opposite direction)

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Pair Sum Closest to 0

[https://www.geeksforgeeks.org/problems/two-numbers-with-sum-closest-to-zero1737/1](https://www.geeksforgeeks.org/problems/two-numbers-with-sum-closest-to-zero1737/1)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Find All Pairs in Given Sum

[https://www.geeksforgeeks.org/problems/find-all-pairs-whose-sum-is-x5808/1](https://www.geeksforgeeks.org/problems/find-all-pairs-whose-sum-is-x5808/1)

### Pattern

Two Pointers / Hashing

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Count Pairs Sum Less Than Target

[https://www.geeksforgeeks.org/problems/count-pairs-whose-sum-is-less-than-target/1](https://www.geeksforgeeks.org/problems/count-pairs-whose-sum-is-less-than-target/1)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Union of Arrays

[https://www.geeksforgeeks.org/problems/union-of-two-sorted-arrays-1587115621/1](https://www.geeksforgeeks.org/problems/union-of-two-sorted-arrays-1587115621/1)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Merge Two Sorted Arrays

[https://leetcode.com/problems/merge-sorted-array/](https://leetcode.com/problems/merge-sorted-array/)

### Pattern

Two Pointers (Backward)

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Remove Duplicates from Sorted Array II

[https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Remove Element

[https://leetcode.com/problems/remove-element/](https://leetcode.com/problems/remove-element/)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Compare Version Numbers

[https://leetcode.com/problems/compare-version-numbers/](https://leetcode.com/problems/compare-version-numbers/)

### Pattern

Two Pointer Parsing

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Valid Palindrome

[https://leetcode.com/problems/valid-palindrome/](https://leetcode.com/problems/valid-palindrome/)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Reverse Words in String

[https://leetcode.com/problems/reverse-words-in-a-string/](https://leetcode.com/problems/reverse-words-in-a-string/)

### Pattern

Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

## Next Permutation

[https://leetcode.com/problems/next-permutation/](https://leetcode.com/problems/next-permutation/)

### Pattern

Greedy + Two Pointers

### Key Idea

### Observations

### Edge Cases

### Complexity

Time:  
Space:

### Notes

---

> [!tip] Duplicate Counting Pattern

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
  
for _ in range(c1 * c2):  
    res.append([val1, val2])

---

# Three Pointers

---

## 3 Sum

[https://leetcode.com/problems/3sum/](https://leetcode.com/problems/3sum/)

### Pattern

Sorting + Two Pointers

### Notes

---

## Sort Colors

[https://leetcode.com/problems/sort-colors/](https://leetcode.com/problems/sort-colors/)

### Pattern

Dutch National Flag

### Notes

---

## 4 Sum

[https://leetcode.com/problems/4sum/](https://leetcode.com/problems/4sum/)

### Pattern

Two Pointers

### Notes

---

# Boyer Moore Voting

---

## Majority Element

[https://leetcode.com/problems/majority-element/](https://leetcode.com/problems/majority-element/)

### Pattern

Boyer Moore Voting

### Notes

---

## Majority Element II

[https://leetcode.com/problems/majority-element-ii/](https://leetcode.com/problems/majority-element-ii/)

### Pattern

Extended Boyer Moore

### Notes

---

# Sliding Window

---

## Maximum 1s

[https://www.geeksforgeeks.org/problems/maximize-number-of-1s0905/1](https://www.geeksforgeeks.org/problems/maximize-number-of-1s0905/1)

### Pattern

Sliding Window

### Notes

---

## Longest Substring Without Repeating Characters

[https://leetcode.com/problems/longest-substring-without-repeating-characters/](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

### Pattern

Sliding Window + Hashmap

### Notes

---

## Longest Substring With At Least K Repeating

[https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/)

### Pattern

Sliding Window / Divide and conquer

### Notes

---

## Count Complete Subarrays

[https://leetcode.com/problems/count-complete-subarrays-in-an-array/](https://leetcode.com/problems/count-complete-subarrays-in-an-array/)

### Pattern

Sliding Window

### Notes

---

> [!tip] Sliding Window Formula

AT_MOST(K) = EXACT(1) + EXACT(2) + ... + EXACT(K)  
  
EXACT(K) = AT_MOST(K) - AT_MOST(K-1)

---

# Hashing

---

## Longest Subarray With Sum K

[https://www.geeksforgeeks.org/problems/longest-sub-array-with-sum-k0809/1](https://www.geeksforgeeks.org/problems/longest-sub-array-with-sum-k0809/1)

### Pattern

Prefix Sum + Hashmap

### Notes

---

# Greedy

---

## Max Number of 1s II

[https://www.geeksforgeeks.org/dsa/max-number-of-one-ii/](https://www.geeksforgeeks.org/dsa/max-number-of-one-ii/)

### Pattern

Greedy / Kadane Variant

### Notes

---

# Arrays

---

## Min and Second Min

[https://www.geeksforgeeks.org/problems/find-the-smallest-and-second-smallest-element-in-an-array3226/1](https://www.geeksforgeeks.org/problems/find-the-smallest-and-second-smallest-element-in-an-array3226/1)

### Pattern

Single pass

### Notes

---

# Binary Search

---

## Sorted Insert Position

[https://www.geeksforgeeks.org/problems/search-insert-position-of-k-in-a-sorted-array/1](https://www.geeksforgeeks.org/problems/search-insert-position-of-k-in-a-sorted-array/1)

### Pattern

Binary Search

### Notes

---

## Capacity to Ship Packages

[https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

### Pattern

Binary Search on Answer

### Notes

---

## Search in 2D Matrix

[https://leetcode.com/problems/search-a-2d-matrix/](https://leetcode.com/problems/search-a-2d-matrix/)

### Pattern

Binary Search

### Notes

---

## Search in 2D Matrix II

[https://leetcode.com/problems/search-a-2d-matrix-ii/](https://leetcode.com/problems/search-a-2d-matrix-ii/)

### Pattern

Matrix search

### Notes

---

## Aggressive Cows

[https://www.geeksforgeeks.org/problems/aggressive-cows/1](https://www.geeksforgeeks.org/problems/aggressive-cows/1)

### Pattern

Binary Search on Answer

### Notes

---

## Search in Rotated Sorted Array

[https://leetcode.com/problems/search-in-rotated-sorted-array-ii/](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

### Pattern

Modified Binary Search

### Notes

---

## Find Minimum in Rotated Array

[https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

### Pattern

Binary Search

### Notes

---

## Find Peak Element

[https://leetcode.com/problems/find-peak-element/](https://leetcode.com/problems/find-peak-element/)

### Pattern

Binary Search

### Notes

---

# Backtracking

---

## Subsets

[https://leetcode.com/problems/subsets/](https://leetcode.com/problems/subsets/)

### Pattern

Backtracking

### Notes

---

## Subsets II

[https://leetcode.com/problems/subsets-ii/](https://leetcode.com/problems/subsets-ii/)

### Pattern

Backtracking + Duplicate handling

### Notes

---

## Combination Sum

[https://leetcode.com/problems/combination-sum/](https://leetcode.com/problems/combination-sum/)

### Pattern

Backtracking

### Notes

---

## Combination Sum II

[https://leetcode.com/problems/combination-sum-ii/](https://leetcode.com/problems/combination-sum-ii/)

### Pattern

Backtracking

### Notes