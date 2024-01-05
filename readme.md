# ChatGPT Smart Home Assistant

## Description

This project uses the ChatGPT API to create a smart home assistant that interacts with home appliances through a serial port.
The system can control home lighting and fans based on environmental parameters, such as brightness, temperature.
It's a Python-based project that uses serial communication to control the IoT devices.

## Installation

### prerequisites

Python 3.11 or higher

### Install the required packages

* `conda install pyserial==3.5`

* `pip install serial==0.0.97`

* `pip install openai==1.6.1`

## Usage

1. Install the required Python libraries and configure settings for OpenAI and serial communication. Run the scripts, which will
   continuously monitor environmental parameters and interact with the OpenAI API for control instructions.

* `python OpenAI_Assistant_API.py`

  or
* `python OpenAI_Chat_Completion_API.py`

2. The OpenAI_Assistant_API.py is more advanced and can handle multiple commands in a single request.
3. The scripts control the corresponding home appliances based on instructions received from the OpenAI API.

Note:
* Ensure the OpenAI API key is correctly configured.
* Make sure the serial communication settings are correct, and the relevant hardware devices are connected.

### Comparison between OpenAI_Assistant_API and OpenAI_Chat_Completion_API

OpenAI_Assistant_API.py using the Assistant API, while OpenAI_Chat_Completion_API.py using the Chat Completions API.

In our OpenAI_Chat_Completion_API.py, we realize that using the Chat Completions API to control a fan based on temperature readings which from simulation platform.

In our OpenAI_Chat_Completion_API.py, we introduce a feature called "function calling" which allows the user to call a function in the assistant's code.
This feature is useful for IoT applications. In this project, we use function calling to control a fan based on temperature readings.
We believe that in the future, this feature will be widely used in IoT applications, not just for controlling a fan we use in this project, 
maybe also for controlling a light, a door, or even a car. And notice how all of these API calls are asynchronous operations;
this means we actually get async behavior in our code without the use of async libraries!

The most important thing is that the Assistant API introduces a new feature called "thread", which allows users to communicate with the assistant 
in a more natural way. For example, in the Chat Completions API, the user can only send one message at a time, and the assistant will only reply once.
But in the Assistant API, the user can send messages at multiple times in a thread, and the assistant will reply multiple times. What's more,
threads can be used to create multiple conversations with the same assistant. This feature is very useful for IoT applications in the future,
because it allows assistant to communicate with multiple devices at the same time, while the Chat Completions API can only communicate with one device at a time.

However, the Assistant API is still in beta, and it is not as stable as the Chat Completions API. Besides, we use the authentic API key in this project,
which means that the Assistant API is more expensive than the Chat Completions API, and the Assistant API has rate limits on the number of requests per minute and per day,
because OpenAI need rate limits to help protect against abuse/overuse of the API. So we can't use the Assistant API in a large scale application,
and we can't test too much data.

Despite this, we still think that the Assistant API has a more promising future in IoT applications. Threads is its strong advantage.
And in the future, OpenAI plan to release more OpenAI-built tools, and allow developer to provide their own tools on OpenAI's platform.

## Useful Links
https://platform.openai.com/docs/assistants/tools/function-calling
https://cookbook.openai.com/examples/assistants_api_overview_python
https://community.openai.com/t/assistant-api-message-no-answer-only-question/534101/3