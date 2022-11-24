import requests
from time import sleep
from environs import Env
import telegram
import logging

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.tg_bot = telegram.Bot(tg_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(tg_token, chat_id, *messages):
    bot = telegram.Bot(tg_token)
    bot.send_message(text=f'У 2вас проверили работу "{messages[0]}" \n\n {messages[1]} \n'
                     f'{messages[2]}', chat_id=chat_id)


def main():
    env = Env()
    env.read_env()
    chat_id = env('TG_CHAT_ID')
    tg_token = env('TG_TOKEN')
    token = env('DEVMAN_TOKEN')
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_token, chat_id))
    logger.info('бот запущен')
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
            send_message(tg_token, chat_id, message_title, message_result, message_link)
        except requests.exceptions.ReadTimeout as err:
            logger.info(err)
            continue
        except requests.exceptions.ConnectionError as err:
            logger.info(err)
            sleep(5)
        except Exception:
            logger.exception('что то пошло не так')



if __name__ == '__main__':
    print('Запуск!!!!!')
    main()
