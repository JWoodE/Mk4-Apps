"""Fridge Temperature homescreen

This is a homescreen that includes Temperature
of the beer Fridge.
"""

___name___         = "Homescreen (Temp)"
___license___      = "MIT"
___categories___   = ["Homescreens"]
___dependencies___ = ["homescreen", "shared/logo.png", "shared/sponsors.png", "wifi", "http", "sleep"]
___launchable___   = False
___bootstrapped___ = True

import ugfx
from homescreen import *
import time
from tilda import Buttons
import wifi, http, sleep

# We ❤️ our sponsors
init()
ugfx.display_image(0, 0, "shared/sponsors.png")
wait_until = time.ticks_ms() + 3000
while time.ticks_ms() < wait_until:
    time.sleep(0.1)
    if Buttons.is_pressed(Buttons.BTN_A) or Buttons.is_pressed(Buttons.BTN_B) or Buttons.is_pressed(Buttons.BTN_Menu):
        break

# Padding for name
intro_height = 30
intro_text = "Hi! I'm"
name_height = 60
status_height = 20
info_height = 30
logo_path = "shared/logo.png"
logo_height = 150
logo_width = 56

# Maximum length of name before downscaling
max_name = 8

# Colour stuff
style = ugfx.Style()
style.set_enabled([ugfx.WHITE, ugfx.html_color(0x800080), ugfx.html_color(0x800080), ugfx.html_color(0x800080)])
style.set_background(ugfx.html_color(0x800080))
ugfx.set_default_style(style)

def paint_screen():
    global status

    # Background stuff
    ugfx.clear(ugfx.html_color(0x800080))

    # Logo stuff
    ugfx.display_image(
        int((ugfx.width() - logo_width) / 2),
        int((ugfx.height() - logo_height) / 2),
        logo_path
    )

    # Draw for people to see
    ugfx.orientation(90)
    # Draw introduction
    ugfx.set_default_font(ugfx.FONT_TITLE)
    ugfx.Label(0, ugfx.height() - name_height - intro_height, ugfx.width(), intro_height, intro_text, justification=ugfx.Label.CENTER)
    # Process name
    name_setting = name("Set your name in the settings app")
    if len(name_setting) <= max_name:
        ugfx.set_default_font(ugfx.FONT_NAME)
    else:
        ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
    # Draw name
    ugfx.Label(0, ugfx.height() - name_height, ugfx.width(), name_height, name_setting, justification=ugfx.Label.CENTER)

    # Draw for wearer to see
    ugfx.orientation(270)
    # Title
    ugfx.set_default_font(ugfx.FONT_TITLE)
    ugfx.Label(0, ugfx.height() - info_height * 2, ugfx.width(), info_height, "TiLDA Mk4", justification=ugfx.Label.CENTER)
    # info
    ugfx.Label(0, ugfx.height() - info_height, ugfx.width(), info_height, "Long Press MENU", justification=ugfx.Label.CENTER)

    ugfx.set_default_font(ugfx.FONT_SMALL)
    status = ugfx.Label(0, ugfx.height() - info_height * 2 - status_height, ugfx.width(), status_height, "", justification=ugfx.Label.CENTER)

    Buttons.enable_interrupt(Buttons.BTN_B, lambda button_id:get_temp(), on_press=True, on_release=False)

def get_temp():
    global value_wifi_strength, value_temp

    if not wifi.is_connected():
        wifi.connect(show_wait_message=True)
    paint_screen()
    if wifi.is_connected():
        value_wifi_strength = wifi_strength()
        value_temp = http.get("http://ipswichmakerspace.mooo.com/temp.txt").raise_for_status().content

value_wifi_strength = 0
value_temp = 0.00
get_temp()

# update loop
while True:
    text = "";
    value_battery = battery()
    if value_wifi_strength:
        text += "W: %s%%, " % int(value_wifi_strength)
    if value_battery:
        text += "B: %s%%, " % int(value_battery)
    if value_temp:
        text += '{} {:.7}'.format("T: ", value_temp)
    status.text(text)
    sleep_or_exit(0.5)
