
Same caveat as the LLD/HLD companion doc: **DocuSign has thinner, more US-skewed source coverage** than the Salesforce compilation — no dedicated `interviewexperiences.in` or `hiredvoices.com` pages were found. Data below spans LeetCode Discuss, Blind, Glassdoor, Medium, and GeeksforGeeks, roughly 2020–2026.

---

## 1. Online Assessment (OA) problem statements

|#|Problem|Notes|Source|
|---|---|---|---|
|—|_No fully-specified OA problem statements surfaced in the sources scanned._|Multiple sources confirm the OA is **HackerRank-hosted**, testing "algorithmic problems" and "logical reasoning," but none of the accounts found gave the literal prompt (unlike the Salesforce dataset, which had several verbatim OA questions).|[DesignGurus.io – DocuSign interview process overview](https://www.designgurus.io/answers/detail/what-is-docusign-interview-process-like)|

**What is confirmed about the OA format:**

- Hosted on **HackerRank**.
- Focuses on **data structures, algorithms, and logical reasoning** rather than domain-specific or custom problems (unlike Salesforce's occasional custom spam-classification-style prompts).
- Recommended prep list circulated by an interview-prep site (not confirmed as literally asked, but tagged as DocuSign-relevant on LeetCode): **Two Sum**, **Longest Substring Without Repeating Characters**, **Median of Two Sorted Arrays**, **Climbing Stairs**, **Longest Increasing Subsequence**, **Coin Change** — a fairly standard array/string/DP spread, skewed toward sliding-window and DP fundamentals. ([DesignGurus.io](https://www.designgurus.io/answers/detail/which-docusign-interview-questions-to-prepare-leetcode))

## 2. DSA (live technical) round problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**[Sort Colors](https://leetcode.com/problems/sort-colors/description/)**|SDE2, Technical Round 1 — full working code required, tested against multiple cases|[Medium – DocuSign SDE2 Interview Experience](https://medium.com/@anishacse2018/sde-2-docusign-interview-experience-59aa8460bcd0)|
|2|**[Minimum Cost to Make at Least One Valid Path in a Grid](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/description/)**|Same round as above|[Medium – DocuSign SDE2 Interview Experience](https://medium.com/@anishacse2018/sde-2-docusign-interview-experience-59aa8460bcd0)|
|3|**[Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)** (linked list)|Initial phone screen; candidate found and fixed their own edge-case bug live|[LeetCode Discuss – DocuSign Interview Experience (Seattle)](https://leetcode.com/discuss/interview-experience/562585/docusign-interview-experience/)|
|4|**[Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/description/)**|P4 offer loop — extra coding round added same-day after two positive design-round signals|[LeetCode Discuss – DocuSign P4 Offer](https://leetcode.com/discuss/interview-experience/6294868/Docusign-P4-offer/)|
|5|**[House Robber II](https://leetcode.com/problems/house-robber-ii/description/)** → extended live to **[House Robber III](https://leetcode.com/problems/house-robber-iii/description/)**|P4 offer loop; interviewer escalated to the harder tree-DP variant after the first was solved optimally|[LeetCode Discuss – DocuSign P4 Offer](https://leetcode.com/discuss/interview-experience/6294868/Docusign-P4-offer/)|
|6|**Hard DSA question combining heap + greedy, plus logic "riddles"** (exact prompt not disclosed)|Bengaluru campus loop, Feb 2026; candidate reported rejection at this round|[Glassdoor – DocuSign Interview Experience](https://www.glassdoor.com/Interview/Docusign-Interview-Questions-E307604.htm)|
|7|**3× LeetCode Hard problems** in one round ("basic LC hard, at least 3")|Anonymized Blind account, level/team unspecified; another commenter on the same thread reported the opposite — LC Easy only, "easiest interview I've ever given"|[Blind – "help what to expect in docusign interview"](https://www.teamblind.com/post/help-what-to-expect-in-docusign-interview-wpzml3ec)|
|8|**Shortest palindrome via character insertion** (`"bubble"` example)|Also listed in the LLD doc — string-manipulation coding question|[MockQuestions – DocuSign Interview Questions](https://www.mockquestions.com/company/DocuSign,+Inc./)|
|9|**Generic "string manipulation problem" + JSON-parsing-with-edge-cases task**|Aggregator-reported "representative" question set, not a single verified candidate account|[Dataford – DocuSign SWE Interview Guide](https://dataford.io/interview-guides/docusign/software-engineer)|

## 3. Pattern / difficulty summary

- **Difficulty is reported as highly team- and interviewer-dependent** — the same Blind thread had one candidate doing 3 LeetCode Hards and another doing all LeetCode Easy for what appears to be a comparable loop. Don't calibrate too hard off any single account; prepare for the harder end.
- Confirmed live-round problems skew toward: **array/matrix manipulation (Sort Colors, Spiral Matrix IV), DP (House Robber II→III escalation, grid pathfinding), and linked lists (Add Two Numbers)** — a fairly standard FAANG-style medium-to-hard spread rather than a distinctive "DocuSign house style" the way Salesforce's graph-heavy pattern was.
- **Interviewers escalate mid-round** at DocuSign too (House Robber II → III), same pattern seen at Salesforce (thread-safe scheduler → Observer → Kafka). Worth having a mental model of the "harder sequel" for common patterns (e.g., House Robber I → II → III; LRU → LFU) so an escalation doesn't catch you flat-footed.
- One data point (P4 offer) shows DocuSign sometimes runs **a bonus coding round same-day** if the first two rounds go well — worth being mentally prepared for a longer single-day loop than scheduled.

## 4. Process notes

- OA → 1–2 DSA technical rounds (LC medium, sometimes hard) → system design round (P4+) → behavioral/HM round, roughly matching the general structure confirmed across Glassdoor and Blind.
- Full working, tested code is expected in live rounds — several accounts mention the interviewer running test cases against submitted code, not just accepting a verbal walkthrough.
- Machine-coding rounds (see LLD doc) sometimes explicitly **don't require execution** — code is judged as-written, which is a different muscle than "make it pass the visible test cases."

## 5. Sources scanned

- LeetCode Discuss (DocuSign interview-experience threads)
- Blind / teamblind.com
- Glassdoor — DocuSign interview questions & experiences
- Medium — individual candidate write-up (Anishacse, SDE2)
- GeeksforGeeks — DocuSign intern interview experience (confirmed OA existed but didn't detail problems)
- MockQuestions.com, DesignGurus.io, Dataford, Interview Query — aggregator/prep-guide sources, flagged where content is "recommended prep" rather than a confirmed asked question

---

_Compiled July 27, 2026. Confidence is lower than the Salesforce compilation due to smaller sample size and heavier reliance on aggregator sites for OA specifics — treat this as a starting point, not a comprehensive bank._