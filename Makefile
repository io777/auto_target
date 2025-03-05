DOCKER_COMPOSE = docker-compose

.PHONY: prepare build up down restart logs clean

prepare:
	@echo "Подготовка системы..."
	@sudo apt-get update && sudo apt-get install -y \
		docker.io \
		docker-compose \
		v4l-utils \
		x11-xserver-utils
	@sudo usermod -aG docker $(USER)
	@sudo usermod -aG video $(USER)
	@sudo chmod 666 /dev/video0
	@xhost +local:docker
	@mkdir -p yolo
	@echo "Загрузка моделей YOLO..."
	@if [ ! -f "yolo/yolov4-tiny.weights" ]; then \
		curl -L https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights -o yolo/yolov4-tiny.weights; \
	fi
	@if [ ! -f "yolo/yolov4-tiny.cfg" ]; then \
		curl -L https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg -o yolo/yolov4-tiny.cfg; \
	fi
	@if [ ! -f "yolo/coco.names" ]; then \
		curl -L https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names -o yolo/coco.names; \
	fi

build:
	@echo "Сборка Docker образа..."
	$(DOCKER_COMPOSE) build

up:
	@echo "Проверка X11..."
	@xhost +local:docker
	@echo "Запуск контейнера..."
	$(DOCKER_COMPOSE) up -d
	@echo "Для просмотра логов используйте: make logs"

down:
	@echo "Остановка контейнера..."
	$(DOCKER_COMPOSE) down

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f

clean:
	@echo "Очистка ресурсов..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	@rm -rf yolo/*.weights yolo/*.cfg yolo/*.names
	@echo "Очистка завершена"
