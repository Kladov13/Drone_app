# паттерн MVC(посредник)
class UAVController:
    """
    Класс UAVController управляет логикой работы дрона.
    """

    def __init__(self, model, view):
        """
        Инициализация контроллера.
        """
        self.model = model
        self.view = view

    def adjust_position(self, new_coordinates):
        """
        Изменяет координаты дрона.
        """
        self.model.update_coordinates(new_coordinates)
        return self.view.show_status(self.model)

    def adjust_height(self, new_height):
        """
        Изменяет высоту дрона.
        """
        self.model.update_height(new_height)
        return self.view.show_status(self.model)

    def adjust_velocity(self, new_velocity):
        """
        Изменяет скорость дрона.
        """
        self.model.update_velocity(new_velocity)
        return self.view.show_status(self.model)

    def check_battery(self):
        """
        Проверяет уровень заряда батареи.
        """
        if self.model.battery < 20:
            return self.view.warning("Battery low! Initiating return to base.")
        return {"battery_level": self.model.battery}

    def return_to_base(self):
        """
        Возвращает дрон на базу.
        """
        self.model.update_coordinates((0, 0))
        self.model.update_height(0)
        self.model.update_velocity(0)
        return self.view.warning("UAV has returned to base.")
