try:
    from PIL import Image
    from plyer import notification as npa
    from threading import Thread, Event
    from pystray import Icon, MenuItem
    import os
    import pyautogui
    import time
    from datetime import datetime
    from random import randint
except Exception as exp:
    print (f'Error: {exp}')
    exit()
    
WAIT_TIME = 60 # s

class StayAwakeApp():
    
    def __init__(self, action_to_wake=None) -> None:
        self._WS = os.getcwd()
        try:
            self._sleep_img = Image.open(os.path.join(self._WS, "icon\\zzz-sleep-symbol.png"))
            self._allarm_img = Image.open(os.path.join(self._WS, "icon\\alarm-clock.png"))
            self._on_action_img = Image.open(os.path.join(self._WS, "icon\\alarm-clock-on-action.png"))
        except FileNotFoundError:
            print("Files not found in", os.path.join(self._WS, "icon"))
            # npa.notify("Error",
            #     message=f"Files not found in {os.path.join(self._WS, 'icon')}",
            #     timeout = 5)
            exit()
        pass
    
        pyautogui.FAILSAFE = False
        self._current_location = pyautogui.position()
        
        self._action_flag = Event()
        self._thread = Thread(target=self._thread_task, 
                              args=(
                                  self._action_flag,
                                  action_to_wake if action_to_wake else self._do_move,
                                ),
                              daemon=True
                            )

        self._app = Icon("StayAwake", self._sleep_img, menu=self._generate_menu())
        
    def _generate_menu(self):
        toggle_item = MenuItem(
                'Activate' if not self._action_flag.is_set() else "Deactivate",
                self._on_click,
                visible= self._action_flag
            )
        close_item = MenuItem(
                'Close',
                action= lambda : self.stop()
            )
        return [
            toggle_item,
            close_item
        ]
    
    def _on_click(self):
        if not self._action_flag.is_set():
            self._app.icon = self._allarm_img
            self._action_flag.set()
        else:
            self._app.icon = self._sleep_img
            self._action_flag.clear()
        self._app.menu = self._generate_menu()
        
    def _thread_task(self, flag:Event, action_to_wake):
        print(">> Thread started <<")
        try:
            while True:
                if flag.is_set():
                    print('>> Checking')
                    if self._current_location == pyautogui.position():
                        print(">> No manual movement detected >> Triggering stay-awake")
                        self._app.icon = self._on_action_img
                        action_to_wake()
                        self._app.icon = self._allarm_img
                    else:
                        current_location = pyautogui.position()
                        print(f'>> Mouse manually moved from {self._current_location} to {current_location} >> No stay-awake triggered')
                        self._current_location = current_location
                else:
                    pass
                time.sleep(WAIT_TIME)
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def _has_moved(self, currentLocation):
        try:
            time.sleep(randint(0,2))
            if pyautogui.position() == currentLocation:
                return False
            else:
                print('>> Input detected, interrupting stay-awake')
                return True
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def _do_move(self):
        try:
            print(f'>> Moving at {self._current_location}')
            for n_move in range(1, randint(2,4)):
                if self._has_moved(self._current_location):break
                pyautogui.moveTo(self._current_location[0] + n_move, self._current_location[1] + n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] - n_move, self._current_location[1] - n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] - n_move, self._current_location[1] + n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] + n_move, self._current_location[1] - n_move)
                pyautogui.moveTo(self._current_location)
            print(f'>> Made movement at {datetime.now().time()}')
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def run(self):
        self._thread.start()
        self._app.run()
    
    def stop(self):
        self._app.stop()

def press_key(key='capslock'):
    pyautogui.press(key)
    time.sleep(1)
    pyautogui.press(key)

if __name__ == "__main__":
    StayAwakeApp(press_key).run()