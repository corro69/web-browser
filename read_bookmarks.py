import PySimpleGUI as sg
import os
from pathlib import Path

home = str(Path.home())

### WINDOW ###
sg.theme('DarkGray6')

sg.set_options(button_element_size=(12, 1),
               element_padding=(20, 0),
               auto_size_buttons=True,
               border_width=2)

col_layout = [
    [sg.Button("VIEW"),sg.Button("Exit")]
]

layout = [
    [sg.Text("")],
    [sg.Text("BOOKMARKS")],
    [sg.Text(size=(60,20), enable_events=True, key=f'OUTPUT1')],
    {sg.Text("")},
    [sg.Column(col_layout, element_justification='center', expand_x=True)],
]

window = sg.Window("Bookmarks",layout, size=(400,400), finalize=True)
### LOOP

while True:
    event, values = window.read()

    file = open(home + "/.dweb/bookmarks.dat","r")
    read = file.readlines()
    modified = []
    modified1 = []
    modified2 = []
    modified3 = []
    x = []

    for line in read:
        modified.append(line.strip('PyQt5.QtCore.QUrl'))
    for line in modified:
        modified1.append(line.strip("('"))
    for line in modified1:
        modified2.append(line.replace("')",""))
    for line in modified2:
        modified3.append(line.replace("file:///home/dustin/Downloads/web-browser/bookmarks.dat",""))

        with open(home + '/.dweb/bookmarks.dat','w') as writer:
            for x in modified3:
                writer.write(x)
        
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event.startswith("URL "):
        url = event.split(' ')[1]
        dweb.open(url)

    window['OUTPUT1'].update(x)

writer.close()

window.close()