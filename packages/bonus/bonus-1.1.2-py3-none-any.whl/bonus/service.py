import time
import requests
from IPython.display import clear_output, display
from ipywidgets import HBox

from .utils import (
    BonusABC,
    text_input,
    btn,
    progress_bar,
)


class bonus(BonusABC):
    api_endpoint = 'https://new.analytic.neural-university.ru/api/v1/roulette/'

    def __init__(self, uuid):
        self.uuid = uuid
        self.session = requests.Session()

        # Виджеты для сохранения в гугл таблицу
        self.name = text_input(placeholder='Имя', description='Имя:')
        self.email = text_input(placeholder='e-mail', description='e-mail:')
        self.phone = text_input(placeholder='телефон', description='Телефон:')

        # Кнопка Забронировать
        self.btn_access = btn(description='Забронировать', style='success', tooltip='Забронировать')
        # Кнопка Заново
        self.btn_reload = btn(description='Заново', style='warning', tooltip='Заново')
        # Кнопка Сохранить
        self.btn_send = btn(description='Сохранить', style='success', tooltip='Сохранить')
        # Виджет для полосы загрузки
        self.progress = progress_bar()

    def _btn_access_clicked(self, btn_access):
        """
        Функция, которая выводит поля для ввода
        """
        self._show_bonus_summary()
        display(self.name)
        display(self.email)
        display(self.phone)
        display(self.btn_send)

    def _btn_reload_clicked(self, btn_reload):
        """
        Функция, которая крутит рулетку заново
        """
        # Отчищаем поле вывода ячейки, чтобы там не копились прошлые бонусы
        clear_output(wait=True)
        # Новый обработчик событий нажатия на кнопку СОХРАНИТЬ
        self.btn_send.on_click(self._save_data)
        # выбираем бонус
        self.bonus = self._get()
        # Выводим сообщения
        self._show()
        # Нажатие на кнопки ЗАБРОНИРОВАТЬ и ЗАНОВО
        self.btn_access.on_click(self._btn_access_clicked)
        self.btn_reload.on_click(self._btn_reload_clicked)

    def _get(self):
        # Получаем словарь с бонусами
        response = self.session.get(self.api_endpoint,
                                    params={
                                        'uuid': self.uuid
                                    })
        return response.json()['bonus']

    def _post(self):
        # Сохраняем в гугл таблицу
        data = {
            'name': self.name.value,
            'phone': self.phone.value,
            'email': self.email.value
        }
        response = self.session.post(self.api_endpoint,
                                     data=data
                                     )
        return response

    def _save_data(self, b: None = None) -> None:
        response = self._post()
        if response.status_code == 200:
            self.btn_send.disabled = False
            clear_output(wait=True)
            print('\033[95m' + 'Отлично, эти подарки теперь забронированы за вами!')
            print('Скоро мы вам позвоним :)')
        else:
            print('\033[91m' + 'Ошибка сервера! Обратитесь, пожалуйста, к менеджерам УИИ')

        self.session.close()

    def _show_bonus_summary(self):
        # Чистим все и выводим снова все бонусы сразу
        clear_output(wait=True)
        print('\033[1m' + '\033[92m' + 'Поздравляем! Ваш список бонусов:' + '\033[0m')
        for key, value in self.bonus.items():
            print(f'- {key} ({value} руб)')

        # Считаем сумму всех бонусов и выводим
        total_bonus = sum(int(value) for value in self.bonus.values())
        print('\033[4m' + f'\nВам выпало бонусов на {total_bonus} руб.\n' + '\033[0m')
        # Это принт, который можно потом стереть, не стирая все остальное.
        print('\nВам нравится такой бонус?')

    def _show(self):
        print('\033[1m' + 'Готовимся выбирать бонусы. . .' + '\033[0m')
        time.sleep(1)
        clear_output(wait=True)

        for key, value in self.bonus.items():
            # Выводим полосу загрузки и подпись под ней
            display(self.progress)
            print('Выбираем бонусы')

            # Обновляем полосу загрузки в течение 2 секунд
            for i in range(1, 21):
                time.sleep(0.15)
                self.progress.value = i / 20

            # Очищаем вывод
            clear_output(wait=True)
            # Выводим бонус
            print('\033[1m' + '\033[92m' + 'Поздравляем! Ваш список бонусов:' + '\033[0m')
            print(f'- {key} ({value} руб)')

        self._show_bonus_summary()
        # Две кнопки, расположенные рядом
        buttons = HBox((self.btn_access, self.btn_reload))
        # Отображаем принт и кнопки
        display(buttons)

    def __start(self):
        # выбираем бонус
        self.bonus = self._get()
        # Выводим сообщения
        self._show()
        # Обработчик событий нажатия на кнопку ЗАНОВО. При нажатии крутит рулетку заново
        self.btn_reload.on_click(self._btn_reload_clicked)
        # Обработчик событий нажатия на кнопку СОХРАНИТЬ. При нажатии на кнопку данные пользователя
        # и его бонус отправляются в гугл таблицу
        self.btn_send.on_click(self._save_data)
        # Обработчик событий нажатия на кнопку ЗАБРОНИРОВАТЬ.
        # При нажатии показывает поля для ввода данных и кнопку СОХРАНИТЬ
        self.btn_access.on_click(self._btn_access_clicked)

    def run(self):
        self.__start()

    def __call__(self, *args, **kwargs):
        self.__start()
