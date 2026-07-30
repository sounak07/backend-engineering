
Same method as the earlier compilations, combined into one doc — Harness's process is dominated by **live DSA and machine-coding rounds**; a couple of Glassdoor mentions reference a lightweight OA ("simple Q's mostly") for some tracks, but no candidate account surfaced a specific OA problem statement, so it's folded in here rather than getting its own section. Sources: `interviewexperiences.in`, LeetCode Discuss, Glassdoor, GeeksforGeeks, Medium, and EnginEBogie — mostly 2023–2026, India (Bangalore/Bengaluru) offices, with a couple of US (New York) data points for senior/staff levels.

Harness uses a standard **SDE 1 / SDE 2 (Senior SDE) / Staff / Principal** ladder. Every level — including SDE-1/intern — gets **live pair-programming-style DSA rounds**; **machine coding / LLD rounds** become common from SDE-2 upward; **dedicated system design rounds** appear consistently at Senior+ and are near-mandatory at Staff/Principal.

---

## 1. DSA (live coding) problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**[GCD Sort of an Array](https://leetcode.com/problems/gcd-sort-of-an-array/description/)** (LeetCode Hard)|Senior SDE, Round 2, after a Hiring Manager discussion|[LeetCode Discuss – Harness Senior SDE Offer](https://leetcode.com/discuss/post/7560806/)|
|2|**Search in a row-wise and column-wise sorted matrix**|Software Engineer 2024 loop, problem 1 of 3|[GeeksforGeeks – Harness Interview Experience 2024](https://www.geeksforgeeks.org/interview-experiences/harness-interview-experience-for-software-engineer-2024/)|
|3|**Minimum time to burn a binary tree from a given node**|Same loop, problem 2 — candidate was weak on trees and asked to swap the question|[GeeksforGeeks – Harness Interview Experience 2024](https://www.geeksforgeeks.org/interview-experiences/harness-interview-experience-for-software-engineer-2024/)|
|4|**[Paint House](https://leetcode.com/problems/paint-house/description/)**|Same loop, problem 3 — recursive → DP/memoization escalation; candidate struggled with the recursive formulation|[GeeksforGeeks – Harness Interview Experience 2024](https://www.geeksforgeeks.org/interview-experiences/harness-interview-experience-for-software-engineer-2024/)|
|5|**Find an index where sum of left subarray == sum of right subarray** (return -1 if none exists)|Senior SDE, Round 1 (60 min), problem 1 of 2|[LeetCode Discuss – Harness Senior SDE Offer, Dec '23](https://leetcode.com/discuss/interview-experience/4465747/Harness-or-Senior-Software-Engineer-or-Bangalore-or-Dec'23-Offer/)|
|6|**[Symmetric Tree](https://leetcode.com/problems/symmetric-tree/description/)**|Same round, problem 2|[LeetCode Discuss – Harness Senior SDE Offer, Dec '23](https://leetcode.com/discuss/interview-experience/4465747/Harness-or-Senior-Software-Engineer-or-Bangalore-or-Dec'23-Offer/)|
|7|**Sort a list of integers by count of set bits (1's) in binary representation**, preserving original order for ties — similar to [Sort Integers by the Number of 1 Bits](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/description/)|Same loop, Round 2 (60 min), problem 1 of 2|[LeetCode Discuss – Harness Senior SDE Offer, Dec '23](https://leetcode.com/discuss/interview-experience/4465747/Harness-or-Senior-Software-Engineer-or-Bangalore-or-Dec'23-Offer/)|
|8|**Sort a binary (0/1) array without using a built-in sort function**|SDE-1, Round 2 (Engineering Manager, tech + behavioral), problem 1 of 2, rated Easy|[LeetCode Discuss – Harness SDE-1 Selected](https://leetcode.com/discuss/interview-experience/3732347/Harness-oror-SDE-1-oror-Bangalore-oror-Selected/)|
|9|**[Range Sum of BST](https://leetcode.com/problems/range-sum-of-bst/description/)**|SDE Intern loop, one of the coding rounds|[interviewexperiences.in – Harness SDE Intern, Bangalore, Selected](https://interviewexperiences.in/experience/harness/harness-sde-intern-banglore-march-2023-selected)|
|10|**[Merge Intervals](https://leetcode.com/problems/merge-intervals/description/)**|Same SDE Intern loop|[interviewexperiences.in – Harness SDE Intern, Bangalore, Selected](https://interviewexperiences.in/experience/harness/harness-sde-intern-banglore-march-2023-selected)|
|11|**Complex tree-evaluation problem involving logical operators and numeric intervals** (custom, not a named LC problem)|Senior SDE loop, Round 1 (60 min)|[EnginEBogie – Harness Senior SDE Interview Experience](https://enginebogie.com/interview/experience/harness-senior-software-development-engineer/1522)|
|12|**Implement a Trie (prefix tree) in TypeScript**|SDE I, Peer Programming Round 1 — paired with a discussion on API request-optimization techniques|[interviewexperiences.in – Harness SDE I Interview](https://interviewexperiences.in/experience/harness/harness-interview-experience-sde-i)|
|13|**Render a text-based folder/tree structure into HTML** using nested list elements (`<ul>/<li>`) — input given as an ASCII tree (`|- A`,`|- B`,`|
|14|**Standard DP question, "House Robbery"-style ([House Robber](https://leetcode.com/problems/house-robber/description/))**|Reported generically among a 3-question Senior SE loop (paired with a linked-list question and an LLD question — see below)|[Glassdoor – Harness Senior Software Engineer Interview Qs](https://www.glassdoor.com/Interview/Harness-Senior-Software-Engineer-Interview-Questions-EI_IE1828521.0,7_KO8,32.htm)|
|15|**Medium-difficulty linked list question** (exact prompt not disclosed)|Same Senior SE loop as above|[Glassdoor – Harness Senior Software Engineer Interview Qs](https://www.glassdoor.com/Interview/Harness-Senior-Software-Engineer-Interview-Questions-EI_IE1828521.0,7_KO8,32.htm)|
|16|**Whiteboard algo/DS round, 2 problems, medium-to-hard**, at a US (New York) Principal-level loop|First technical round of a 3-round US loop; second round paired a medium algo-DS problem with an OO-design problem|[Glassdoor – Harness Senior Software Engineer Interview Qs](https://www.glassdoor.com/Interview/Harness-Senior-Software-Engineer-Interview-Questions-EI_IE1828521.0,7_KO8,32.htm)|
|17|**1 hard + 1 medium problem, candidate's choice of language**, with explicit grading on optimized/bug-free/syntactically-correct code, complexity analysis, and dry-run with edge cases|Senior SDE technical round|[Medium – Senior SDE Interview at Harness (Krishna Mundra)](https://medium.com/@23krishna.mundra/senior-sde-interview-at-harness-my-full-experience-questions-what-i-wish-i-knew-011eec393862)|

## 2. LLD / Machine-Coding problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**Design a simplified Shopify** — multi-tenant architecture (multiple independently-catalogued stores), inventory management with correctness guarantees (no overselling / no negative inventory), cart functionality, order placement with inventory validation + deduction, and a **pluggable payment-integration abstraction** (interface only, no real payment logic)|Senior SDE loop, appears to be the "appeared again" / second-attempt round after an earlier Hiring Manager + hard-LC round|[LeetCode Discuss – Harness Senior SDE Interview](https://leetcode.com/discuss/post/7560806/)|
|2|**Complete ordering and inventory management system** — full machine-coding implementation|Senior SDE loop, Round 2 (90 minutes)|[EnginEBogie – Harness Senior SDE Interview Experience](https://enginebogie.com/interview/experience/harness-senior-software-development-engineer/1522)|
|3|**API design discussion → small LLD problem: design a feature from an app**, with heavy focus on **concurrency handling**|Senior SDE round — also included core Java questions and behavioral questions in the same round|[Medium – Senior SDE Interview at Harness (Krishna Mundra)](https://medium.com/@23krishna.mundra/senior-sde-interview-at-harness-my-full-experience-questions-what-i-wish-i-knew-011eec393862)|
|4|**Render folder-structure text → HTML nested list** (see DSA table #13) — arguably an LLD/implementation task as much as a DSA one, since the interviewer explicitly wanted a more structural/extensible solution than direct DOM manipulation|SDE I, Peer Programming Round 2|[interviewexperiences.in – Harness SDE I Interview](https://interviewexperiences.in/experience/harness/harness-interview-experience-sde-i)|
|5|**"Interesting machine coding problem"** given by the India head in a 3rd/final round, alongside role/team/product discussion|US Principal Engineer loop|[Glassdoor – Harness Senior Software Engineer Interview Qs](https://www.glassdoor.com/Interview/Harness-Senior-Software-Engineer-Interview-Questions-EI_IE1828521.0,7_KO8,32.htm)|
|6|**"Some OOPs coding"** round, distinct from the 2 LeetCode rounds and 1 system-design round in a 4-round onsite loop|Generic Glassdoor-reported onsite loop structure|[Glassdoor – Harness Interview Questions & Experiences](https://www.glassdoor.com/Interview/Harness-Interview-Questions-E1828521.htm)|
|7|**Uber-style machine coding rounds** cited as representative prep material the candidate used|Senior Frontend Engineer, 8-round loop — candidate explicitly credits "Yomesh Gupta's content on Uber-style machine coding rounds" as directly useful prep, distinguishing it from plain LeetCode practice|[Medium – Harness Senior Frontend Engineer, 8 Rounds (Yashpreet Bathla)](https://medium.com/@yashpreetbathla/harness-senior-software-engineer-frontend-interview-experience-all-8-rounds-questions-a06f8347dda5)|

## 3. HLD / System Design problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**Design a simplified Shopify** (see LLD table #1) — the prompt blends HLD (multi-tenancy, architecture) and LLD (cart/order/inventory implementation details) in one open-ended spec, similar to the Salesforce/Stripe pattern of combined rounds|Senior SDE loop|[LeetCode Discuss – Harness Senior SDE Interview](https://leetcode.com/discuss/post/7560806/)|
|2|Generic **dedicated System Design round**, confirmed as a standard stage in Harness's process alongside 2 DSA rounds and a behavioral round|Reported structurally across multiple Glassdoor accounts|[Glassdoor – Harness Interview Questions & Experiences](https://www.glassdoor.com/Interview/Harness-Interview-Questions-E1828521.htm)|
|3|Design round explicitly framed as assessing **"ability to design scalable and efficient systems,"** covering architectural decisions, tradeoffs, and how you'd approach building a specific feature/service — with an emphasis on **distributed-systems understanding**|Generic guide description, consistent with confirmed candidate accounts|[Interview Query – Harness Software Engineer Interview Guide](https://www.interviewquery.com/interview-guides/harnessinc-software-engineer)|
|4|Interviewers value candidates who can **diagnose and troubleshoot complex problems in distributed computing environments**, and who understand **Harness's own product modules** (CI/CD, Cloud Cost Management, Feature Flags) — worth grounding a system-design answer in language that connects to these domains where natural|Prep-guide advice, not a specific asked question|[Interview Query – Harness Software Engineer Interview Guide](https://www.interviewquery.com/interview-guides/harnessinc-software-engineer)|

## 4. Recurring themes

- **Escalating/two-part rounds are common**, similar to what you saw at Stripe — several accounts describe an interviewer swapping in a harder follow-up once the first problem is solved cleanly (tree-burn problem swapped out when the candidate self-disclosed weakness on trees; recursive→DP escalation on Paint House). Being upfront about a weak area ("I'm not comfortable with trees, could we try something else?") is explicitly reported as accepted gracefully by interviewers here, not penalized.
- **Machine coding / "build something end-to-end" rounds are a house specialty**, especially from Senior SDE upward — a full e-commerce/inventory system, a Shopify clone, and an ordering+inventory system all appear as 60–90 minute build-from-scratch implementation rounds rather than a single-function coding problem. This is a different muscle than LeetCode grinding: multi-class design, correctness invariants (no negative inventory, no overselling), and pluggable abstractions (payment interface) under real time pressure.
- **Concurrency comes up specifically inside LLD rounds**, not just as a system-design buzzword — one candidate's "design a feature" LLD round centered almost entirely on concurrency handling.
- **Frontend-specific loops exist and can run long** (one confirmed 8-round Senior Frontend Engineer loop) — worth confirming with your recruiter exactly which track/role family you're being evaluated for, since round count and content varies more here than at some other companies in this set.
- **Explicit grading rubric elements repeatedly named by interviewers**: working code for sample test cases, dry-run with edge cases, and time/space complexity analysis — treat these three as mandatory closing steps for every DSA answer, not optional polish.
- **Process reliability is a recurring complaint** — several accounts (Glassdoor, Medium) report scheduling issues, ghosting after rounds, or missed feedback timelines. Not a prep concern, but worth setting expectations around communication turnaround.

## 5. Process / round-structure notes

- Typical loop: **Recruiter/HR screen (15–45 min)** → **Hiring Manager round** (background, behavioral, sometimes light technical) → **1–2 DSA rounds** (60 min each, live IDE, 1–2 problems, medium-to-hard) → **Machine Coding / LLD round** (60–90 min, especially Senior+) → **System Design round** (Senior+/Staff/Principal) → final round sometimes with a **regional/India head** covering machine coding + role/team/product discussion.
- Some loops back-to-back schedule **two problem-solving rounds on the same day** with only a ~1 hour buffer — worth being mentally prepared for a long single-day format.
- A Glassdoor mention of **"OA round have simple Q's mostly"** suggests an online-assessment stage exists for at least some tracks (possibly campus/intern hiring), but no candidate account gave a specific OA problem — treat this as a minor, low-difficulty gate rather than a major prep target.
- Glassdoor aggregate: **58.8% positive interview-experience rating**, difficulty **3.25/5**, average time-to-hire **~31 days** — moderate difficulty, slightly higher than Stripe's reported difficulty in this set, with process/communication cited as a bigger pain point than the technical bar itself.
- Interviewers explicitly warn against **jumping straight to the optimized solution without narrating the brute-force → optimization path** — signaling they want to see your reasoning process, not just the destination.

## 6. Sources scanned

- [interviewexperiences.in — Harness filter](https://interviewexperiences.in/company/harness) (5 detailed pages: Senior SDE ×2, SDE I, SDE Intern, Staff Software Engineer)
- LeetCode Discuss (Harness SE/Senior SDE/SDE-1 interview-experience threads)
- Glassdoor — Harness Senior Software Engineer & general interview questions/experiences
- GeeksforGeeks — Harness Interview Experience for Software Engineer 2024
- Medium — individual candidate write-ups (Krishna Mundra – Senior SDE; Yashpreet Bathla – Senior Frontend Engineer, 8 rounds)
- EnginEBogie — Harness Senior SDE machine-coding/DSA account
- Comparably, Interview Query, InterviewPrep — aggregator/prep-guide sources (flagged where content is guide-generated rather than a confirmed candidate account)

---

_Compiled July 27, 2026. No confirmed OA problem statements exist in the sources scanned — Harness's real gate is the live DSA + machine-coding rounds, so prep effort is best concentrated there._