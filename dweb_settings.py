from configparser import ConfigParser
from curses import window
from optparse import Values
import PySimpleGUI as sg
from pathlib import Path

home = str(Path.home())


sg.theme('DarkGray6')

sg.set_options(button_element_size=(12, 1),
               element_padding=(20, 0),
               auto_size_buttons=True,
               border_width=2)

col_layout = [
    [sg.Button("Save"),sg.Button("Exit")]
]

layout=[
    [sg.Text("")],
    [sg.Text("Homepage URL:"), sg.Text(size=(40,1), key='OUTPUT1')],
    [sg.InputText()],
    [sg.Text("")],    
    [sg.Text("Default Font Size:"), sg.Text(size=(40,1), key='OUTPUT2')], 
    [sg.InputText()], 
    [sg.Text("")],
    [sg.Text("Background Color:"), sg.Text(size=(40,1), key='OUTPUT3')], 
    [sg.InputText()],
    [sg.Text("")],
    [sg.Text("Color:     "), sg.Text(size=(40,1), key='OUTPUT4')], 
    [sg.InputText()],
    [sg.Text("")],
    [sg.Text("Font Size:"), sg.Text(size=(40,1), key='OUTPUT5')], 
    [sg.InputText()],     
    [sg.Text("")],
    [sg.Text("")],
    [sg.Column(col_layout, element_justification='center', expand_x=True)],
]

window = sg.Window("Dweb Settings",layout, size=(400,400))

config = ConfigParser()

## homepage_url = "https://www.google.com"
## default_font_size = 22
## style_sheet = """
##            background-color: #3b393c;
##            color: #f7f7f5;
##            font-size:22px;
##            """

config['Default_settings'] = {
    "homepage_url": 'https://www.google.com',
    "default_font-size": "22",
    "background-color": "#""3b39c",
    "color": "#""f7f7f5",
    "font-size": "22""px",
}

def Save_Data():
    x = values[0]
    y = values[1]
    z = values[2]
    xx = values[3]
    yy = values[4]

    config['USER_settings'] = {
        "user_homepage_url": x,
        "user_default_font-size": y,
        "user_background-color":  z,
        "user_color":  xx,
        "user_font-size": yy,
    }

    with open(home +"/git/web-browser/dweb-settings.ini","w") as f:
        config.write(f)

#    import settings_read

    window['OUTPUT1'].update(x)
    window['OUTPUT2'].update(y)
    window['OUTPUT3'].update(z)
    window['OUTPUT4'].update(xx)
    window['OUTPUT5'].update(yy)

def load_data():
    config.read(home + "/git/web-browser/dweb-settings.ini") 

def Print_Data():
        config_data = config.read[home + "/git/web-browser/dweb-settings.ini"]
        print(config_data)

while True:
    event, values = window.read()

    load_data()
    
    if event == "Save":
        Save_Data()
#        break
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
