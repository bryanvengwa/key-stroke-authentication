from pynput.keyboard import Key, Listener

# Define a function to handle keystroke events
def on_press(key):
    try:
        # Print the pressed key
        print('Key {} pressed'.format(key))
    except AttributeError:
        # Ignore special keys
        pass

# Define a function to handle key release events
def on_release(key):
    # If the ESC key is pressed, stop the listener
    if key == Key.esc:
        return False

# Create a listener to monitor keystrokes
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Start listening for events
    listener.join()
