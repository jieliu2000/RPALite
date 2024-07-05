from RPALite import RPALite
rpalite = RPALite()

# Press Windows + D to show the desktop
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")

# Open Notepad and type a text
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# Find the notepad application and close it
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
