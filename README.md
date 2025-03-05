# Первый запуск

make prepare # Установка зависимостей и загрузка моделей
make build # Сборка Docker образа
make up # Запуск контейнера
make logs # Просмотр логов

# Последующие запуски

make up # Запуск
make logs # Просмотр логов

# Остановка

make down # Остановка контейнера

# Перезапуск

make restart # Перезапуск контейнера

# Полная очистка

make clean # Удаление всех ресурсов

# Статус контейнера

docker ps

# Использование ресурсов

docker stats object_detection

# Проверка доступа к камере

v4l2-ctl --list-devices

# Проверка X11

xhost | grep local:docker
