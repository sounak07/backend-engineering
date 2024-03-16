#### CPP STL
##### Vector

```cpp
vector<int> vec;
vec.push_back(1);
vec.emplace_back(2); // much more efficient and faster than above

vector<pair<int,int>> vect;

vect.push_back({1,2});
vect.emplace_back(1,2);
```

1. Vectors can be extended Dynamically.
2. A linkedList in maintained internally for a vector.

```cpp
vector<int> v;

// v.begin() points to the memory of the first element
vector<int>::iterator it = v.begin()

cout<< it  // prints the memory address
cout<< *(it) // prints the value

// v.end() points to the memory post the last element of vector
vector<int>::iterator it = v.end()

// points to the last element of vector
v.back()

for(vector<int>::iterator it = v.begin(); it != v.end(); it++)
{
	cout<< *(it)<< " ";
}

for(auto it = v.begin(); it != v.end(); it++)
{
	cout<< *(it)<< " ";
}

// Prints value
// auto is set on the int type vector not an iterator 
for(auto it : v)
{
	cout<< it << " ";
}


// erase function

// {10, 20, 35, 40}
v.erase(v.begin()+1);
// {10, 35, 40}

// {10, 20, 35, 40}
v.erase(v.begin()+1, v.begin()+3); 
// {10, 40} -> End is not included -> [start, end)

// insert function

vector<int> v(2, 100) // {100, 100}
vector<int> v(v.begin(), 10) // {10 , 100, 100}
vector<int> v(v.begin()+1, 10) // {10 , 20, 100, 100}

v.pop_back() // {10, 20, 100}
v.size() // 3 

```

#### Set

Stores elements in sorted manner no matter how its inserted. 
Takes `log n` time to do all operations insert , delete , find etc

```cpp

set<int> s;

s.insert(1); // {1}
s.emplace(2); // {1, 2}
s.insert(3); // {1, 2, 3}
s.insert(3); // {1, 2, 3}

auto it = s.find(3); 

auto it = s.find(5); // return s.end() since not found

// {1, 2, 3}
s.erase(3) // {1, 2} 

// {1, 2, 3, 4, 5}
auto it1 = s.find(2);
auto it2 = s.find(4);

// {1, 2, 3, 4, 5}

int cnt = s.count(1) // 1 
int cnt = s.count(8) // 0

s.erase(it1, it2); // {1, 4, 5} -> 4 not included [first, end)

```

#### Maps

- Maps store unique keys in sorted manner. 
- Stored in sorted order of key

```cpp
map<int, int> map;
map<int , pair<int, int>> map2;
map<pair<int, int> , int> map2;

map[1] = 2; // {(1, 2)}
map.emplace({4,5}); // {(1, 2), {4, 5}}
map.insert({3,4}); // {(1, 2), {4, 5}, (3, 4)}


for(auto it : map)
{
	cout<< it.first << " " << it.second;
}

// {(1, 2), {4, 5}, (3, 4)}

cout << map[1] // 2
cout << map[4] // 5
cout << map[7] // null

// {(1, 2), {4, 5}, (3, 4)}
auto it = map.find(1)
cout<< *(it).second // 2

auto it = map.find(8) // Not found -> map.end()

```

#### Sort() in STL

Sorts list or vector in increasing order

```cpp

bool comp(pair<int, int> p1, pair<int, int> p2){
	if (p1.second < p2.second) return true;
	if (p1.second > p2.second) return false;

	// it will be here if they are same
	if (p1.first > p2.first) return true;
	return false;
}

// sort an array
sort(a, a+n);

//sort a vector
sort(v.begin(), v.end());

// sort in decreasing order 
sort(a, a+n, greater<int>);

// sort in custom manner

pair<int, int>a[] = {{1,2}, {4,1}, {2,1}}

sort(a, a+n, comp); //comparator function -> returns a bool 

```