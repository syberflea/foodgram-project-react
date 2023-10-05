# Foodgram — сайт для обмена рецептами. 

## Описание проекта
Наш сайт https://syberflea.ddns.net/ ждет вас!
Пользователи могут регистрироваться, создавать любимые рецепты, загружать их фотографии, давать краткое описание, смотреть фото рецептов, которые опубликовали други пользователи.
Проект создан в рамках учебного курса "Python-разработчик" на платформе Яндекс.Практикум. 
Это дальнейшее развитие проекта в терминах (образах) контейниризации на основе Docker.

## Технологии
 - Python 3.9
 - Django 3.2.3
 - Django REST framework 3.12.4
 - Nginx
 - Gunicorn
 - Docker
 - Postgres


## Локальное развертывание проекта
1. Клонируйте репозиторий [foodgram-project-react](git@github.com:syberflea/foodgram-project-react.git).
2. В каталоге с проектом создайте и активируйте виртуальное окружение: `python3 -m venv venv && source venv/bin/activate`
3. Установите зависимости: `pip install -r requirements.txt`.  
4. Выполните миграции: `python manage.py migrate`.  
5. Создайте суперюзера: `python manage.py createsuperuser`.

### Переменные окружения
В корневом каталоге проекта создайте файл .env и заполните его. В качестве образца используйте .env.example


### Создание Docker-образов
1. Замените username на ваш логин на DockerHub:
```
cd frontend
docker build -t username/foodgram_frontend .
cd ../backend
docker build -t username/foodgram_backend .
```
2. Загрузите образы на DockerHub:
```
docker push username/foodgram_frontend
docker push username/foodgram_backend
```

## Установка проекта на сервер

1. Подключитесь к удаленному серверу

```ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера ```

2. Создайте на сервере директорию kittygram

`mkdir foodgram`

3. Установка docker compose на сервер:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

Скопируйте файл docker-compose.production.yml:
```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
```

4. Запустите docker compose в режиме демона:

`sudo docker compose -f docker-compose.production.yml up -d`

5. Выполните миграции, соберите статику бэкенда и скопируйте их в /backend_static/static/:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

6. На сервере в редакторе nano откройте конфиг Nginx:

`sudo nano /etc/nginx/sites-enabled/default`

7. Добавте настройки location в секции server:
```
location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:8000;
}
```

8. Проверьте работоспособность конфигураций и перезапустите Nginx:
```
sudo nginx -t 
sudo service nginx reload
```

(с) Евгений Андронов, 2023
