import requests
from time import sleep
from environs import Env
import asyncio
import telegram


async def send_message(tg_token, chat_id, *messages):
    bot = telegram.Bot(tg_token)
    async with bot:
        await bot.send_message(text=f'У вас проверили работу "{messages[0]}" \n\n {messages[1]} \n'
                                    f'{messages[2]}', chat_id=chat_id)


def main():
    env = Env()
    env.read_env()
    chat_id = env('TG_CHAT_ID')
    tg_token = env('TG_TOKEN')
    token = env('DEVMAN_TOKEN')
    headers = {'Authorization': token}
    params = None
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                params=params,

            )
            response.raise_for_status()
            result_reviews = response.json()
            if result_reviews['status'] == 'timeout':
                params = {'timestamp': result_reviews["timestamp_to_request"]}
                continue
            params = {'timestamp': result_reviews['last_attempt_timestamp']}
            message_title = result_reviews['new_attempts'][0]['lesson_title']
            if result_reviews['new_attempts'][0]['is_negative']:
                message_result = 'К сожалению, в работе нашлись ошибки.'
            else:
                message_result = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
            message_link = result_reviews['new_attempts'][0]['lesson_url']
            asyncio.run(send_message(tg_token, chat_id, message_title, message_result, message_link))
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print('Интернет отключился,а я нет')
            sleep(10)


if __name__ == '__main__':
    main()


