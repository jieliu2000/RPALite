from RPALite import RPALite
rpalite = RPALite()

# Show the desktop
rpalite.show_desktop()

# Open Notepad and type a text
rpalite.run_command("firefox")
rpalite.input_text("https://www.deepseek.com")

rpalite.close_app(app)
