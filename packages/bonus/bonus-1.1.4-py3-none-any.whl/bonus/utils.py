import abc



class BonusABC(abc.ABC):

    @abc.abstractmethod
    def _get(self):
        """Сделать запрос к серверу по api, чтобы получить список бонусов"""

    @abc.abstractmethod
    def _post(self):
        """Отправить запрос на сервер по api, чтобы сохранить данные в гугл таблицу"""

    @abc.abstractmethod
    def run(self):
        """Запустить рулетку"""

