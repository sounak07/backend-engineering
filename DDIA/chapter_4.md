## Chapter 4 - Encoding & Evolution

Encoding, also known as *Serialization* is a way to transform data from in-memory representation to sequence-of-bytes to be able to send via network protocols. 
JSON is a example of sequence-of-bytes since its default format is text and text is encoded as `utf-8` which is the standard encoding format. 
Each character of json is converted to its corresponding byte sequence and sent over the network. 

#### Language Specific Formats

Its quite convenient to use in-built language specific encoders but they come with a price that it becomes incompatible with other language formats. There are other issues too like in-built encoder being inefficient, the requirement to allow instantiation of arbitrary classes which can open gates to attackers etc. 

#### JSON, XML and Binary formats

JSON and XML are probably the most popular encoding formats. But there certain issues with them. 
- JSON and XML can't distinguish between numbers and string in the form of digits. JSON can between string and number but fail to do so in case of floating pointers leading to incorrect precision parsing. So this is something that should be kept in mind while dealing with floats in JSON.
- Both have support for unicode chars(human readable chars) but Binary strings can't be send via JSON or XML. They need to be to converted to base64 format which increases the size by 33%.

Despite these problems they are still quite popular among stakeholders for communicating among services.

##### Binary Encoding

Cases where communication only happens internally binary bytes could be a great way. Parsing JSON could be expensive when dealing with huge amount of data. So binary json encoders were brought in like MessagePack, ojson, bSON etc. 
Some of them just extended the data type to distinguish between floats and numbers and ability to send bstrings.
 They did not need any schema to describe them, just adding all the fields to the data to encode would do.

But these were not really widely adopted as compared to textual format because the size difference in the encoded data wasn't much. *Refer page 116 for example*

#### Thrift and Protocol Buffers

Thrift and Protocol Buffers are binary encoding libraries. They are schema based and needs a defined type of the data before it can encode it.

```cpp
struct Person {  
	1: required string userName,  
	2: optional i64 favoriteNumber, 
	3: optional list<string> interests
}

message Person {
	required string user_name= 1;
	optional int64  favorite_number = 2;
	repeated string interests= 3;

}
```

Both of them have code generators that generate class and methods in different langs to encode and decode the data. Thrift has 2 types of encoding methods namely Thrift Binary Protocol and Thrift CompactProtocol. Both are similar with a little difference on how they encode data which actually influences the size of the generated data. 
Similarly for Protocol buffers there is only one encoding method but its quite efficient.
*Refer Page 119 for details*

##### Field tags and Schema Evolution 

Now how do we add or remove fields or say any schema changes. The encoding if we see in the examples no where refers the name , its always the tag numbers that is being referred to. So updating field to a new name should not be an issue. We just need to make sure that the field tag is set correctly.

Similarly, to add a new field we need to add a new field tag in order it to work. So the code 
