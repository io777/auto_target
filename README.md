# Первый запуск

### Установка зависимостей и загрузка моделей

```bash
make prepare
```

### Сборка Docker образа

```bash
make build
```

### Запуск контейнера

```bash
make up
```

### Просмотр логов

```bash
make logs
```

# Последующие запуски

### Запуск

```bash
make up
```

### Просмотр логов

```bash
make logs
```

### Остановка контейнера

```bash
make down
```

### Перезапуск

```bash
make restart
```

### Полная очистка

```bash
make clean
```

### Статус контейнера

```bash
docker ps
```

### Использование ресурсов

```bash
docker stats object_detection
```

### Проверка доступа к камере

```bash
v4l2-ctl --list-devices
```

### Проверка X11

```bash
xhost | grep local:docker
```
