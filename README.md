# Инструкция по развертке бекенда для приложения хранения файлов Megadisk

Примеры в инструкции будут написаны для Ubuntu, предустановленную на платформе reg.ru. Но, по образу и подобию, вы можете развернуть данный продукт на других линуксоподобных ОС.

## Обновление информации о пакетах ОС

Перед установкой программного обеспечени необходимо обновить информацию о пакетах операционной системы, чтобы установить актуальные версии программ

#### Пример для Ubuntu v22 reg.ru

```
apt update
``` 

## Установка программ

Для работы бекенда нужно установить следующее ПО:
1. Git
2. Python 3 версии
3. Pip
4. Venv
5. Postgresql
6. Nginx

#### Пример для Ubuntu v22 reg.ru

На данной операционной системе уже установлен Git и Python3 нормальных версий

Устанавливаем остальное ПО

```
apt install postgresql python3-pip python3-venv nginx
```

## Создаем папку для проекта

Нужно создать папку для проекта и перейти в нее

#### Пример для Ubuntu v22 reg.ru

```
mkdir /home/backend
cd /home/backend/
```

## Скачиваем бекенд из репозитория и переходим в папку проекта

Скачиваем код бекенда с github.com. После скачивания необходимо перейти в папку проекта

#### Пример для Ubuntu v22 reg.ru

```
git clone https://github.com/babka40000/DIPLOM_BACKEND.git
cd DIPLOM_BACKEND
```

## Создаем и активируем виртуальное окружение

Необходимо создать и активировать виртуальное окружение с помощью Venv

```
python3 -m venv env
source env/bin/activate
```

## Устанавливаем зависимости

Переходим в папку с django и устанавливаем зависимости из файла requirements.txt

```
cd megadisk
pip install -r requirements.txt
```

## Настраиваем postgresql

Меняем пользователя на постгрес

```
su postgres
```

Открываем программу psql

```
psql
```

Задаем пароль для пользователя "postgres"

```
ALTER USER postgres WITH PASSWORD 'новый пароль';
```

Создаем базу данных для проекта

```
CREATE DATABASE megadisk OWNER postgres;
```

Выходим из psql

```
\q
```

Выходим из пользователя postgres

```
exit
```

## Прописываем переменные окружения

Переходим в папку megadisk

```
cd megadisk
```

Нам нужно создать файл .env и прописать переменные окружения для текущего сервера. В папке лежит файл .env.example, в котором прописаны все поля со сначеними для примера. Нужно скопировать этот файл в .env и изменить значения в нем на нужные нам.

```
cp .env.example .env
nano .env
```

После редактировани параметров сохраняемся и выходим из редактора.

После этого возвращаемся в родительскую папку megadisk 

```
cd ..
```

## Миграции

Делаем миграции таблиц в БД postgresql

```
python manage.py migrate
```

## Собираем static файлы

Собираем статические файлы в папку staic специальной командой

```
python manage.py collectstatic
```

## Создаем администратора.

Обязательно нужно создать super user`а. Это первый пользователь, который в системе всегда будет администратором. Остальных администратоов может создать superuser

```
python manage.py createsuperuser
```

## Устанавливаем и настраиваем gunicorn

Gunicorn - специальная программа для связи веб-сервера (например nginx) и Django.

Устанавливаем программу

```
pip install gunicorn
```

Теперь нам нужно сделать из gunicorn демона, чтобы он мог автоматически запускаться и работать в фоновом режиме

Создаем файл и открываем его на редактирование

```
touch /etc/systemd/system/gunicorn.service
nano /etc/systemd/system/gunicorn.service
```

Вставляем в созданные код следующий код:

```
gunicorn.service
[Unit]
Description=gunicorn server
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/home/backend/DIPLOM_BACKEND/megadisk
ExecStart=/home/backend/DIPLOM_BACKEND/env/bin/gunicorn --access-logfile - --workers=4 --bind unix:/home/backend/DIPLOM_BACKEND/megadisk/megadisk/project.sock megadisk.wsgi:application
[Install]
WantedBy=multi-user.target
```

Сохраняемся и выходим из редактора.

Запускаем демона и прописываем его в автозагрузку

```
systemctl start gunicorn
systemctl enable gunicorn
```

## Настройка nginx

nginx - веб сервер, который обрабатывает запросы вашего браузера. Потом он их должен по цепочке отправлять в gunicorn. Также нужно указать веб-серверу папку со статикой.

Делаем файл с настройками и открываем его в редакторе

```
touch /etc/nginx/sites-available/megadisk_backend
nano /etc/nginx/sites-available/megadisk_backend
```

Копируем в файл следующую конфигурацию:

```
server {
  listen 8000;
  server_name localhost;

  location /static/ {
    root /home/backend/DIPLOM_BACKEND/megadisk;
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/home/backend/DIPLOM_BACKEND/megadisk/megadisk/project.sock;
  }
}
```

Сохраняемся и выходим

Включаем нашу настройку в конфигурацию nginx

```
ln -s /etc/nginx/sites-available/megadisk_backend /etc/nginx/sites-enabled/
```

Перезапускаем nginx

```
service nginx restart
```

Открываем порты фаервола для nginx

```
ufw allow 'Nginx Full'
```

На этом настройка бекенда завершена.