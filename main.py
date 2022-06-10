import requests
from time import sleep
from environs import Env
import asyncio
import telegram

async def main():
    bot = telegram.Bot(env('TG_TOKEN'))
    async with bot:
        await bot.send_message(text='Hello world',chat_id=305151573)


def get_notification():
    headers = {'Authorization': env('DEVMAN_TOKEN')}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers)
            if response.json()['status'] == 'timeout':
                timestamp = {'timestamp': response.json()['timestamp_to_request']}
                new_response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=timestamp)
        except requests.exceptions.ReadTimeout:
            print('время истекло')
        except requests.exceptions.ConnectionError:
            print('интернет отключился,а я нет')
            sleep(5)

env = Env()
env.read_env()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
