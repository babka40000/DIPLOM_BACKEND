# Инструкция по развертке бекенда для приложения хранения файлов Megadisk

Примеры в инструкции будут написаны для Ubuntu, предустановленную на платформе reg.ru. Но, по образу и подобию вы можете развернуть данный продукт на других линуксоподобных ОС.

## Обновление информации о пакетах ОС

Перед установкой программного обеспечени не обходимо обновить информацию о пакетах операционно системы, чтобы установить актуальные версии программ

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

Скачиваем код бекенда с github.com. После скчивания необходимо перейти в папку проекта

#### Пример для Ubuntu v22 reg.ru

```
git clone https://github.com/babka40000/DIPLOM_BACKEND.git
cd DIPLOM_BACKEND
```





## Установка программ

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

gunicorn.service
[Unit]
Description=gunicorn server
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/home/backend/DIPLOM_BACKEND/megadisk
ExecStart=/home/backend/DIPLOM_BACKEND/megadisk/env/bin/gunicorn --access-logfile - --workers=4 --b>
[Install]
WantedBy=multi-user.target

ln -s /etc/nginx/sites-available/megadisk_frontend /etc/nginx/sites-enabled/

python manage.py collectstatic

systemctl enable gunicorn
 ufw allow 'Nginx Full'
 
  pip install gunicorn
  
python3 -m venv env

postgresql python3-pip python3-venv

apt update