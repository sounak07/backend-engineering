# Salesforce MTS / SMTS — OA & DSA Interview Questions (Compiled)

Companion to the LLD/HLD compilation. Same source sweep: interview-experience aggregator sites, LeetCode Discuss, Reddit/Blind, Glassdoor, and individual Medium write-ups — mostly 2024–2026, India offices (Bangalore/Hyderabad).

**Format notes across sources:**

- OA is almost always on **HackerRank**, **2–3 problems**, **60–90 minutes**, LeetCode Medium–to–Hard difficulty, with a reported **~80% score cutoff** to advance.
- The DSA round(s) after OA (Round 1/2 "Technical") are **live, 45–60 min**, usually 1–2 problems, often opening with a resume/project deep-dive before coding starts.
- Multiple candidates note there's no fixed bank — questions are frequently **story-wrapped variations** of well-known patterns rather than verbatim LeetCode problems, so pattern fluency matters more than memorizing exact problems.

---

## 1. Online Assessment (OA) problem statements

|#|Problem|Notes|Source|
|---|---|---|---|
|1|**Text classification for spam detection** — label texts "spam" if they contain ≥2 spam-word occurrences (case-sensitive)|Custom string/hashmap problem, not on LeetCode directly|[interviewexperiences.in – SalesForce OA](https://interviewexperiences.in/experience/salesforce/salesforce-oa)|
|2|**[Delete and Earn](https://leetcode.com/problems/delete-and-earn/description/)**|Standard LeetCode Medium (DP)|[interviewexperiences.in – SalesForce OA](https://interviewexperiences.in/experience/salesforce/salesforce-oa)|
|3|**Minimum length subarray with k distinct integers**|Sliding window|[LeetCode Discuss – SMTS Hyderabad Feb 2026](https://leetcode.com/discuss/post/7840794/salesforce-smts-hyderabad-march-2026-off-0fi6/)|
|4|**Shortest cycle in a DAG**|Graph|[LeetCode Discuss – SMTS Hyderabad Feb 2026](https://leetcode.com/discuss/post/7840794/salesforce-smts-hyderabad-march-2026-off-0fi6/)|
|5|**Sliding window variation + Tree DP** (two separate problems)|HackerRank, hidden test case failed due to integer overflow for one candidate|[interviewexperiences.in – SDE2 March 2026](https://interviewexperiences.in/experience/salesforce/salesforce-sde2-march-2026)|
|6|**Remove duplicate values from a Linked List**|Easy|[interviewexperiences.in – SMTS Interview Exp](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-1)|
|7|**Complementary string pairs forming a palindrome permutation** — count pairs (i,j) where concatenation of strings[i]+strings[j] can be rearranged into a palindrome|Custom, hashmap/bitmask-parity based|[interviewexperiences.in – SMTS Interview Exp](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-1)|
|8|**Spiral Matrix** ([LeetCode link](https://leetcode.com/problems/spiral-matrix/))|Solved fully|[Roundz Substack – SMTS Rejected](https://roundz.substack.com/p/interview-experience-salesforce-smts)|
|9|**Longest time interval without a meeting** — given total time `n` and meeting start/end arrays, find the longest gap with no meeting|Interval/sweep-line; candidate hit TLE with O(nk)|[Roundz Substack – SMTS Rejected](https://roundz.substack.com/p/interview-experience-salesforce-smts)|
|10|**Occurrence pattern encoding** — for each element, output whether it reappears earlier / later in the array as two binary strings|Custom hashmap/two-pass|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|11|**K-th largest value for every prefix of a permutation array**|Heap / order-statistics|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|12|**Minimum replacements to avoid adjacent duplicate characters** (per string in an array)|Run-length / greedy: for each run of length L, need `L // 2` replacements|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|13|**Longest subsequence of X that is also a substring of Y**|Two-pointer per starting index in Y, O(n·m)|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|14|**Kth largest in every prefix subarray of a permutation** (senior-level variant)|Maintain sorted array + binary insertion|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|15|**Spam text classification (case-insensitive variant) with duplicate-occurrence counting**|Same family as #1, phrased slightly differently at PMTS level|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|16|**Maximize sum of selected processor "power" values where selecting x excludes x−1 and x+1**|House Robber–style DP over value counts (like Delete and Earn)|[Linkjob.ai – Salesforce HackerRank writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|17|**Similar to [Coin Change](https://leetcode.com/problems/coin-change/description/)**|DP|[LeetCode Discuss – SMTS Offered](https://leetcode.com/discuss/interview-experience/6321318/Salesforce-or-SMTS-or-Awaited/)|
|18|**[Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/description/)**|Staircase search|[LeetCode Discuss – SMTS Offered](https://leetcode.com/discuss/interview-experience/6321318/Salesforce-or-SMTS-or-Awaited/)|
|19|**Similar to Maximum number of envelopes that fit inside each other (Russian Doll Envelopes)**|DP + sorting/patience sorting|[GeeksforGeeks – Salesforce On-Campus](https://www.geeksforgeeks.org/interview-experiences/salesforce-interview-experience-on-campus-4/)|
|20|**Similar to "Minimum steps to make an array decreasing"**|Array/greedy|[GeeksforGeeks – Salesforce On-Campus](https://www.geeksforgeeks.org/interview-experiences/salesforce-interview-experience-on-campus-4/)|
|21|**Similar to "Number of subsequences in a string divisible by n"**|DP over remainders|[GeeksforGeeks – Salesforce On-Campus](https://www.geeksforgeeks.org/interview-experiences/salesforce-interview-experience-on-campus-4/)|
|22|**Longest Common Subsequence**|Classic DP|[Naukri Code360 – Salesforce 2021 exp](https://www.naukri.com/code360/interview-experiences/salesforce/salesforce-interview-experience-apr-2021-exp-0-2-years)|

## 2. DSA (live technical) round problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**[Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)**|Paired with the BookMyShow LLD in the same round|[interviewexperiences.in – SMTS Offer](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-offer)|
|2|**Graph traversal (BFS) with conditions, story-format**|Round 2, separate from Round 1 DSA|[interviewexperiences.in – SMTS Offer](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-offer)|
|3|**Variation of Longest Palindromic Substring**|Same round as above|[interviewexperiences.in – SMTS Offer](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-offer)|
|4|**"Meximum"** — for every window of size k compute the min, then return the max of those window-minimums|Sliding window + monotonic deque|[interviewexperiences.in – SMTS Hyderabad Feb 2026](https://interviewexperiences.in/experience/salesforce/salesforce-smts-hyderabad-feb-2026-offer)|
|5|**Cycle detection in a DAG** (approach-only, no code required)|Interviewer only wanted verbal approach|[interviewexperiences.in – SMTS Hyderabad Feb 2026](https://interviewexperiences.in/experience/salesforce/salesforce-smts-hyderabad-feb-2026-offer)|
|6|**Floyd–Warshall (all-pairs shortest path)**|Rated "easy" by candidate|[interviewexperiences.in – SMTS MissionForce](https://interviewexperiences.in/experience/salesforce/salesforce-interview-smts-missionforce-team-hyderabad-location)|
|7|**Add two polynomials**|Asked in the Hiring Manager round, not the DSA round|[interviewexperiences.in – SMTS MissionForce](https://interviewexperiences.in/experience/salesforce/salesforce-interview-smts-missionforce-team-hyderabad-location)|
|8|**Variation of "Maximum Profit Triplet"**|Discussed Fenwick Tree vs. Segment Tree tradeoffs; candidate coded O(n²) fallback|[interviewexperiences.in – SDE2 March 2026](https://interviewexperiences.in/experience/salesforce/salesforce-sde2-march-2026)|
|9|**[Reorganize String](https://leetcode.com/problems/reorganize-string/)**|Heap/greedy|[interviewexperiences.in – SMTS Interview Exp](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-1)|
|10|**[Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/)**|Backtracking|[interviewexperiences.in – SMTS Interview Exp](https://interviewexperiences.in/experience/salesforce/salesforce-smts-interview-experience-1)|
|11|**Given a dictionary and a character array, count valid words formable from the characters**|Trie/hashmap|[LeetCode Discuss – MTS 12th July](https://leetcode.com/discuss/post/5526715/salesforce-interview-experience-mts-12th-dbi1/)|
|12|**Snake and Ladder — minimum dice throws to reach the last cell**|BFS shortest path on graph of board positions|[LeetCode Discuss – MTS 12th July](https://leetcode.com/discuss/post/5526715/salesforce-interview-experience-mts-12th-dbi1/)|
|13|**Count of all triplets** (variation of an earlier "similar" question)|Follow-up to a prior round's problem|[LeetCode Discuss – MTS Interview Experience](https://leetcode.com/discuss/interview-question/4257345/Salesforce-or-MTS-Interview-Experience/)|
|14|**Priority Queue–based problem** (LC Easy–Medium, exact prompt not recalled)|Paired with a graph problem in the same round|[LeetCode Discuss – MTS Bangalore Selected](https://leetcode.com/discuss/interview-experience/6934266/)|
|15|**Graph problem (LC Medium, exact prompt not recalled)**|Same round as above|[LeetCode Discuss – MTS Bangalore Selected](https://leetcode.com/discuss/interview-experience/6934266/)|
|16|**Given dictionary/char array + Snake-and-Ladder pairing** (also seen standalone)|See #11–12|—|
|17|**Zigzag string traversal** — given a string and number of rows, print zigzag order|Classic LC Medium pattern|[CodingKaro – Salesforce compilation](https://www.codingkaro.in/jobs-internships/leetcode-interview-experience/Salesforce)|
|18|**Phone keypad letter combinations** (like [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/))|Backtracking|[CodingKaro – Salesforce compilation](https://www.codingkaro.in/jobs-internships/leetcode-interview-experience/Salesforce)|
|19|**K-th greatest element for every subarray from size K to N**|Heap / sliding window order-statistics|[LeetCode Discuss – LMTS April 2025 Offer](https://leetcode.com/discuss/post/6857467/salesforce-interview-experience-lmts-apr-a9rw/)|
|20|**Reorder array in-place: all negatives first, then positives**|Two-pointer partition|[LeetCode Discuss – LMTS April 2025 Offer](https://leetcode.com/discuss/post/6857467/salesforce-interview-experience-lmts-apr-a9rw/)|
|21|**For each index: has this value appeared before / will it appear again? (two binary strings)**|Two-pass hashmap|[LeetCode Discuss – LMTS April 2025 Offer](https://leetcode.com/discuss/post/6857467/salesforce-interview-experience-lmts-apr-a9rw/)|
|22|**After each 0→1 update in a binary array, count sweeps needed to fully sort it**|Simulation / bubble-sort-pass counting|[LeetCode Discuss – LMTS April 2025 Offer](https://leetcode.com/discuss/post/6857467/salesforce-interview-experience-lmts-apr-a9rw/)|
|23|**Sort names containing Roman numerals — by name, then by numeral value**|String parsing + custom comparator|[Linkjob.ai – General SDE Backend OA writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|24|**Given campaign costs and number of weeks, partition optimally to minimize the sum of weekly maxima**|DP/binary-search-on-answer partition problem|[Linkjob.ai – General SDE Backend OA writeup](https://www.linkjob.ai/interview-questions/salesforce-hackerrank-test/)|
|25|**Given M microservices' daily pass/fail status, find the longest streak of all-pass days**|Array scan|[Medium – MTS Selected (Tanu)](https://medium.com/@tanushreeb2607/my-salesforce-interview-experience-mts-selected-dc9a12c230bf)|
|26|**[Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)**|Linked list, recursive approach discussed with complexity follow-up|[Medium – MTS Interview Exp (Imran)](https://medium.com/@imran2018wahid/salesforce-mts-interview-experience-b7ffe939d21f)|
|27|**Longest subsequence of X that is a substring of Y** (also appears in OA table)|Same problem asked live in some loops|[Medium – MTS Interview Exp (Imran)](https://medium.com/@imran2018wahid/salesforce-mts-interview-experience-b7ffe939d21f)|
|28|**Number of Islands**|Standard grid BFS/DFS, reported as an easy round|[Glassdoor – SMTS Software Engineer Interview Qs](https://www.glassdoor.co.in/Interview/Salesforce-SMTS-Software-Engineer-Interview-Questions-EI_IE11159.0,10_KO11,33.htm)|
|29|**Quick Sort — explain the algorithm/approach** (conceptual, not coded)|Also asked to compare top-down vs. bottom-up DP|[LeetCode Discuss – MTS Interview Exp 2026](https://leetcode.com/discuss/post/7561138/salesforce-mts-interview-experience-2026-nl4g/)|
|30|**Candidate's choice: board-game simulation problem OR implement LRU Cache**|Interviewer offered a choice; candidate picked LRU Cache|[LeetCode Discuss – MTS Interview Exp 2026](https://leetcode.com/discuss/post/7561138/salesforce-mts-interview-experience-2026-nl4g/)|
|31|**Decode-string-style problem with many edge cases** (exact prompt not recalled, no LC match found)|Custom string parsing|[LeetCode Discuss – MTS Interview Exp 2026](https://leetcode.com/discuss/post/7561138/salesforce-mts-interview-experience-2026-nl4g/)|
|32|**Network connectivity / minimum time to connect all nodes with variable edge weights** — evolves into Dijkstra follow-up ("what if each connection has a different time?")|Graph, MST→shortest-path pivot|[LeetCode Discuss – MTS Bangalore May 2026](https://leetcode.com/discuss/post/8354296/salesforce-mts-bangalore-may-2026-by-ano-ckd0/)|
|33|**0-1 Knapsack variant with extra conditions**|DP|[Medium – Deepanshi Sharma](https://medium.com/@deecodes/salesforce-interview-experience-bc816d38bdc1)|
|34|**Count palindromic subsequences in a string**|Classic interval DP|[GeeksforGeeks – Salesforce On-Campus](https://www.geeksforgeeks.org/interview-experiences/salesforce-interview-experience-on-campus-4/)|

## 3. Pattern frequency summary (what to drill)

Based on how often each pattern recurs across the sources above:

1. **Sliding window / monotonic deque** — "Meximum," min-subarray-with-k-distinct, campaign-cost partitioning. High frequency.
2. **Graph (BFS/DFS/shortest-path/cycle-detection)** — DAG cycle detection, Floyd–Warshall, Snake & Ladder BFS, Dijkstra follow-up, Number of Islands, story-wrapped BFS. The single most recurring category.
3. **DP** — Delete and Earn, processor-power maximization (House-Robber family), Maximum Profit Triplet, 0-1 Knapsack variants, LCS, palindromic subsequence counting, weekly-maxima partitioning.
4. **Two-pointer / array partitioning** — negatives-then-positives reorder, longest-subsequence-that's-a-substring.
5. **Heap / order statistics** — K-th largest per prefix, K-th greatest per sliding window.
6. **Hashmap/counting on strings** — spam classification, complementary palindrome pairs, occurrence-encoding, run-length replacement counting.
7. **Classic data structures asked directly** — LRU Cache implementation, Reverse Nodes in k-Group, Combination Sum II, Generate Parentheses, Reorganize String.

This lines up closely with your existing prep list (sliding window, prefix sum, graph patterns) — **graph problems (especially with a cycle-detection or shortest-path twist) and sliding-window/monotonic-structure problems are the two highest-value buckets** to keep sharp for Salesforce specifically, alongside general DP fluency.

## 4. Format / process notes

- OA cutoff is reportedly **~80%** correct to advance (per one recruiter's explicit statement).
- Some OAs include a **custom, non-LeetCode problem** (spam classification, processor-power maximization) alongside one standard LeetCode-style problem — don't assume every OA problem will have a direct LC match.
- DSA rounds are sometimes **only evaluated on verbal approach**, not working code (e.g., the DAG cycle-detection question above) — practice articulating complexity tradeoffs out loud, not just typing solutions.
- Interviewers sometimes **offer a choice of problem** or **swap the question mid-round** if you're stuck (seen in both the LRU Cache case and the thread-safe-scheduler→Observer-pattern swap from the LLD compilation) — a sign it's worth saying "I'm not confident implementing X live, could we pivot to Y where I can show clean code" rather than freezing.
- A few Fresher/Intern-level OAs include **MCQs** (JS/web-dev, OOPS/DBMS) alongside the coding problems — not relevant at your level but confirms the OA format varies by track.

---

_Compiled July 24, 2026. Interview content varies by team and changes over time — treat this as directional pattern-matching, not a guaranteed question bank._