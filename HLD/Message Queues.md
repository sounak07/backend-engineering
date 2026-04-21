
![Screenshot_2026-04-21_at_7.56.44_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_7.56.44_PM.png)![Screenshot_2026-04-21_at_7.57.10_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_7.57.10_PM.png)

- Decoupling means scaling and maintaining the services independently , may be some require more resources and some less

Scaling a message queues can be done my introducing partitions, and attaching a consumer or even consumer groups for higher throughput. 
Partition key is a major aspect since thats what decides which data goes where and downstream how its processed.  
A key which gives ordering might not give you distributions, we would want to avoid hot partitions. 


Poisoned messages leading to failures again and again could break the process since the poisoned message will always fail to be consumed. This might lead to introduce DLQ. 

![Screenshot_2026-04-21_at_8.16.31_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_8.16.31_PM.png)