import time
from pynput.keyboard import Key, Listener
def record_keystrokes():
    # Generate a unique user ID for the user


    # Initialize the keystroke dictionary
    keystrokes = {'presses': [], 'releases': []}

    # Define the key press and release event handlers
    def on_press(key, event_time):
        if key == Key.esc:
            return False
        keystrokes['presses'].append(key)
        return None

    def on_release(key, event_time):
        if key == Key.esc:
            return False
        keystrokes['releases'].append(key)
        return None

    # Start capturing keystrokes for the specified user
    with Listener(on_press=lambda k: on_press(k, time.time()),
                  on_release=lambda k: on_release(k, time.time())) as listener:
  
        listener.join()


    return keystrokes