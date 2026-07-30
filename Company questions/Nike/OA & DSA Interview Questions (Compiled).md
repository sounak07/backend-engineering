
Companion to the Nike LLD/HLD doc. Same sources: `interviewexperiences.in`, LeetCode Discuss, Glassdoor, CodingKaro — mostly 2025–2026, India offices.

**Format notes:** Nike's OA/live-coding format is less standardized across sources than Salesforce's HackerRank-heavy pipeline. Several accounts describe **no separate OA at all** — DSA is assessed live, sometimes on a **whiteboard or pen-and-paper** rather than an IDE, with the interviewer explicitly more interested in **approach and complexity analysis than working code**. Where an OA does exist (e.g., internship loops), it's **HackerRank-hosted, live/collaborative** rather than an async take-home.

---

## 1. Online Assessment (OA) problem statements

|#|Problem|Notes|Source|
|---|---|---|---|
|—|_No fully-specified async OA problem statements surfaced._|One intern account confirms the "OA" was actually a **live, collaborative HackerRank pair-programming session** (~1 hour) rather than an async test — Nike appears to skip a traditional take-home OA for many roles, moving straight to live technical rounds|[LockedIn AI – Nike SWE Intern Interview Review](https://www.lockedinai.com/company-details/NKE/7c69170c-e767-4599-86a2-33b6f661401c)|
|—|Some loops include a **HireVue async video interview** (behavioral/situational) before any technical round|Confirms a non-coding screening stage exists for some tracks|[LockedIn AI – Nike SWE Intern Interview Review](https://www.lockedinai.com/company-details/NKE/7c69170c-e767-4599-86a2-33b6f661401c)|

## 2. DSA (live technical) round problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**[Sqrt(x)](https://leetcode.com/problems/sqrtx/description/)** — compute integer square root|SDE 3, Team 2, R1 — only 30 min; interviewer cared more about approach/analysis of the optimized solution than the code itself|[interviewexperiences.in – Nike SDE 3 Interview Experience](https://interviewexperiences.in/experience/nike/nike-sde-3-interview-experience)|
|2|**Modified version of [Permutations](https://leetcode.com/problems/permutations/description/)**, solved recursively with follow-ups|SDE 1, Round 1 — strict timing (5 min to understand, 5 min to explain approach + complexity, 10 min to write full code, pen-and-paper format)|[LeetCode Discuss – Nike SDE 1 Interview Experience](https://leetcode.com/discuss/interview-experience/6739533/)|
|3|**[Group Anagrams](https://leetcode.com/problems/group-anagrams/description/)**|Same SDE 1 loop|[CodingKaro – Nike SDE 1 Interview Experience](https://www.codingkaro.in/jobs-internships/leetcode-interview-experience/NIKE)|
|4|**Maximum integer in a nested array** (arbitrarily nested list/array structure)|Same SDE 1 loop|[LeetCode Discuss – Nike SDE 1 Interview Experience](https://leetcode.com/discuss/interview-experience/6739533/)|
|5|**[Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)**|SDE 2 Backend loop, paired with a long list of core Java conceptual questions (method overloading, Comparator vs. Comparable, interface vs. abstract class, `equals` vs. `==`, Java 8 default methods, StringBuilder/StringBuffer)|[LeetCode Discuss – Nike SDE 2 Backend Round 1](https://leetcode.com/discuss/interview-experience/6920229/)|
|6|**Variation of Longest Consecutive Sequence**|SDE-2, Round 1 — candidate answered quickly enough that pseudocode explanation sufficed instead of full code|[interviewexperiences.in – SDE-2 Nike Experience](https://interviewexperiences.in/experience/nike/sde-2-nike-experience)|
|7|**"Target Sum in One Pass"** — given an array and target `k`, determine if any two numbers sum to `k`, required to be solved in a single pass with a HashMap|Generic technical round; example given: `[10,15,3,7], k=17 → true`|[interviewexperiences.in – My Nike Interview Experience](https://interviewexperiences.in/experience/nike/my-nike-interview-experience)|
|8|**[Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)** (no division allowed)|Same round as above|[interviewexperiences.in – My Nike Interview Experience](https://interviewexperiences.in/experience/nike/my-nike-interview-experience)|
|9|**HashMap internals conceptual question** — a `Student` class with `hashCode()` always returning `1`; walked through bucket collisions, `equals()` resolution, and skewed-distribution handling|Framed as a DSA-adjacent Java-internals question rather than pure algorithmic coding|[interviewexperiences.in – My Nike Interview Experience](https://interviewexperiences.in/experience/nike/my-nike-interview-experience)|
|10|**DP: variation of Knapsack or Coin Change**, focused specifically on transition states and space optimization|SE-2, Round 2 (Technical Round, conducted by an SE-3)|[interviewexperiences.in – SE-2 Nike Interview Exp](https://interviewexperiences.in/experience/nike/se-2-nike-interview-exp)|
|11|**"Binary Search on Answer"-style problem**|Same SE-2 round; followed by an explicit O(n log n) vs. O(n) complexity discussion|[interviewexperiences.in – SE-2 Nike Interview Exp](https://interviewexperiences.in/experience/nike/se-2-nike-interview-exp)|
|12|**One Medium-level Array/String manipulation problem** (exact prompt not disclosed)|SE-2, Round 1 (Bar-Raiser, conducted by a third party)|[interviewexperiences.in – SE-2 Nike Interview Exp](https://interviewexperiences.in/experience/nike/se-2-nike-interview-exp)|
|13|**Variation of Longest Palindromic Substring / string manipulation** (unspecified prompt referenced generically in aggregator prep guides)|Cited as representative difficulty ("Medium, arrays/strings/trees") rather than a confirmed specific prompt|[Dataford – NIKE Software Engineer Interview Guide](https://dataford.io/interview-guides/nike/software-engineer)|

## 3. Java/conceptual questions that recur alongside DSA

Nike's live rounds blend algorithmic DSA with a heavier-than-usual dose of **language/framework internals**, especially for backend roles:

- **Core Java**: method overloading, `Comparator` vs. `Comparable`, interface vs. abstract class, `equals()` vs. `==`, Java 8 default methods, `StringBuilder`/`StringBuffer`, pass-by-value semantics and object mutation gotchas.
- **Spring Boot**: bean lifecycle, annotations, dependency injection, exception handling, multithreading.
- **HashMap internals**: bucket/collision behavior under a poor `hashCode()` implementation.
- **Cloud/AWS theory**: EC2 vs. Lambda, S3 vs. RDS, SQS/SNS for decoupling — asked even of candidates without hands-on AWS experience, evaluated as conceptual understanding.

## 4. Pattern summary

- **Sliding-window/array fundamentals, HashMap-based one-pass problems, and DP transition-state problems (Knapsack/Coin Change family) recur most** — broadly consistent with your existing sliding-window/prefix-sum/graph prep, though Nike leans more DP/array/hashmap than graph-heavy compared to what showed up in the Salesforce dataset.
- **Time pressure and format vary a lot by round** — some rounds are strict pen-and-paper with hard 5/5/10-minute splits (understand/explain/code), others are relaxed IDE-based collaborative sessions where a correct approach with pseudocode is enough if time is short.
- **Interviewers frequently care more about approach/complexity articulation than a fully working, compiled solution** — several accounts explicitly note the interviewer cut the coding short once the approach and complexity were clearly explained. Worth practicing crisp verbal complexity justification as its own skill, separate from typing the final code.
- **Backend/Java-heavy loops pair DSA with a long tail of framework and language internals questions** — worth brushing up Java 8+ features, Spring Boot internals, and basic AWS service tradeoffs alongside DSA grinding, since these appear to be asked nearly every round rather than as an occasional aside.

## 5. Sources scanned

- [interviewexperiences.in — Nike filter](https://interviewexperiences.in/company/nike)
- LeetCode Discuss (Nike SDE 1/2/3 and SWE I interview-experience threads)
- Glassdoor — NIKE Software Engineer interview questions
- CodingKaro — Nike interview experience aggregation
- LockedIn AI — Nike SWE Intern interview review
- Dataford — NIKE Software Engineer interview guide (flagged where content is guide-generated rather than a confirmed candidate account)

---

_Compiled July 27, 2026. Coverage is moderate — treat as directional pattern-matching, not a guaranteed question bank._