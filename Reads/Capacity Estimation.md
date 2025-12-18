[Reference](https://www.youtube.com/watch?v=WZjSFNPS9Lo)
##### Cheatsheets

KB -> 1 thousand = 10^3
MB -> 1 million = 10^6
GB -> 1 billion = 10^9
TB -> 1 trillion = 10^12
PB -> 1 Quadrillion = 10^15

1 B = 8 bits
1 KB = 1024 B
1 MB = 1024 KB
1 GB = 1024 MB

 K * K = M
 M * M = G 

1 million/ day = 12 / sec
1 million/ day = 700 / min
1 million/ day = 42000 / hr

| Action                                       | Time   | Comparison |
| -------------------------------------------- | ------ | ---------- |
| Reading 1mb sequentially from memory         | 0.25ms |            |
| Reading 1mb sequentially from SSD            | 1ms    | 4x memory  |
| Reading 1mb sequentially from spinning disk  | 20ms   | 20x SSD    |
| Round trip network latency CA to Netherlands | 150ms  |            |

| Item                                                 | Size  |
| ---------------------------------------------------- | ----- |
| A two-hour movie                                     | 1gb   |
| A small book of plain text                           | 1mb   |
| A high-resolution photo                              | 1mb   |
| A medium-resolution image (or a site layout graphic) | 100kb |

|Metric|Order of Magnitude|
|---|---|
|Daily active users of major social networks|O(1b)|
|Hours of video streamed on Netflix per day|O(100m)|
|Google searches per second|O(100k)|
|Size of Wikipedia|O(100gb)|

**Storage Formula**

X Million(10^6) users * Y MB Space used/user (10^6) = XY TB (10^12)

***Note*** - Always round off like 960 becomes 1000, 86400 to 100000. 
##### What to Estimate

- **Traffic** - Total daily action users and how many request per user is doing. So we need to calculate daily requests per second.
- **Storage** - Total how much storage users going to use up every day , say they are creating posts or uploading images etc. 
- **RAM** - Data we are caching per day , say we are caching x number of recent tweets by user.  So if we need 100 GB cache and each machine can hold 10 GB cache, we need 10 machines
- **Latency** - Rough estimate p(95) - 500ms , p(99) - 550ms
- **Request a server can serve** - So we have 50 threads in a server , so each server can serve 100 requests (1/2 sec * 50 threads), so if we have to serve 100k req/sec it will be 100 machines. 
- **Trade-offs (CAP)** - Based on the requirement of the system , we choose the strategy. 

