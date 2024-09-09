# паттерн Строитель(хранитель)
class UAVModel:
    """
    Класс UAVModel управляет состоянием дрона.

    Основные характеристики:
    - Хранение текущей высоты, скорости, координат и уровня заряда батареи дрона.
    - Методы для обновления этих данных.

    Цели:
    - Обеспечить управление состоянием дрона и предоставление данных для взаимодействия с другими компонентами системы.
    """

    def __init__(self):
        """
        Инициализация начальных данных дрона.
        """
        self.height = 0
        self.velocity = 0
        self.coordinates = (0, 0)
        self.battery = 100

    def update_coordinates(self, new_coordinates):
        """
        Обновляет координаты дрона.

        Параметры:
        - new_coordinates: новые координаты (tuple)
        """
        self.coordinates = new_coordinates

    def update_height(self, new_height):
        """
        Обновляет высоту дрона.

        Параметры:
        - new_height: новая высота (int)
        """
        self.height = new_height

    def update_velocity(self, new_velocity):
        """
        Обновляет скорость дрона.

        Параметры:
        - new_velocity: новая скорость (int)
        """
        self.velocity = new_velocity

    def consume_battery(self, consumption):
        """
        Уменьшает заряд батареи.

        Параметры:
        - consumption: количество потребляемой энергии (int)
        """
        self.battery -= consumption
