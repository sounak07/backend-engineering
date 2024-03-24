## Change Data capture

Change Data capture is a form of data replication technique which is used to update or trigger certain events based on a change in the database. There is a source database and a target database/system where the data or the event gets sent. 

Basically CDC tracks the changes on a certain table in the source db and propagates that change to trigger certain events. The change can be propagated to multiple sources like another database, cache, to another service etc.

![alt text](/resources/Screenshot%202024-03-14%20at%2011.07.13%20PM.png)

How to set up CDC?
- Create an initial snapshot and load it into the target system.
- Identify the tables or rows we would want to track. 
- Enable the CDC on those tables
- Start the replication and track the changes

There are mainly 3 types of CDC approaches

- **Log based** - Changes in the db gets logged to a certain file called transactional logs. These transactional logs are then used to trigger changes to target systems.
- **Trigger based** - Changes to a certain table or row can used to enables some procedures in database called triggers. These triggers are then used to publish changes to target source.
- **Timestamp Based** - Timestamp columns like `updated_at` can be used to publish certain events as well. 

[Reference](https://newsletter.systemdesigncodex.com/p/intro-change-data-capture)

