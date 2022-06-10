import requests
from time import sleep

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    headers = {'Authorization': 'Token 1ff0f78cc5a3bec7437264cfb33e8c86c0d2e58e'}
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


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
