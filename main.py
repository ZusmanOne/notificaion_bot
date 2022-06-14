import requests
from time import sleep
from environs import Env
import asyncio
import telegram



async def send_message(*messages):
    bot = telegram.Bot(TG_TOKEN)
    async with bot:
        await bot.send_message(text=f'У вас проверили работу "{messages[0]}" \n\n {messages[1]} \n'
                                    f'{messages[2]}', chat_id=CHAT_ID)


def get_notification():
    headers = {'Authorization': TOKEN}
    params = None
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                params=params
            )
            if response.json()['status'] == 'timeout':
                params["timestamp"] = response.json()["timestamp_to_request"]
                continue
            params = {'timestamp': response.json()['last_attempt_timestamp']}
            message_1 = response.json()['new_attempts'][0]['lesson_title']
            if response.json()['new_attempts'][0]['is_negative']:
                message_2 = 'К сожалению, в работе нашлись ошибки.'
            else:
                message_2 = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
            message_3 = response.json()['new_attempts'][0]['lesson_url']
            asyncio.run(send_message(message_1, message_2, message_3))
        except requests.exceptions.ReadTimeout:
            print('время истекло')
            continue
        except requests.exceptions.ConnectionError:
            print('Интернет отключился,а я нет')
            sleep(5)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    CHAT_ID = env('TG_CHAT_ID')
    TG_TOKEN = env('TG_TOKEN')
    TOKEN = env('DEVMAN_TOKEN')

    get_notification()


