# Notice how all of these API calls are asynchronous operations;
# this means we actually get async behavior in our code without the use of async libraries!

# Threads can be used to create multiple conversations with the same assistant.
import json
import time

from openai import OpenAI

from coordinator import *


def create_thread_and_run(user_input):
    api_thread = client.beta.threads.create()
    run = submit_message(HOME_ASSISTANT_ID, api_thread, user_input)
    return api_thread, run


def submit_message(assistant_id, api_thread, user_message):
    client.beta.threads.messages.create(
        thread_id = api_thread.id, role = "user", content = user_message
    )
    return client.beta.threads.runs.create(
        thread_id = api_thread.id,
        assistant_id = assistant_id,
    )


def wait_on_run(run, api_thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id = api_thread.id,
            run_id = run.id,
        )  # retrieve the run status
        time.sleep(0.5)
        print('run.status: ', run.status)
    return run


def pretty_print(messages):
    print("# Messages")
    count = 0
    for message in messages:
        if message.role == "user":
            count += 1
            print('* conversation {}'.format(count))
        print(f"{message.role}: {message.content[0].text.value}")


control_fan_json = {
    "name": "control_fan",
    "description": "When temperature is high, key_status will be 'ON', so set the fan on,"
                   "when temperature is low, key_status will be 'OFF', so set the fan off.",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {"type": "string",
                        "description": "The next status of fan, only ON or OFF is allowed."}
        },
        "required": ["command"]
    }
}

control_lamp_json = {
    "name": "control_lamp",
    "description": "When brightness is high, key_status will be 'OFF', so set the fan off,"
                   "when brightness is low, key_status will be 'ON', so set the fan on."
                   "The suitable brightness range is approximately between 1200 and 1500."
                   "So, when the brightness is higher than 1700, you should turn off the lamp."
                   "So, when the brightness is lower than 1000, you should turn on the lamp.",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {"type": "string",
                        "description": "The next status of lamp, only ON or OFF is allowed."}
        },
        "required": ["command"]
    }
}

with open('OpenAI_API.json', 'r') as f:
    api_key = json.load(f)['assistant_api']['api_key']

client = OpenAI(
    api_key = api_key
)

assistant = client.beta.assistants.create(
    name = "Home Assistant",
    instructions = "You are a smart home assistant,"
                   "and you can control the lamp based on the current brightness to make the homeowner feel comfortable.",
    tools = [{"type": "code_interpreter"},
             {"type": "retrieval"},
             {"type": "function", "function": control_fan_json},
             {"type": "function", "function": control_lamp_json}],
    model = "gpt-3.5-turbo-1106"
)

HOME_ASSISTANT_ID = assistant.id

while True:  # wait for the brightness value
    if not data_stack.empty():
        brightness = data_stack.get()
        break

# brightness = data_queue.get()

api_thread, run = create_thread_and_run("The brightness value is {}.".format(brightness))
run = wait_on_run(run, api_thread)

while True:
    try:
        tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # The Assistants API will pause execution during a Run when it invokes functions,
        # and you can supply the results of the function call back to continue the Run execution.
        if name == "control_lamp":  # In the future, we will support more functions.
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id = api_thread.id,
                run_id = run.id,
                tool_outputs = [
                    {
                        "tool_call_id": tool_call.id,
                        "output": transmit_coordinator_command(arguments["command"]),
                    }
                ],
            )

            run = wait_on_run(run, api_thread)

            messages = client.beta.threads.messages.list(
                thread_id = api_thread.id,
                order = "asc"
            )
            pretty_print(messages)

    except Exception as e:
        print('Exception: ', e)

    finally:
        print('\nwait for 20 seconds')
        time.sleep(20)  # make sure run.status won't be 'failed', because the rate limit is 3 requests per minute.
        # Add a new message to the api_thread

        brightness = data_stack.get()
        data_stack.queue_clear()  # clear the stack
        run = submit_message(HOME_ASSISTANT_ID, api_thread, "The brightness value is {}.".format(brightness))
        run = wait_on_run(run, api_thread)
