from RPALite import RPALite
rpalite = RPALite()

# Show the desktop
rpalite.show_desktop()

# Open Firefox browser
rpalite.run_command("firefox")

# Wait for Firefox to open and then navigate to a website
rpalite.sleep(3)
rpalite.input_text("https://www.deepseek.com")
rpalite.send_keys("{ENTER}")

# Wait for page to load
rpalite.sleep(5)

# Find and close the Firefox application
app = rpalite.find_application("Firefox")
if app:
    rpalite.close_app(app)
