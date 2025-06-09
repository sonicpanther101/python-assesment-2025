# python-assesment-2025

## Achieved parts

### Programming Functionality
- It displays a menu
- It allows the user to select items and quantities.
- It calculates a total cost.
- It shows an order summary.
- It has a GUI interface
- No Critical Bugs: The program doesn't crash or get stuck when performing the basic, expected operations.
- Output Matches Basic Expectations: The output (menu, order summary) is understandable and contains the correct information for a standard order.

### Code Presence and execution
- Code is provided and is runnable with the correct packages installed
- Code executes
- Code is written in python and uses fundamental programming constructs

### Addressing Specific Task Features
- Menu is displayed
- Order inputs are functional
- Orders are calculated correctly
- Output is displayed
- GUI interface includes labels, buttons and reactive labels
- I used classes
- Constants are used defining the items
- Code has relevant comments

### Object-Oriented Programming
- I have defined more than 2 classes to store widgets and item info
- I have created instances of each class
- In the itemWidget class I have an init function and an updateButtonState function. I have not included more than that because it was uneccesarry in this assesment.
- Objects (classes) interact with one another using functions

### GUI
- Custom tkinter GUI framework used for a modern looking style over regular tkinter
- GUI includes basic widgets
- Includes basic event handling with traces attached to tkinter string variables

### Data Structures Beyond Simple Variables
- Lists to store the cart items
- Item class to store item info

### Basic Input Validation
- As actually good code does not allow users to input the incorrect type I have made it a button only GUI. This doesn't allow the user to give an incorrect type input.
- Using try and except is useful in debuging, however it should never be included in production code, therefore I have not left any in my code, though they were used for debuging purposes.
- I have used adaptive disabling of the buttons to prevent the user from going out of the range of 0 <= x <= 5

### Constants
- Constants are used defining the items