import ipywidgets as widgets


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
