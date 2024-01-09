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
    while True:
        if not data_stack.empty():
            temperature = data_stack.get()
            humidity = data_stack.get()
            completion = client.chat.completions.create(
                model = "gpt-3.5-turbo-16k-0613",
                messages = [
                    {"role": "system", "content": "You are a smart home assistant,"
                                                  "and you can control the fan and dehumidifier respectively"
                                                  "based on the current temperature and humidity"
                                                  "to make the homeowner feel comfortable."
                                                  "The normal temperature value is approximately between 24 and 26."
                                                  "So, when the temperature is higher than 26, you should turn on the fan."
                                                  "So, when the temperature is lower than 24, you should turn off the fan."
                                                  "The normal humidity value is approximately between 70 and 80."
                                                  "So, when the humidity is higher than 85, you should turn on the dehumidifier."
                                                  "So, when the humidity is lower than 65, you should turn off the dehumidifier."
                                                  "You should reply 'fan_on & dehumidifier_on' or 'fan_off & dehumidifier_on'"
                                                  "or 'fan_on & dehumidifier_off' or 'fan_off & dehumidifier_off'"
                                                  "without any other words."},
                    {"role": "user", "content": "The temperature is {} and the humidity is {}. Can you help me "
                                                "decide whether to open the fan?".format(temperature, humidity)},
                ]
            )

            print('* The temperature is {} and the humidity is {}'.format(temperature, humidity), 'so',
                  transmit_coordinator_command(completion.choices[0].message.content))
            time.sleep(5)

except KeyboardInterrupt:
    print("KeyboardInterrupt")

finally:
    ser.close()
    print("Serial port {} is close.".format(ser.name))
