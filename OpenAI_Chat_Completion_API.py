import json

from openai import OpenAI

# from coordinator import *

with open('OpenAI_API.json', 'r') as f:
    chat_completion_api = json.load(f)['chat_completion_api']
api_key = chat_completion_api['api_key']
base_url = chat_completion_api['base_url']

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

# while True:
#     temperature = receive_coordinator_data()
#     completion = client.chat.completions.create(
#         model = "gpt-3.5-turbo-16k-0613",
#         messages = [
#             {"role": "system", "content": "You are a smart home assistant, and you can control the fan"
#                                           "based on the current temperature to make the homeowner feel comfortable."
#                                           "You only need to reply 'ON' or 'OFF'."},
#             # or use regex to match 'ON' or 'OFF'
#             {"role": "user", "content": "The temperature is {} (in Celsius). Can you help me "
#                                         "decide whether to open the fan?".format(temperature)},
#         ]
#     )
#
#     print('The temperature is {} (in Celsius),'.format(temperature), 'so', transmit_coordinator_data(completion.choices[0].message.content))
#     time.sleep(1)
