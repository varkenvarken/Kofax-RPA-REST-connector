# SPDX-License-Identifier: BSD-3-Clause-Modification

# restconnector (c) 2023 Michel Anders (varkenvarken)

# restconnector is a python based custom connector for Kofax RPA Robot workflows in version 11.5 or newer.
#
# This specific file defines a helper function to extract an attribute from a JSON serialized object.
# This is just a convenience function because at this moment the Robot workflow does not offer convenient
# facilities to work with JSON (it can serialize a complex variable to JSON but otherwise has no JSON 
# specific functionality)

from json import loads, dumps

from jsonpath_ng.ext import parse

class ExtractJSON:
    @staticmethod
    def extract(*, string: str, attr: str):
        """
        Extracts a specified attribute from a JSON-formatted string.

        Parameters:
        - string (str): A JSON-formatted string to extract the attribute from.
        - attr (str): The attribute key to extract from the JSON object.

        Returns:
        - any: The value associated with the specified attribute in the JSON object.

        Raises:
        - JSONDecodeError: If the input string is not a valid JSON.
        - KeyError: If the specified attribute is not present in the JSON object.
        """
        obj = loads(string)
        if type(obj) == dict:
            return str(obj[attr])
        return str(obj[int(attr)])
        
    @staticmethod
    def extract_with_path(string:str, path:str):
        """
        Extracts JSON data from a given string using a JSONPath expression.

        Parameters:
        - string (str): The input string containing JSON data.
        - path (str): The JSONPath expression to specify the data to be extracted.

        Returns:
        str: A JSON-formatted string representing the extracted data.

        Example:
        >>> input_string = '{"name": "John", "age": 30, "city": "New York"}'
        >>> json_path = '$.name'
        >>> result = extract_with_path(input_string, json_path)
        >>> print(result)
        '["John"]'
        """
        path = parse(path)
        return dumps([f.value for f in path.find(loads(string))])
    
# a (very) minimalistic set of tests 
if __name__ == "__main__":

    input = """{
        "a": "aaa",
        "b": "bbb"
    }
    """
    assert ExtractJSON.extract(string=input, attr="a") == "aaa"

    input2 = """[1,2,3,4]"""
    assert ExtractJSON.extract(string=input2, attr="2") == "3"

    JSON = '''{
    "store": {
        "book": [
        {
            "category": "reference",
            "author": "Nigel Rees",
            "title": "Sayings of the Century",
            "price": 8.95
        },
        {
            "category": "fiction",
            "author": "Herman Melville",
            "title": "Moby Dick",
            "isbn": "0-553-21311-3",
            "price": 8.99
        },
        {
            "category": "fiction",
            "author": "J.R.R. Tolkien",
            "title": "The Lord of the Rings",
            "isbn": "0-395-19395-8",
            "price": 22.99
        }
        ],
        "bicycle": {
        "color": "red",
        "price": 19.95
        }
    },
    "expensive": 10
    }'''

    assert ExtractJSON.extract_with_path(string=JSON, path="$.store.book[*].author") == '["Nigel Rees", "Herman Melville", "J.R.R. Tolkien"]'
