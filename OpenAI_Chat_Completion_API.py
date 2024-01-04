import json

from openai import OpenAI

from coordinator import *

with open('OpenAI_API.json', 'r') as f:
    chat_completion_api = json.load(f)['chat_completion_api']
api_key = chat_completion_api['api_key']
base_url = chat_completion_api['base_url']

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

try:
    while not data_queue.empty():
        brightness = data_queue.get()
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo-16k-0613",
            messages = [
                {"role": "system", "content": "You are a smart home assistant, and you can control the lamp"
                                              "based on the current brightness to make the homeowner feel comfortable."
                                              "You only need to reply 'ON' or 'OFF'."},
                {"role": "user", "content": "The brightness is {}. Can you help me "
                                            "decide whether to open the lamp?".format(brightness)},
            ]
        )

        print('The brightness is {} (in Celsius),'.format(brightness), 'so',
              transmit_coordinator_data(completion.choices[0].message.content))

except KeyboardInterrupt:
    print("KeyboardInterrupt")

finally:
    ser.close()
    print("Serial port {} is close.".format(ser.name))
