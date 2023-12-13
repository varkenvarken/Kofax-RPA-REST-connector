# SPDX-License-Identifier: BSD-3-Clause-Modification

# restconnector (c) 2023 Michel Anders (varkenvarken)

# restconnector is a python based custom connector for Kofax RPA Robot workflows in version 11.5 or newer.
#
# This specific file defines a helper function to extract an attribute from a JSON serialized object.
# This is just a convenience function because at this moment the Robot workflow does not offer convenient
# facilities to work with JSON (it can serialize a complex variable to JSON but otherwise has no JSON 
# specific functionality)

from json import loads


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
        return obj[attr]

# a (very) minimalistic test
if __name__ == "__main__":
    input = """{
        "a": "aaa",
        "b": "bbb"
    }
    """
    assert ExtractJSON.extract(string=input, attr="a") == "aaa"
