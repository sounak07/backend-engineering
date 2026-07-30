[Read](https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes)

Lets say we are dealing with a system thats has multiple services and needs a chain of events to complete a task. how do we manage this?

One way could be to just await each call and make the next call while persisting state in the db with a orchestrator service, but what if that fails, who would catch the payment webhooks and update the next step. How do we backtrack and undo what we did since lets say inventory svc is down after payment charge. 

A **Saga pattern** can be used where we run a compensation for every action we did if they fail but it also has its down of things like what if the compensation request fails.

Another way could be **choreography** where each service is driven by a set of events emmitted by others and based on which topic the event came in (failure or next steps), we proceed. But what if we need to add a new flow or step in the middle, we need to change the contracts of neighbouring services, which is not a trivial but common things. It can useful some less complex steps with not a lot changes happening.

**Orchestration** using durable execution engines like Temporal. 

```java
const {
    processPayment,
    reserveInventory,
    shipOrder,
    sendConfirmationEmail,
    refundPayment
} = proxyActivities<Activities>({
    startToCloseTimeout: '5 minute',
    retry: {
        maximumAttempts: 3,
    }
});

async function myWorkflow(input: Order): Promise<OrderResult> {
    const paymentResult = await processPayment(input);

    if(paymentResult.success) {
        const inventoryResult = await reserveInventory(input);

        if(inventoryResult.success) {
            await shipOrder(input);
            await sendConfirmationEmail(input);
            return { success: true };
        } else {
            await refundPayment(input);
            return { success: false, error: "Inventory reservation failed" };
        }
    } else {
        return { success: false, error: "Payment failed" };
    }
}
```

 Temporal has two main building blocks: **Workflows** and **Activities**. A **Workflow** contains the business logic and orchestration, but it must be **deterministic**, meaning that given the same sequence of events, it should always produce the same execution. Because of this, workflows cannot directly perform external operations like API calls, database queries, sending emails, reading the current time, or generating random numbers. Instead, all such side effects are delegated to **Activities**. Activities perform the actual work such as fetching data, calling external services, writing to databases, or sending emails. Since Activities may be retried automatically if a worker crashes or times out, they should be **idempotent** to avoid duplicate side effects.

  
![Screenshot_2026-07-25_at_5.27.06_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-07-25_at_5.27.06_PM.png)

Temporal persists every important event in a workflow's lifecycle as an **Event History**, including activity scheduling, completion, timer events, signals, etc. During execution, a **Workflow Worker** runs the workflow code until it reaches an Activity. Rather than executing it directly, it schedules an Activity Task. An **Activity Worker** picks up the task, performs the external work, reports the result back to the Temporal Server, and the server appends the completion event to the workflow's history. The Workflow Worker then resumes execution using that recorded result. If a Workflow Worker crashes midway, another worker simply reloads the workflow's event history and **replays the workflow code from the beginning**. Whenever it encounters an Activity that has already completed, it doesn't execute it again—instead, Temporal returns the previously recorded result from the event history. This replay mechanism is exactly why workflow code must be deterministic.

Temporal also supports **Signals**, which allow external events such as human approvals, payment confirmations, or user actions to interact with a running workflow. Since the workflow's state is durably stored in the event history, the workflow can remain paused for hours, days, or even months without consuming compute resources. When a Signal arrives, it is recorded as a new event in the history, a Workflow Worker picks up the execution again, replays the workflow to reconstruct its state, and continues execution from the point where it was waiting. This enables long-running, fault-tolerant workflows without requiring any process or thread to stay alive continuously.

```python
Workflow Code
      │
      ▼
Activity Scheduled
      │
      ▼
Activity Worker executes
      │
      ▼
Result stored in Event History
      │
      ▼
Workflow replayed
      │
      ▼
Next Activity...
```
AWS Step functions, GCP Cloud workflows are another example for similar functions.

**How do u handle updates for workflow?**

We can use workflow versioning. The patched method in workflow helps in determining the path we need to take during execution. 

![Screenshot_2026-07-25_at_5.48.32_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-07-25_at_5.48.32_PM.png)

**"How do we keep the workflow state size in check?"**

There's a few aspects of the solution: first, we should try to minimize the size of the activity input and results. If you can pass an identifier which can be looked up in a database or external system rather than a huge payload, you can do that.

Second, we can periodically snapshot a long-running workflow and hand off to a fresh copy of itself. Temporal calls this "Continue-as-New". Instead of dragging the full event history along, you capture the workflow's current state, start a new run with an empty history, and seed it with just that state so it picks up right where the old one left off. The new run starts at the current position, not back at step 1. This


**How do u ensure the activity is run exactly once?**

Lets say an activity ran but the update never reaches the server to update the history, a retry for a event like payment could be an issue. Storing a key that is unique in db after execution and checking if that exists is a common way to do it. 
But its still not atomic, lets say server failed after executing but before updating. So a better approach could be to have in_progress and completed flags for before and after signals. Only for cases we find in_progress, we need some reconciliation with payment gateway.


**How to use this in interviews**

- Payment systems can use this since it involves multiple steps in them
- Don't use in simple async processing, high frequency low value actions

