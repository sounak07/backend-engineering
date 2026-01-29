#### Killing Transactions in databases

**Deadlock**

![Screenshot_2026-01-30_at_12.05.43_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.05.43_AM.png)

### 🛠️ How databases deal with this

**MySQL**

- Actively detects cycles(the circular dependency basically) in lock dependencies
- Automatically **kills one transaction**
- Releases its locks so the other can continue

**PostgreSQL**

- Uses a more **optimistic approach**
- Uses predicate locks and lock timeouts
- Allows transactions to proceed
- At commit time, if a conflict is detected:
    - One transaction commits
    - The other is rolled back

Different strategies, same goal: **ensure the system keeps moving**.

**Dining Philosophers — the timeless analogy**

![Screenshot_2026-01-30_at_12.22.47_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.22.47_AM.png)

