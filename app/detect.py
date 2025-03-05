import cv2
import numpy as np
import argparse
import os
import time


class ObjectDetector:
    def __init__(self, args):
        self.args = args
        self.initialize_model()
        self.camera_index = int(os.getenv("CAMERA_INDEX", 0))

        # Создаем окно до инициализации камеры
        cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)
        # Устанавливаем размер окна по умолчанию
        cv2.resizeWindow("Object Detection", 1280, 720)

        self.initialize_camera()

    def initialize_camera(self):
        print(f"[INFO] Подключение к камере {self.camera_index}...")

        self.cap = cv2.VideoCapture(self.camera_index)

        # Настройка камеры
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"[ERROR] Не удалось подключиться к камере {self.camera_index}"
            )

        # Проверка успешного захвата
        ret, test_frame = self.cap.read()
        if not ret:
            raise RuntimeError("[ERROR] Не удалось получить кадр с камеры")

        print("[INFO] Камера успешно инициализирована")
        print(
            f"Разрешение: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
        )
        print(f"FPS: {int(self.cap.get(cv2.CAP_PROP_FPS))}")

    def process_frame(self, frame):
        # Добавляем информацию о производительности
        start_time = time.time()

        height, width = frame.shape[:2]

        # Создание блоба
        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
        )
        self.net.setInput(blob)

        # Получение результатов
        outputs = self.net.forward(self.output_layers)

        # Подготовка списков
        boxes = []
        confidences = []
        class_ids = []

        # Обработка результатов
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # Получение координат
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Вычисление координат прямоугольника
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Применение non-maximum suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Отрисовка результатов
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                label = f"{self.classes[class_ids[i]]}: {confidences[i]:.2f}"

                # Рисуем прямоугольник
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Добавляем фон для текста
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(
                    frame, (x, y - 25), (x + text_size[0], y), (0, 255, 0), cv2.FILLED
                )

                # Добавляем текст
                cv2.putText(
                    frame,
                    label,
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    2,
                )

        # Вычисление и отображение FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        return frame

    def run(self):
        print("[INFO] Запуск обработки видео...")

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("[WARNING] Ошибка получения кадра")
                    continue

                # Обработка кадра
                processed_frame = self.process_frame(frame)

                # Показ результата
                cv2.imshow("Object Detection", processed_frame)

                # Проверка нажатия клавиш
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q") or key == 27:  # q или ESC
                    break
                elif key == ord("f"):  # Переключение полноэкранного режима
                    if (
                        cv2.getWindowProperty(
                            "Object Detection", cv2.WND_PROP_FULLSCREEN
                        )
                        == cv2.WINDOW_FULLSCREEN
                    ):
                        cv2.setWindowProperty(
                            "Object Detection",
                            cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_NORMAL,
                        )
                    else:
                        cv2.setWindowProperty(
                            "Object Detection",
                            cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_FULLSCREEN,
                        )

        except KeyboardInterrupt:
            print("\n[INFO] Прерывание пользователем")
        finally:
            self.cleanup()

    def cleanup(self):
        print("[INFO] Очистка ресурсов...")
        if hasattr(self, "cap"):
            self.cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # Необходимо для корректного закрытия окон


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--yolo", required=True, help="путь к директории YOLO")
    args = vars(ap.parse_args())

    detector = ObjectDetector(args)
    detector.run()


if __name__ == "__main__":
    main()
