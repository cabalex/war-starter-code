import PySimpleGUI as sg


def make_window(window=None, justification='left', element_justification='left',
    vertical_alignment='top', expand_x=True, expand_y=True):


    column_layout = [
        [sg.Text("(0, 0)", text_color='black', background_color='yellow'),
         sg.Text("(0, 1)", text_color='black', background_color='green')],
        [sg.Text("(1, 0)", text_color='black', background_color='red'),
         sg.Text("(1, 1)", text_color='black', background_color='blue')],
    ]

    layout = [
        [
         sg.Column([[sg.Text("Fixed Column")]], size=(200, 200), background_color='blue'),
         sg.Column(
            column_layout,
            justification=justification,
            element_justification=element_justification,
            expand_x=expand_x,
            expand_y=expand_y,
            vertical_alignment=vertical_alignment,
            background_color='gray',
            key='Column'),
         ],
    ]

    radios = []
    for group, text in [
            ("justification", ("left", "center", "right")),
            ("element_justification", ("left", "center", "right")),
            ("vertical_alignment", ("top", "center", "bottom")),
            ("expand_x", (True, False)),
            ("expand_y", (True, False))]:
        row = []
        row.append(sg.Text(group, size=(25, 1)))
        for i, value in enumerate(text):
            row.append(sg.Radio(str(value), group, default=eval(f"{group}==value"), size=(6, 1),  enable_events=True, key=(group, value)))
        radios.append(row)

    layout += radios
    win = sg.Window(title="Lights", layout=layout, size=(800, 400), margins=(0, 0), finalize=True)
    if window:
        window.close()
    return win


sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 12))

window = make_window()
justification, element_justification, vertical_alignment, expand_x, expand_y = (
    'left', 'left', 'top', True, True)

while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif isinstance(event, tuple):
        radio = event[0]
        if radio == 'justification':
            justification = event[1]
        elif radio == 'element_justification':
            element_justification = event[1]
        elif radio == 'vertical_alignment':
            vertical_alignment = event[1]
        elif radio == 'expand_x':
            expand_x = event[1]
        elif radio == 'expand_y':
            expand_y = event[1]

        window = make_window(window, justification=justification,
            element_justification=element_justification,
            vertical_alignment=vertical_alignment, expand_x=expand_x,
            expand_y=expand_y)

window.close()
