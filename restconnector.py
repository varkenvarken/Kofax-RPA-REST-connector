# SPDX-License-Identifier: BSD-3-Clause-Modification

# restconnector (c) 2023 Michel Anders (varkenvarken)

# restconnector is a python based custom connector for Kofax RPA Robot workflows in version 11.5 or newer.
#
# It defines a custom step that allows to POST to a REST service on a given endpoint (URL) with customizable
# headers and an arbitrary body (typically JSON serialized data) and returns any response as a string (again,
# typically JSON serialized data). Any error that occurs during the request is return as a JSON object with a
# single "error" attribute whose value is the error text.
# This file is the Python implementation with some test code; The file manifest.json defines the interface of
# of the custom step that can be used in a Robot workflow.
# See the file Readme.md for more details.

# we ignore any import errors that may occur when trying to import the requests package
# that way any function that will use this module will throw an exception that indicates
# that requests could no be found, which makes it a bit clearer for user of this connector
# that the python environment is not as it should be.
# (Note that this doesn't guard against python not being installed at all)
try:
    import requests
except ImportError:
    pass


class RESTwebservice:
    @staticmethod
    def _split(cs: str):
        """
        Splits a string containing a colon into two parts: key and value.

        Parameters:
        - cs (str): The input string to be split.

        Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing two elements:
            1. The key (left part of the string after stripping whitespaces), or None if the input is invalid.
            2. The value (right part of the string after stripping whitespaces), or None if the input is invalid.
        """
        if cs is None or cs.strip() == "":
            return None, None
        try:
            cs = cs.strip()
            colon_index = cs.index(":")
            return cs[:colon_index].strip(), cs[colon_index + 1 :].strip()
        except ValueError:
            return None, None

    @staticmethod
    def call(*, endpoint: str, method: str, headers: dict, body: str):
        """
        Make a POST request to the specified endpoint with the provided headers and body.

        Parameters:
        - endpoint (str): The URL endpoint for the request.
        - method (str): a valid HTTP method (like POST, GET, PUT or DELETE).
        - headers (dict): A dictionary containing HTTP headers for the request.
        - body (str): The request body as a string.

        Returns:
        Union[dict, str]: If the request is successful (status code 2xx), returns the response as a JSON dictionary.
        If the request is not successful, returns an error message JSON string.
        If an exception occurs during the request, returns an error message JSON string.

        Note:
        The error message JSON string format: '{"error": <error_details>, "info": <additional text>}'
        """
        try:
            # Make the request, will raise an exception if the method is not known by requests
            method = method.lower()
            if hasattr(requests, method):
                response = getattr(requests, method)(
                    endpoint, headers=headers, data=body
                )
            else:
                raise AttributeError(f"unknown method '{method}'")
            # Check if the request was successful (status code 2xx)
            if response.ok:
                return response.json()  # Return the response as JSON
            else:
                return (
                    f'{{"error": {response.status_code}, "info": "{response.reason}"}}'
                )

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return f'{{"error": "{str(e)}"}}'

    @staticmethod
    def call2(
        *,
        endpoint: str,
        method: str = "POST",
        header1: str = None,
        header2: str = None,
        header3: str = None,
        header4: str = None,
        header5: str = None,
        body: str = None,
    ):
        """
        Make a POST request to the specified endpoint with the provided headers and body.

        Parameters:
        - endpoint (str): The URL endpoint for the POST request.
        - method (str): a valid HTTP method (like POST, GET, PUT or DELETE).
        - header1, header2, header3, header4, header5 (str, optional): Strings containing headers in the format "key: value".
        These headers will be added to the request if provided.
        - body (str): The request body as a string.

        Returns:
        Union[dict, str]: If the request is successful (status code 2xx), returns the response as a JSON dictionary.
        If the request is not successful, returns an error message JSON string.
        If an exception occurs during the request, returns an error message JSON string.

        Note:
        The error message JSON string format: '{"error": <error_details>, "info": <additional text>}'

        Note2:
        This function internally calls RESTwebservice.call() but is provided because RPA connectors can only work
        with scalar arguments, so there is no way to pass a dictionary from a Robot workflow to a connector. In fact,
        a Robot does not even have the concept of a dictionary, so anything you pass to or from a connector is either
        a string or an integer.
        """
        headers = {}
        k, v = RESTwebservice._split(header1)
        if k is not None:
            headers[k] = v
        k, v = RESTwebservice._split(header2)
        if k is not None:
            headers[k] = v
        k, v = RESTwebservice._split(header3)
        if k is not None:
            headers[k] = v
        k, v = RESTwebservice._split(header4)
        if k is not None:
            headers[k] = v
        k, v = RESTwebservice._split(header5)
        if k is not None:
            headers[k] = v
        
        if method == "":
            method = "POST"
            
        return RESTwebservice.call(
            endpoint=endpoint, method=method, headers=headers, body=body
        )


# The following code is just test code.
# It is not used by the connector
if __name__ == "__main__":
    from os import environ

    endpoint = "https://jsonplaceholder.typicode.com/posts"
    header1 = "Content-Type: application/json"
    body = """{
        "title": "foo",
        "body": "bar",
        "userId": 1
    }"""
    print(RESTwebservice.call2(endpoint=endpoint, header1=header1, body=body))

    endpoint = "https://jsonplaceholder.typicode.com/posts/1"
    print(RESTwebservice.call2(endpoint=endpoint, method="GET"))
