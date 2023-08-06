# Getting Started with Multiple Responses Test API

## Getting Started

### Install the Package

The package is compatible with Python versions `2 >=2.7.9` and `3 >=3.4`.
Install the package from PyPi using the following pip command:

```python
pip install altest-multiple-res==2.0.0
```

You can also view the package at:
https://pypi.python.org/pypi/altest-multiple-res

### Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 3** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 0** |

The API client can be initialized as follows:

```python
from multipleresponsestestapi.multipleresponsestestapi_client import MultipleresponsestestapiClient

client = MultipleresponsestestapiClient()
```

### Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `nose` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
nosetests
```

## Client Class Documentation

### Multiple Responses Test APIClient

The gateway for the SDK. This class acts as a factory for the Controllers and also holds the configuration of the SDK.

### Controllers

| Name | Description |
|  --- | --- |
| send_messages | Provides access to SendMessagesController |

## API Reference

### List of APIs

* [Send Messages](#send-messages)

### Send Messages

#### Overview

##### Get instance

An instance of the `SendMessagesController` class can be accessed from the API Client.

```
send_messages_controller = client.send_messages
```

#### Multiple Responses Without Range

:information_source: **Note** This endpoint does not require authentication.

```python
def multiple_responses_without_range(self)
```

##### Response Type

[`List of MultipleMessageModel`](#multiple-message-model)

##### Example Usage

```python
result = send_messages_controller.multiple_responses_without_range()
```

##### Example Response *(as JSON)*

```json
[
  {
    "from": "Littlecab",
    "to": [
      "+254700000001",
      "+254700000002",
      "+254700000003"
    ],
    "text": "Welcome to our Little world."
  }
]
```

##### Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 404 | Not found | [`FailureResponseModelException`](#failure-response-model) |
| 500 | Internal server error | [`FailureResponseModelException`](#failure-response-model) |
| Default | Continue | [`SuccessResponseModelException`](#success-response-model) |

#### Multiple Responses With Range

:information_source: **Note** This endpoint does not require authentication.

```python
def multiple_responses_with_range(self)
```

##### Response Type

[`List of MultipleMessageModel`](#multiple-message-model)

##### Example Usage

```python
result = send_messages_controller.multiple_responses_with_range()
```

##### Example Response *(as JSON)*

```json
[
  {
    "from": "Littlecab",
    "to": [
      "+254700000001",
      "+254700000002",
      "+254700000003"
    ],
    "text": "Welcome to our Little world."
  }
]
```

##### Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 404 | Not found | [`FailureResponseModelException`](#failure-response-model) |
| 500 | Internal server error | [`FailureResponseModelException`](#failure-response-model) |
| Default | Continue | [`SuccessResponseModelException`](#success-response-model) |

## Model Reference

### Structures

* [Single Message Model](#single-message-model)
* [Multiple Message Model](#multiple-message-model)
* [Id Type](#id-type)
* [Reason](#reason)

#### Single Message Model

Any payload to send a single message should be in this format

##### Class Name

`SingleMessageModel`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mfrom` | `string` | Optional | The SMS header you would like to use, these should be registered under the account being managed by the API KEY used. |
| `to` | `string` | Optional | Mobile number of the recipient of the message with the country code included |
| `text` | `string` | Optional | Your message to the recipient user |

##### Example (as JSON)

```json
{
  "from": null,
  "to": null,
  "text": null
}
```

#### Multiple Message Model

Any payload to send a message to multiple numbers should be in this format

##### Class Name

`MultipleMessageModel`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mfrom` | `string` | Optional | The SMS header you would like to use, these should be registered under the account being managed by the API KEY used. |
| `to` | `List of string` | Optional | List of mobile numbers in the international format receiving your message |
| `text` | `string` | Optional | Your message to the recipient user |

##### Example (as JSON)

```json
{
  "from": null,
  "to": null,
  "text": null
}
```

#### Id Type

##### Class Name

`IdType`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | `string` |  | - |
| `channel_id` | `string` | Optional | - |
| `video_id` | `string` | Optional | - |

##### Example (as JSON)

```json
{
  "kind": "kind8",
  "channelId": null,
  "videoId": null
}
```

#### Reason

Reason of the failure

##### Class Name

`Reason`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `name` | `string` | Optional | Name of the error generated |
| `message` | `string` | Optional | Literal description of the error generated |

##### Example (as JSON)

```json
{
  "name": null,
  "message": null
}
```

### Exceptions

* [Success Response Model](#success-response-model)
* [Failure Response Model](#failure-response-model)

#### Success Response Model

Any successful response will have this format

##### Class Name

`SuccessResponseModelException`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `status` | `bool` | Optional | Status of the response, when unsuccessful this value will be `false` |
| `message` | `string` | Optional | Successful message to your previous request. Messages:<br><br>* `Request sent to queue` => "Your messages are being processed for delivery to your different recipients" |

##### Example (as JSON)

```json
{
  "status": null,
  "message": null
}
```

#### Failure Response Model

Any unsuccessful response with have this format

##### Class Name

`FailureResponseModelException`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `status` | `bool` | Optional | Status of the response, when successful this value will be `true` |
| `reason` | [`Reason`](#reason) | Optional | Reason of the failure |

##### Example (as JSON)

```json
{
  "status": null,
  "reason": null
}
```

## Utility Classes Documentation

### ApiHelper

A utility class for processing API Calls. Also contains classes for supporting standard datetime formats.

#### Methods

| Name | Description |
|  --- | --- |
| json_deserialize | Deserializes a JSON string to a Python dictionary. |

#### Classes

| Name | Description |
|  --- | --- |
| HttpDateTime | A wrapper for datetime to support HTTP date format. |
| UnixDateTime | A wrapper for datetime to support Unix date format. |
| RFC3339DateTime | A wrapper for datetime to support RFC3339 format. |

## Common Code Documentation

### HttpResponse

Http response received.

#### Parameters

| Name | Type | Description |
|  --- | --- | --- |
| status_code | int | The status code returned by the server. |
| reason_phrase | str | The reason phrase returned by the server. |
| headers | dict | Response headers. |
| text | str | Response body. |
| request | HttpRequest | The request that resulted in this response. |

### HttpRequest

Represents a single Http Request.

#### Parameters

| Name | Type | Tag | Description |
|  --- | --- | --- | --- |
| http_method | HttpMethodEnum |  | The HTTP method of the request. |
| query_url | str |  | The endpoint URL for the API request. |
| headers | dict | optional | Request headers. |
| query_parameters | dict | optional | Query parameters to add in the URL. |
| parameters | dict &#124; str | optional | Request body, either as a serialized string or else a list of parameters to form encode. |
| files | dict | optional | Files to be sent with the request. |

