import requests
from time import sleep
from environs import Env
import asyncio
import telegram

env = Env()
env.read_env()

CHAT_ID = env('CHAT_ID')
TG_TOKEN = env('TG_TOKEN')
TOKEN = env('DEVMAN_TOKEN')


async def main(*messages):
    bot = telegram.Bot(TG_TOKEN)
    async with bot:
        await bot.send_message(text=f'У вас проверили работу "{messages[0]}" \n\n {messages[1]}', chat_id=CHAT_ID)


def get_notification():
    headers = {'Authorization': TOKEN}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers)
            if response.json()['status'] == 'found':
                message_1 = response.json()['new_attempts'][0]['lesson_title']
                if response.json()['new_attempts'][0]['is_negative']:
                    message_2 = 'К сожалению, в работе нашлись ошибки.'
                    asyncio.run(main(messages_1, message_2))
                else:
                    message_2 = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
                    asyncio.run(main(message_1, message_2))
            elif response.json()['status'] == 'timeout':
                timestamp = {'timestamp': response.json()['timestamp_to_request']}
                new_response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=timestamp)
                if new_response.json()['status'] == 'found':
                    asyncio.run(main())
        except requests.exceptions.ReadTimeout:
            print('время истекло')
        except requests.exceptions.ConnectionError:
            print('интернет отключился,а я нет')
            sleep(5)


if __name__ == '__main__':
    get_notification()
