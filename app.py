from flask import Flask, request, jsonify, Response, render_template
import cv2
import threading
import subprocess
from models import UAVModel
from views import UAVView
from controllers import UAVController

app = Flask(__name__, static_folder='static', template_folder='templates')

# Описание проекта:
# Этот проект представляет собой веб-приложение для управления и мониторинга дрона.
# Основные характеристики включают:
# - Возможность отображения текущего статуса дрона.
# - Обновление координат, высоты и скорости дрона.
# - Проверка уровня заряда батареи.
# - Возвращение дрона на базу.
# Цели проекта: предоставить простой интерфейс для взаимодействия с дроном через веб-приложение.
# Область применения: управление дронами в реальном времени через веб-интерфейс.

# Инициализация модели, представления и контроллера
# Создаем экземпляры модели, представления и контроллера, которые будут использоваться для управления
# состоянием дрона, отображения данных и обработки запросов.
uav_model = UAVModel()  # Модель для хранения и управления состоянием дрона.
uav_view = UAVView()    # Представление для отображения состояния дрона.
uav_controller = UAVController(uav_model, uav_view)  # Контроллер для обработки логики управления дронов.

# Настройка видеопотока с веб-камеры
def start_video_stream():
    """
    Запускает видеопоток с веб-камеры через FFmpeg.
    """
    capture = cv2.VideoCapture(0)
    resolution = f'{int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))}'

    frame_rate = 25
    codec = 'libx264'
    preset = 'fast'
    output_format = 'mpegts'
    address = 'udp://127.0.0.1:1234'

    settings = [
        'ffmpeg',
        '-loglevel', 'debug',
        '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', resolution,
        '-r', str(frame_rate),
        '-i', '-', '-an',
        '-c:v', codec,
        '-preset', preset,
        '-f', output_format,
        address
    ]
    ffmpeg = subprocess.Popen(settings, stdin=subprocess.PIPE)

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        ffmpeg.stdin.write(frame.tobytes())

    capture.release()
    ffmpeg.stdin.flush()
    ffmpeg.stdin.close()
    ffmpeg.wait()

# Запуск видеопотока в отдельном процессе

video_thread = threading.Thread(target=start_video_stream)
video_thread.start()


@app.route('/')
def index():
    """
    Отображение главной страницы.
    Главная страница загружает HTML-шаблон для взаимодействия с пользователем.
    """
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    """
    Получение текущего статуса дрона.
    Использует представление для получения состояния дрона и возвращает его в формате JSON.
    """
    return jsonify(uav_view.show_status(uav_model))

@app.route('/position', methods=['POST'])
def update_position():
    """
    Обновление координат дрона.
    Принимает новые координаты из JSON-запроса и передает их контроллеру для обновления модели.
    """
    data = request.get_json()
    new_coordinates = data.get('coordinates', (0, 0))
    return jsonify(uav_controller.adjust_position(new_coordinates))

@app.route('/height', methods=['POST'])
def update_height():
    """
    Обновление высоты дрона.
    Принимает новую высоту из JSON-запроса и передает её контроллеру для обновления модели.
    """
    data = request.get_json()
    new_height = data.get('height', 0)
    return jsonify(uav_controller.adjust_height(new_height))

@app.route('/velocity', methods=['POST'])
def update_velocity():
    """
    Обновление скорости дрона.
    Принимает новую скорость из JSON-запроса и передает её контроллеру для обновления модели.
    """
    data = request.get_json()
    new_velocity = data.get('velocity', 0)
    return jsonify(uav_controller.adjust_velocity(new_velocity))

@app.route('/battery', methods=['GET'])
def check_battery():
    """
    Проверка уровня заряда батареи дрона.
    Использует контроллер для получения информации о заряде батареи и возвращает её в формате JSON.
    """
    return jsonify(uav_controller.check_battery())

@app.route('/return_to_base', methods=['POST'])
def return_to_base():
    """
    Возвращение дрона на базу.
    Использует контроллер для выполнения команды возврата на базу и возвращает результат в формате JSON.
    """
    return jsonify(uav_controller.return_to_base())

@app.route('/video_feed')
def video_feed():
    """
    Обработка видеопотока с веб-камеры.
    """
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    """
    Генератор кадров для видеопотока с веб-камеры.
    """
    cap = cv2.VideoCapture('udp://127.0.0.1:1234')  # Видеопоток с FFmpeg
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Кодируем кадры в JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Отправляем кадры как поток данных
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
