#!/bin/bash

# Функция для проверки наличия Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker не установлен. Установка..."
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker $USER
        echo "Требуется перезагрузка системы"
        exit 1
    fi
}

# Функция для проверки наличия Docker Compose
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose не установлен. Установка..."
        sudo apt-get update
        sudo apt-get install -y docker-compose
    fi
}

# Функция для проверки наличия YOLO файлов
check_yolo_files() {
    if [ ! -f "yolo/yolov4-tiny.weights" ] || [ ! -f "yolo/yolov4-tiny.cfg" ] || [ ! -f "yolo/coco.names" ]; then
        echo "Отсутствуют необходимые файлы YOLO. Загрузка..."
        mkdir -p yolo
        wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights -O yolo/yolov4-tiny.weights
        wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg -O yolo/yolov4-tiny.cfg
        wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names -O yolo/coco.names
    fi
}

# Функция для настройки прав доступа к камере
setup_camera_permissions() {
    if [ ! -c /dev/video0 ]; then
        echo "Камера не найдена в /dev/video0"
        exit 1
    fi
    sudo chmod 666 /dev/video0
}

# Функция для настройки X11
setup_x11() {
    xhost +local:docker
}

case "$1" in
    "start")
        check_docker
        check_docker_compose
        check_yolo_files
        setup_camera_permissions
        setup_x11
        docker-compose up --build
        ;;
    "stop")
        docker-compose down
        ;;
    "restart")
        docker-compose restart
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "clean")
        docker-compose down --rmi all --volumes
        ;;
    *)
        echo "Использование: $0 {start|stop|restart|logs|clean}"
        exit 1
        ;;
esac
