from RPALite import RPALite
rpalite = RPALite()

# Show the desktop
rpalite.show_desktop()

# Open Notepad and type a text
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# Find the notepad application and close it
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
