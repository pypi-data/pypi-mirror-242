import abc
import ipywidgets as widgets


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


def text_input(placeholder, description, value='', disabled=False):
    return widgets.Text(
        value=value,
        placeholder=placeholder,
        description=description,
        disabled=disabled
    )


def btn(description, style, tooltip, icon='check', disabled=False):
    return widgets.Button(
        description=description,
        disabled=disabled,
        button_style=style,
        tooltip=tooltip,
        icon=icon
    )


def progress_bar(value=0.0, min_value=0.0, max_value=1.0):
    return widgets.FloatProgress(value=value,
                                 min=min_value,
                                 max=max_value)
