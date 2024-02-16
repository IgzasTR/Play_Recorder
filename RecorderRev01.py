from pynput import mouse, keyboard
from time import time, sleep
import json
import pyautogui

mouse_listener = None
start_time = None
last_coordinate = [0, 0]
# MAUS HASSASİYETİ -- (HASSASİYET ARTTIKÇA DAHA YAVAŞ ÇALIŞIR).
THRESHOLD = 200
upToNow = 0
events = []

def save_json():
    with open('events.json', 'w') as event:
        json.dump(events, event, indent=4)

def on_press(key):
    try:
        save_event(current_time=round(time(), 2), action=0, key=key.char)
        print('Alfanumerik tuş {0} basıldı'.format(key.char))
    except AttributeError:
        save_event(current_time=round(time(), 2), action=0, key=str(key))
        print('Özel tuş {0} basıldı'.format(key))

    # Herhangi bir tuşa basıldığında
    if key != keyboard.Key.cmd:  # Windows tuşu dışındaki tuşlara basıldığında
        if key != keyboard.Key.esc:  # ESC tuşuna basıldığında işlemi sonlandırma
            pyautogui.press('win')  # Windows tuşunu bas
        else:
            stop_listening()  # ESC tuşuna basıldığında dinlemeyi durdur

def stop_listening():
    global mouse_listener
    mouse_listener.stop()
    save_json()
    print('Mouse and Keyboard listener has stopped')

# İzlemeyi durdurmak için klavye dinleyicisini durdurur
def on_release(key):
    if key == keyboard.Key.esc:
        print(time()-start_time)
        stop_listening()
        return False
    save_event(current_time=round(time(), 2), action=1, key=str(key))

def on_move(x, y):
    save_event(current_time=round(time(), 2), action=2, coordinate=[x, y])
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    if pressed:
        save_event(current_time=round(time(), 2), action=3, coordinate=[x, y])
        print('{0} noktasında {1}'.format((x, y), 'Basıldı' if pressed else 'Bırakıldı'))

def on_scroll(x, y, dx, dy):
    save_event(current_time=round(time(), 2), action=4, coordinate=[x, y], direction=('down' if dy < 0 else 'up'))
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

class ActionTypes():
    KEYPRESS = 0
    KEYRELEASE = 1
    MOUSEMOVE = 2
    MOUSECLICK = 3
    MOUSESCROLL = 4

def save_event(current_time, action, key='', coordinate=[], direction='up'):
    global upToNow
    elapsed_time = current_time-start_time
    theduration = round(elapsed_time - upToNow, 2)
    if action == ActionTypes.KEYPRESS:
        info = {'time': theduration, 'action': ActionTypes.KEYPRESS, 'key': key}
    elif action == ActionTypes.KEYRELEASE:
        info = {'time': theduration, 'action': ActionTypes.KEYRELEASE, 'key': key}
    elif action == ActionTypes.MOUSEMOVE:
        global last_coordinate
        if abs(coordinate[0] - last_coordinate[0]) > THRESHOLD or abs(coordinate[1] - last_coordinate[1]) > THRESHOLD:
            info = {'time': 0, 'action': ActionTypes.MOUSEMOVE, 'coordinate': coordinate}
            last_coordinate = coordinate
            events.append(info)
        return
    elif action == ActionTypes.MOUSECLICK:
        info = {'time': theduration, 'action': ActionTypes.MOUSECLICK, 'coordinate': coordinate}
    elif action == ActionTypes.MOUSESCROLL:
        info = {'time': theduration, 'action': ActionTypes.MOUSESCROLL, 'coordinate': coordinate, 'direction': direction}
    upToNow = elapsed_time
    events.append(info)

def settingUpMouseSensitive():
    global THRESHOLD
    print('Hassasiyeti Değiştirmek İster misiniz ? Evet için Y, Hayır için N ye basınız. Hassasiyet arttıkça daha yavaş çalışır.')
    while True:
        print('Fare hassasiyetini belirtin: (Varsayılan: 200)')
        response = input('Y/N').lower()
        if response == 'y':
            try:
                sensitive = int(input('Hassasiyeti Giriniz (0-300):'))
                if 0 <= sensitive <= 300:
                    THRESHOLD = sensitive
                    print(f'Hassasiyet değiştirildi. ({sensitive})')
                    break
                else:
                    print('Lütfen uygun bir değer girin.')
            except:
                print('Lütfen uygun bir değer girin.')
        elif response == 'n':
            print(f'Hassasiyet - {THRESHOLD}')
            break

def run():
    global start_time
    settingUpMouseSensitive()
    input('Herhangi bir tuşa basınız')
    for x in range(4, -1, -1):
        print(x+1)
        sleep(1)
    print('Kayıtta...')
    start_time = round(time(), 2)
    print(start_time)

    events.append({'zaman': 0, 'aksiyon': 'Kayıt Başladı'})
    global mouse_listener

    # Klavye olaylarını dinlemek için bir dinleyici başlatılır
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)

    # Fare olaylarını dinlemek için bir dinleyici başlatılır
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()

    print(events)

if __name__ == '__main__':
    run()

