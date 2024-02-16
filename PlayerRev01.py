import pyautogui
import json
import pyperclip
import keyboard
import sys
from time import sleep, time

events = None

SCROLL_SENSITIVE = 135

CHANGE_LETTERS = {
    'alt_l': 'altleft',
    'alt_r': 'altright',
    'alt_gr': 'altright',
    'ctrl_l': 'ctrlleft',
    'ctrl_r': 'ctrlright',
    'shift_l': 'shiftleft',
    'shift_r': 'shiftright',
    'page_down': 'pagedown',
    'page_up': 'pageup',
    'caps_lock': 'capslock',
    'media_volume_down': 'volumedown',
    'media_volume_up': 'volumeup',
    'print_screen': 'printscreen',
    'num_lock': 'numlock',
    'scroll_lock': 'scrolllock'
}

UTF_CHARACTERS = ['ç', 'ı', 'ö', 'ş', 'ğ', 'ü', '@', 'İ', 'é', 'à', 'è', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü', 'ç', 'œ', 'æ', 'ß', 'á', 'í', 'ó', 'ú', 'ñ', '¿', '¡', '€', '£', 'ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü', 'é', 'â', 'ê', 'î', 'ô', 'û', 'è', 'à', 'ù', 'ë', 'ï', 'ü', 'ÿ', 'ç', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'Ä', 'Ë', 'Ï', 'Ö', 'Ü', 'Ÿ', 'Ç', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ã', 'ñ', 'õ', 'ü', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü', 'ç', 'Á', 'É', 'Í', 'Ó', 'Ú', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Ã', 'Ñ', 'Õ', 'Ü', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'Ä', 'Ë', 'Ï', 'Ö', 'Ü', 'Ç']

def ConvertToProperKeys(key):
    properKey = key.replace('Key.', '')
    if properKey in CHANGE_LETTERS.keys():
        return CHANGE_LETTERS[properKey]
    elif properKey in UTF_CHARACTERS:
        pyperclip.copy(properKey)
        pyautogui.hotkey('ctrl', 'v')
        return ''
    return properKey

def load_json():
    global events
    try:
        with open('events.json', 'r') as event:
            events = json.load(event)
    except FileNotFoundError:
        print("Error: events.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in events.json.")
    except Exception as e:
        print("Error:", e)
def play():
    global SCROLL_SENSITIVE
    for x, y in enumerate(events[1:]):
        p = y['time'] - 0.2 # hızlandırılmak istenirse girilebilir bi parametre
        sleep(p if p > 0 else 0)
        if keyboard.is_pressed('esc'):
            print("ESC tuşuna basıldı. Program sonlandırılıyor.")
            return
        if y['action'] == 0:
            if y['key'] == 'cmd':
                pyautogui.press('win')
            else:
                pyautogui.keyDown(ConvertToProperKeys(y['key']))
        elif y['action'] == 1:
            if y['key'] == 'cmd':
                pass  # Windows tuşunu serbest bırakmak için bir şey yapma
            else:
                pyautogui.keyUp(ConvertToProperKeys(y['key']))
        elif y['action'] == 2:
            pyautogui.moveTo(x=y['coordinate'][0], y=y['coordinate'][1])
        elif y['action'] == 3:
            pyautogui.click(x=y['coordinate'][0], y=y['coordinate'][1])
        elif y['action'] == 4:
            pyautogui.scroll(clicks=(SCROLL_SENSITIVE if y['direction'] == 'up' else -SCROLL_SENSITIVE), x=y['coordinate'][0], y=y['coordinate'][1])
def run():
    load_json()
    if events is None:
        print("Error: Events data is not loaded.")
        return

    for x in range(4, -1, -1):
        print(x + 1)
        sleep(1)

    play()

    pyautogui.keyUp('esc')
    print('Bitti...')

if __name__ == '__main__':
    run()
