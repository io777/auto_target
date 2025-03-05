# Первый запуск

### Установка зависимостей и загрузка моделей

make prepare

### Сборка Docker образа

make build

### Запуск контейнера

make up

### Просмотр логов

make logs

# Последующие запуски

### Запуск

make up

### Просмотр логов

make logs

### Остановка контейнера

make down

### Перезапуск

make restart

### Полная очистка

make clean

### Статус контейнера

docker ps

### Использование ресурсов

docker stats object_detection

### Проверка доступа к камере

v4l2-ctl --list-devices

### Проверка X11

xhost | grep local:docker
