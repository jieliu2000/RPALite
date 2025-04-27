#!/usr/bin/env python3
"""
RPALite macOS Calculator Demo

This script demonstrates how to use RPALite to automate tasks on macOS.
It will open the Calculator app, perform a simple calculation, and copy the result.

=== Running the Example ===

Before running this example, you must grant necessary permissions:

1. System Settings > Privacy & Security > Screen Recording:
   - Add Terminal or Visual Studio Code (depending on where you're running this)
   
2. System Settings > Privacy & Security > Accessibility:
   - Add Terminal or Visual Studio Code (depending on where you're running this)

3. System Settings > Privacy & Security > Automation:
   - You'll be prompted to grant automation permissions when the script runs

=== Terminal Instructions ===

To run this example in Terminal:
1. Open Terminal (Applications > Utilities > Terminal)
2. Navigate to the example directory:
   ```
   cd path/to/examples/python
   ```
3. Run the script:
   ```
   python calculator_macos.py
   ```
4. If prompted for permissions, click "OK" to allow

=== VSCode Instructions ===

To run this example in VSCode:
1. Open VSCode and this file
2. Make sure VSCode has required permissions (see above)
3. Open the terminal in VSCode or use the Run button
4. If using the terminal, run:
   ```
   python calculator_macos.py
   ```
5. If prompted for permissions, click "OK" to allow

=== Troubleshooting ===

If the example doesn't work:
- Ensure Terminal/VSCode has proper permissions
- Try restarting Terminal/VSCode after granting permissions
- If you're running Python directly (not through Terminal/VSCode), add Python to permissions
"""

from RPALite import RPALite

# Initialize RPALite
rpalite = RPALite() 

try:
    # Launch Calculator
    print("Launching Calculator...")
    rpalite.run_command("Calculator")
    
    # Clear any previous calculations (press 'Clear' or 'AC' button)
    print("Clearing calculator...")
    rpalite.click_by_text("AC")  # For newer macOS Calculator
    # If the above doesn't work, try these alternatives:
    # rpalite.click_text("Clear")  # For older macOS Calculator
    # rpalite.click_text("C")      # Another possible label
    
    # Perform a simple calculation: 5 + 3 = 8
    print("Performing calculation: 5 + 3...")
    rpalite.click_by_text("5")
    rpalite.click_by_text("+")
    rpalite.click_by_text("3")
    rpalite.click_by_text("=")
    
    # Copy the result to clipboard
    print("Copying result to clipboard...")
    rpalite.click_text("Edit")
    rpalite.click_text("Copy")
    
    # Get the result from clipboard
    result = rpalite.get_clipboard_text()
    print(f"Calculation result: {result}")
    
    # Verify the result
    if result.strip() == "8":
        print("Test passed! The calculation result is correct.")
    else:
        print(f"Test failed! Expected '8', but got '{result.strip()}'")
    
    # Close Calculator using keyboard shortcut
    print("Closing Calculator...")
    rpalite.send_keys("^q")  # Command+Q on macOS
    
except Exception as e:
    print(f"An error occurred: {e}")
    print("Check that you've granted all required permissions.")
    
finally:
    print("Demo completed.") 