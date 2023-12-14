# REST Connector

In [Kofax RPA version 11.5](https://docshield.kofax.com/Portal/Products/en_US/RPA/11.5.0-nlfihq5gwr/RPA.htm)
we can run Robots stand-alone and seldomly have to fall back on functionality provided by Basic Engine robots.

Calling REST services however is not yet an option that is natively supported in the Robot workflow (it is in the Basic Engine Robot workflow),
and working with JSON strings is also limited, which is inconvenient when interacting with REST services.

However, Kofax RPA provides ways to add custom steps to the robot using external connectors written in any language,
and this Python REST connector aims to bridge the gap in functionality for now.

It provides a single custom step with two possible actions: performing a REST call and a helper action to extract
the value of an attribute in a JSON serialized object.

Note: quite extensive comments are provided in the python sources and be aware that this connector was not exhaustively tested,
so use it with great care.

## Prerequisites

On all machines where this connector will be used, python (version 3.11 or newer) should be present,
and the `requests` package should be installed.
Be aware that the machine where the robot is running depends on the situation:

- in the Design Studio this will be on the same machine as the Design Studio itself,
- when running on a RoboServer that will be on any RoboServer in the cluster the Robot might run,
- when using the connector an a non-local device, this will be on that device, i.e. the remote machine.

## Building

The connector should placed in an RPA project as a .zip file with a .connector extension.

If you change anything in the python files, makes sure to update the manifest.json accordingly and then:

- zip the python files along with the manifest (make sure they end up at the toplevel, i.e. not inside an additional folder)
- rename the .zip to .connector

in a bash shell this can be done in one go:

```bash
zip restconnector.connector *.py manifest.json
```


## Installation

Simply copy the file `restconnector.connector` to the Library folder of the project you want to use it in.

## Usage

The connector currently provided two actions:

- `call`, that will call a REST service and return the result of the call, and
- `extract`, a helper action that takes a JSON serialized object and an attribute name and returns the value of that attribute
  
### call

Has the following parameters:

- `endpoint`  the URL of the REST service
- `method`    optional, the method to use in the call, defaults to POST
- `header1`   optional, header to pass along with the call
- `header2`   idem
- `header3`   idem
- `header4`   idem
- `header5`   idem
- `body`      optional, the body to pass (typically a JSON serialized object)

It returns the body of the response on success or a JSON string containing an error attribute if something went wrong.

### extract

Has the following parameters

- `json`      a JSON serialized object
- `attr`      the name of an attribute

