
https://careers.nike.com/software-engineer-iii-itc/job/R-85807
https://careers.nike.com/senior-software-engineer-itc/job/R-87481

**Data Structures & Algorithms (DSA)**

- Find three triplets in an array that sum to a target value (3Sum problem).
- Approaches requested: Brute force, optimal approach using sorting/three-pointer technique, and a variation using a HashMap.

**Microservices & System Design**

- What are the major microservices design patterns (top three)?
- How do you prevent cascading failures in a chain of services (e.g., if a downstream service becomes slow or fails)? (Specifically regarding the Circuit Breaker pattern).
- What is Kafka, why is it used in microservices architecture, and how does it differ from a traditional message queue?
- When should you use microservices versus a monolithic architecture?
- How do you handle API versioning?
- How do you handle long-running APIs that might cause timeouts?
- Why use synchronous versus asynchronous communication in backend systems?
- How do you establish connectivity from an application to hosted services (databases and external APIs)?
- How do you design systems for reliability, scalability, and fault tolerance?

**Java & Spring Boot**

- What are the important Java versions, and which one are you using in your project?
- What is the difference between an Out of Memory error and a Stack Overflow error?
- What are heap memory and stack memory in the JVM?
- What are the top three or four most important concepts in Spring Boot?
- How does dependency injection work in Spring Boot?
- How does Spring Boot connect to databases and external services?
- How would you design a Spring Boot service that handles heavy processing without timing out?

- I**ntroduction:** Asked to introduce himself, cover his current role, day-to-day tasks, and his transition from a systems engineer to a software developer, including his backend experience.
- **Data Structures & Algorithms (DSA):** Asked to find the first and last occurrence of a target number in a sorted integer array using an optimized binary search approach.
- **Python:** A question related to lambda functions was asked (which the candidate skipped due to lack of experience).
- **Object-Oriented Programming (OOPS):** Concepts such as inheritance, polymorphism, and interfaces were discussed.
- **Backend & System Design:**
    - General backend concepts including microservices, controller-service-repository design patterns, and REST APIs.
    - Infrastructure questions involving Docker (how to deploy images) and Kubernetes (general high-level concepts and how pods restart themselves).


Same method as the Salesforce/DocuSign compilations. Sources: `interviewexperiences.in`, LeetCode Discuss, Glassdoor, CodingKaro, and interview-guide aggregators — mostly 2025–2026, India offices (Bangalore/Bengaluru). Coverage is **moderate**: better than DocuSign, thinner than Salesforce.

Nike engineering uses an **SDE 1 / SDE 2 / SDE 3 (also seen as "Software Engineer I/II")** ladder in India. Design-round depth scales with level, same pattern as elsewhere: SDE 1 loops lean DSA + light design, **SDE 2 and SDE 3 loops consistently include a dedicated system design round**, and SDE 3 loops sometimes run a second, more open-ended architecture discussion in addition.

---

## 1. LLD problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**Build a user-input form (React/JS) that filters out competitor brand names** (e.g., blocks "Adidas", "Puma" from a text field)|SDE 1 round, after explaining the HLD of a current work project; Nike-flavored twist on standard form-validation LLD|[LeetCode Discuss – Nike SDE 1 Interview Experience](https://leetcode.com/discuss/interview-experience/6739533/)|
|2|**Write a small server with a few APIs (Python + FastAPI)**, then discuss best practices for securing them|SDE 3 loop, Team 1 — framed as the "LLD" portion of a 90-minute HLD-first round|[LeetCode Discuss – Nike SDE 3 Interview Experience](https://leetcode.com/discuss/interview-experience/7318007/)|
|3|**HLD and LLD grilling on a Circuit Breaker Pattern implementation** the candidate had used in a past production system|SDE 2 round; interviewer went deep on the candidate's own resume-claimed pattern usage rather than a fresh prompt|[LeetCode Discuss – SDE 2 Interview Experience NIKE](https://leetcode.com/discuss/post/7284017/sde-2-interview-experience-nike-by-anony-kt3a/)|
|4|**Write controller logic on a whiteboard** for an MVC-style backend (Node.js/Express/MongoDB), covering route-controller design, DB integration, and API flow|Software Engineer I onsite, Bangalore|[LeetCode Discuss – SWE I Interview Experience (Bangalore Onsite)](https://leetcode.com/discuss/interview-experience/6629435/)|
|5|**Explain SOLID principles with real-world examples** from the candidate's own projects|SE-2 round, Engineering Manager interviewer; framed as an LLD/code-quality check rather than a fresh design prompt|[interviewexperiences.in – SE-2 Nike Interview Exp](https://interviewexperiences.in/experience/nike/se-2-nike-interview-exp)|

## 2. HLD / system design problem statements

|#|Problem|Round context|Source|
|---|---|---|---|
|1|**Design an online store for a retail brand like Nike**|SDE 3, Team 1, R1 — 90 min, explicitly "HLD-focused, minimal LLD," open-ended discussion on scalability, distributed systems, CI/CD, and a deep CAP-theorem consistency-vs-availability discussion around database scaling|[LeetCode Discuss / interviewexperiences.in – Nike SDE 3 Interview Experience](https://interviewexperiences.in/experience/nike/nike-sde-3-interview-experience)|
|2|**Design a backend system to ingest streaming concert-ticket bookings from multiple vendors and route data efficiently to multiple analytics teams**|SDE 3, Team 2, R2 — 60 min; interviewer explicitly noted this leans Data-Engineer-flavored but evaluated the same way; focus was scaling challenges and how to address them|[LeetCode Discuss / interviewexperiences.in – Nike SDE 3 Interview Experience](https://interviewexperiences.in/experience/nike/nike-sde-3-interview-experience)|
|3|**Design a cloud file-storage system with a sync feature** (Dropbox/Google-Drive-style)|SDE-2, Round 2 (dedicated System Design round), rated "Hard" by the candidate; paired with CI/CD questions|[interviewexperiences.in – SDE-2 Nike Experience](https://interviewexperiences.in/experience/nike/sde-2-nike-experience)|
|4|**API design for a high-scale system** (generic prompt, discussed as part of a resume deep-dive)|SDE-2, Round 3 (Techno-Managerial), second half after a resume deep-dive|[interviewexperiences.in – SDE-2 Nike Experience](https://interviewexperiences.in/experience/nike/sde-2-nike-experience)|
|5|**Design a Rate Limiter** — covered Token Bucket, Leaking Bucket, and Fixed Window Counter algorithms|SE-2, Round 3 (Technical & Design, run by the Engineering Manager)|[interviewexperiences.in – SE-2 Nike Interview Exp](https://interviewexperiences.in/experience/nike/se-2-nike-interview-exp)|
|6|**Scenario-based middleware question: route networking packets** — candidate solved it with a **Priority Queue**; explicitly framed by the interviewer as "not typical LeetCode style"|SDE 2 round, Bengaluru|[LeetCode Discuss – SDE 2 Interview Experience NIKE](https://leetcode.com/discuss/post/7284017/sde-2-interview-experience-nike-by-anony-kt3a/)|
|7|**"Design a scalable notification system for product drops"**|Cited as representative of Nike's retail-flavored system design prompts (e-commerce launch/traffic-spike handling)|[Dataford – NIKE Software Engineer Interview Guide](https://dataford.io/interview-guides/nike/software-engineer)|
|8|Generic **"system to design and break down"** — candidate was upfront about still building system-design depth and answered at a high, tech-stack-planning level|Software Engineer I onsite, Bangalore|[LeetCode Discuss – SWE I Interview Experience (Bangalore Onsite)](https://leetcode.com/discuss/interview-experience/6629435/)|
|9|Discussion of **"architectures I had used before"** in lieu of a fresh whiteboard prompt — a whiteboard-based, discussion-style round rather than live coding|Generic SWE loop, whiteboard format, no live coding|[Interview Query – Nike Software Engineer Interview Guide](https://www.interviewquery.com/guides/nike-software-engineer)|

## 3. Recurring themes

- **Retail/e-commerce-domain framing is common but not universal.** "Design an online store like Nike," "notification system for product drops," and the competitor-brand-name form filter are Nike-flavored; but rate limiters, cloud file sync, and packet routing are generic infra/systems questions asked at most companies — don't over-index on retail-specific prep at the expense of fundamentals.
- **HLD rounds frequently pivot into a deep CAP-theorem / consistency-vs-availability discussion once a design is on the board** — several accounts describe interviewers "challenging every design choice" around database scaling specifically. Worth rehearsing a crisp CAP tradeoff narrative you can drop into any design round, not just prepping the initial architecture.
- **LLD is often anchored to the candidate's own past project** (Circuit Breaker Pattern grilling, SOLID-principles-with-real-examples, "explain the HLD of your current project") rather than a fresh prompt — meaning your Raft AI architecture explanations (workflow engine, rule evaluator, EAV ingestion) are directly reusable material here, probably more so than at Salesforce/DocuSign where prompts are more often fresh whiteboard scenarios.
- **AWS and cloud-service tradeoffs (EC2 vs. Lambda, S3 vs. RDS, SQS/SNS for decoupling) show up as theory questions** attached to design rounds even when the candidate hasn't had hands-on production AWS experience — worth having conceptual answers ready even without deep hands-on time.
- Multiple accounts explicitly note Nike interviewers value **honesty about depth of experience** ("I was honest that I haven't had much hands-on AWS experience... questions were more theoretical") over bluffing — a good norm to carry into any round where you hit an edge of your knowledge.

## 4. Process / round-structure notes

- Typical loop: **Recruiter screen** → 1–2 **DSA/technical rounds** → 1 dedicated **System Design round** → **Manager/Hiring Manager round** (behavioral, "Why Nike?") → sometimes a **Director/Regional Manager round** (mostly resume-based, often just confirming an already-decided outcome).
- SDE 3 candidates report being interviewed for **two different teams under the same vertical simultaneously**, with meaningfully different round content between them — the exact design prompt is highly team-dependent.
- One candidate explicitly advises **keeping prep windows short (~2 days between rounds)** despite Nike giving generous scheduling gaps, to avoid over-thinking.
- Some loops are **whiteboard-only with no live coding** at all, evaluating clarity of approach over syntax — worth practicing explaining a design or algorithm out loud on paper, not just typing it.
- "Why Nike?" and brand-alignment questions recur across multiple levels — worth having a genuine, specific answer ready alongside the technical prep.

## 5. Sources scanned

- [interviewexperiences.in — Nike filter](https://interviewexperiences.in/company/nike)
- LeetCode Discuss (Nike SDE 1/2/3 and SWE I interview-experience threads)
- Glassdoor — NIKE Software Engineer interview questions
- CodingKaro — Nike interview experience aggregation
- Dataford, Interview Query — interview-guide aggregators (flagged where content is guide-generated rather than a confirmed candidate account)
- Note: Blind/teamblind.com searches for Nike-specific design threads mostly surfaced unrelated company threads; no additional Nike-specific design content found there beyond what's cited above.

---

_Compiled July 27, 2026. Coverage is moderate — better than DocuSign's, thinner than Salesforce's — treat as directional pattern-matching, not a guaranteed question bank._