# json_key_press
Compress and decompress JSON keys given a data schema for minimal data size during transport.

## Example
Say, we have the following object we want to transfer via a REST API:
```json
{
    "order": {
        "order_uuid": "7234723467",
        "amount": 50,
        "category": "apple"
    },
    "amount": 10,
    "customer_name": "Harald"
}
```

Since the object follows a strict schema (e.g. no uuids as keys), the keys 
can be shortened to just 
a single character. Also the value for "order.category" has a limited value
range and can be seen as an enum. If we take just these two properties of the data into
consideration, the length of the JSON string can be reduced from 115 to 69 
Bytes, which is a saving of 40%, nice. The object with the shortened keys 
looks like this:
```json
{
    "A": {
        "A": "7234723467",
        "C": 50,
        "B": "a"
    },
    "B": 10,
    "C": "Harald"
}
```

The schema that is used for compression and decompression of the keys and the 
enum are specified in Python code:
```python
from json_key_press import CompressibleObject, JSONKeyPress

class OrderCategory(CompressibleObject):
    def compress(self, o):
        return {'apple': 'a', 'peach': 'p', 'cherry': 'c'}[o]

    def decompress(self, o):
        return {'a': 'apple', 'p': 'peach', 'c': 'cherry'}[o]

schema = {
    "order": {
        "order_uuid": int,
        "category": OrderCategory,
        "amount": int,
    },
    "amount": int,
    "customer_name": str,
}

t = JSONKeyPress(schema)
```

In combination with gzip compression, the key shortening is a good first step to 
reduce the size of the object during transfer, e.g. over an expensive or limited 
network.

For some other ways to use the class JSONKeyPress see the example in the test file.

