## Capacity Estimation

[Reference](https://www.youtube.com/watch?v=WZjSFNPS9Lo)

Always round off like 960 becomes 1000, 86400 to 100000. 
Try to calculate :
- No of read and writes. 
- No of transactions 
- Network bandwidth 
- No of requests per server 
- No of servers , RAM(mostly for cache) and Storage required  (IMP)

Explain the tradeoffs using CAP and start designing. 

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

**Storage Formula**

X Million(10^6) users * Y MB Space used/user (10^6) = XY TB (10^12)

