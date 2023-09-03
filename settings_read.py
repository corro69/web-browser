from configparser import ConfigParser
from fileinput import close
from optparse import Values
from pathlib import Path

config = ConfigParser()
config.read("dweb-settings.ini")

#print(config.get('USER_settings',"user_homepage_url"))
#print(config.get('USER_settings','user_default_font-size'))
#print(config.get('USER_settings','user_background-color'))
#print(config.get('USER_settings','user_color'))
#print(config.get('USER_settings','user_font-size'))

#print(config.sections())

x = (config.get('USER_settings',"user_homepage_url"))
y = (config.get('USER_settings','user_default_font-size'))
z = (config.get('USER_settings','user_background-color'))
xx = (config.get('USER_settings','user_color'))
yy = (config.get('USER_settings','user_font-size'))

if x != "https://google.com":
    homepage_url = x
if y != (config.get("'DEFAULT_settings','default_font-size'")):
    pass

#homepage_url = x
default_font_size = y
style_sheet = """
            background-color: #3b393c;
            color: #f7f7f5;
            font-size:20px;
            """

print(homepage_url)