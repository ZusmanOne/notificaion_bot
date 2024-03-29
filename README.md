# Бот для доставки уведомлений о проверках ваших проектов

Данный бот служит для доставки уведомлений о проверенных работах. Даже если проверка прошла с замечаниями,
этот бот отобразит все в своем сообщении.

## Как запустить бота
Скачайте код  
```
git clone https://github.com/ZusmanOne/notificaion_bot.git
```
перейдите в скачанный каталог 
```sh
cd notificaion_bot
```
[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создайте файл `.env` в корне каталога `bot_notification/` со следующими настройками:

- `DEVMAN_TOKEN` — для этого зарегистрируйтесь на сайте [Devman](https://dvmn.org)
- `TG_TOKEN` — для этого вам нужно написать [отцу ботов](https://telegram.me/BotFather).
- `TG_CHAT_ID` — для этого нужно написать [этому боту](https://telegram.me/getmyid_bot)

Бот готов для запуска, запустите файл `main.py` и после проверки проекта вам придет уведомление.
### Бот так же обернут в докер, что бы запустить проект в докере, следуйте инструкциям:

- для этого установите докер на свою машину согласно [инструкции](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru), если еще это не делалаи
- создайте докер-образ на основе файла Dockerfile:
``` 
docker build -t name_image .
```
- запустите контейнер на основе созданного образа:
``` 
docker run --env-file ./.env name_image
```