import customtkinter as ctk
from PIL import Image

# Initialize main application window
app = ctk.CTk()
app.geometry("900x600")  # Set window dimensions
app.title("Restaurant App")  # Set window title

class Item:
    """Represents a menu item with name, price and image path."""
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = "images/" + image  # add image directory path

# Cart tracking item quantities
cart = {
    "hamburger": 0,
    "cheeseburger": 0,
    "veggie wrap": 0,
    "french fries": 0,
    "soft drink": 0
}

# Dynamic text variables for cart quantity displays
cart_text = [ctk.StringVar(value="0") for _ in range(len(cart))]

# Available menu items
ITEMS = [
    Item("hamburger", 5, "hamburger.jpg"),
    Item("cheeseburger", 6, "cheeseburger.jpg"),
    Item("veggie wrap", 4.5, "veggie wrap.jpg"),
    Item("french fries", 2.5, "french fries.jpg"),
    Item("soft drink", 1.5, "soft drink.jpg"),
]

# Mapping of item names to their index positions
ITEMS_INDEX = {item.name: idx for idx, item in enumerate(ITEMS)}

TAX_RATE = 0.15  # Sales tax percentage

row = 0  # Global row counter for grid layout

def update_variables():
    """Sync cart quantities with display variables"""
    for i, item_name in enumerate(cart):
        cart_text[i].set(str(cart[item_name]))

def add_to_cart(item):
    """Add 1 to item quantity (max 5 per item)"""
    if cart[item.name] < 5:
        cart[item.name] += 1
        update_variables()

def remove_from_cart(item):
    """Remove 1 from item quantity (min 0 per item)"""
    if cart[item.name] > 0:
        cart[item.name] -= 1
        update_variables()

def clear_page():
    """Reset UI by destroying all widgets and reinitializing cart"""
    global cart_text
    cart_text = [ctk.StringVar(value="0") for _ in range(len(cart))]
    update_variables()
    for widget in app.winfo_children():
        widget.destroy()

class Button:
    """Custom button widget with grid placement"""
    def __init__(self, text, command, width=1, column=0):
        global row
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.grid(column=column, row=row, columnspan=width, sticky="nsew")
        # Automatically advance row for layout organization
        if column == 2 or width == 2:
            row += 1

class ItemDisplay:
    """Displays menu item information with image"""
    def __init__(self, item, column=1, flat=False):
        global row
        # Load and display item image
        self.image = ctk.CTkImage(Image.open(item.image), size=(100, 100))
        self.label = ctk.CTkLabel(app, image=self.image, text="")
        self.label.grid(column=column, row=row)
        
        # Adjust layout based on display mode
        if not flat:
            row += 1
            
        # Display item name
        self.label = ctk.CTkLabel(app, text=item.name)
        self.label.grid(column=(column+1 if flat else column), row=row)
        
        # Display item price
        self.label = ctk.CTkLabel(app, text=f"${item.price:.2f}")
        self.label.grid(column=(column+2 if flat else column+1), row=row)
        
        if not flat:
            row += 1

class ReactiveLabel:
    """Auto-updating label bound to StringVar"""
    def __init__(self, variable, column=1):
        global row
        self.variable = variable
        self.label = ctk.CTkLabel(app, textvariable=variable)
        self.label.grid(column=column, row=row)

class Label:
    """Simple static text label"""
    def __init__(self, text, width=1, column=1):
        global row
        self.label = ctk.CTkLabel(app, text=text)
        self.label.grid(column=column, row=row, columnspan=width)

class ItemWidget:
    """Complete menu item UI with quantity controls"""
    def __init__(self, item, index, item_columns):
        global row
        # Calculate column position based on grid layout
        column = 3 * (index % item_columns)
        
        # Display item information
        ItemDisplay(item, column=column+1)
        
        # Create quantity controls
        decrease_button = Button("-", lambda: remove_from_cart(item), column=column)
        ReactiveLabel(cart_text[index], column=column + 1)
        increase_button = Button("+", lambda: add_to_cart(item), column=column + 2)

        # Store original button color for state changes
        original_color = increase_button.button.cget("fg_color")

        def update_button_state():
            """Enable/disable buttons based on quantity limits"""
            value = cart_text[index].get()
            # Disable decrease button at minimum quantity
            if int(value) == 0:
                decrease_button.button.configure(state="disabled", fg_color="grey")
            else:
                decrease_button.button.configure(state="normal", fg_color=original_color)
            
            # Disable increase button at maximum quantity
            if int(value) == 5:
                increase_button.button.configure(state="disabled", fg_color="grey")
            else:
                increase_button.button.configure(state="normal", fg_color=original_color)

        # Automatically update button states when quantity changes
        cart_text[index].trace_add("write", lambda *args: update_button_state())

        # Adjust grid row position for next item
        if index % item_columns == 0:
            row -= 3
        else:
            row += 1

def order_page():
    """Main menu page with item selection"""
    global row
    # Configure grid columns
    app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    clear_page()
    row = 0

    # Display page title
    Label("Menu", width=2, column=2)
    row += 1

    # Display all menu items
    for item in ITEMS:
        ItemWidget(item, ITEMS.index(item), 2)  # 2 items per row

    row += 3
    # Create checkout button
    checkout = Button("View Order", lambda: checkout_page(), width=2, column=2)

    def update_checkout_button_state():
        """Enable checkout only when items are in cart"""
        checkout.button.configure(
            state="normal" if any(cart.values()) else "disabled",
            fg_color="green" if any(cart.values()) else "grey"
        )

    # Update checkout button state when cart changes
    for text_var in cart_text:
        text_var.trace_add("write", lambda *args: update_checkout_button_state())
    update_variables()

def checkout_page():
    """Order summary page with pricing calculations"""
    global row
    row = 0
    clear_page()

    # Page header
    Label("Order Summary", width=2, column=1)
    row += 1

    # Column headers
    Label("Checkout", column=0)
    Label("Item", column=1)
    Label("Price", column=2)
    Label("Quantity", column=3)
    Label("Totals", column=4)
    row += 1
    
    # Display cart items with quantities > 0
    for item_name, quantity in cart.items():
        if quantity > 0:
            item = ITEMS[ITEMS_INDEX[item_name]]
            # Display item in row format
            ItemDisplay(item, column=0, flat=True)
            ReactiveLabel(cart_text[ITEMS_INDEX[item_name]], column=3)
            Label(f"${quantity * item.price:.2f}", column=4)
            row += 1
    
    # Calculate pricing breakdown
    subtotal = sum(quantity * ITEMS[ITEMS_INDEX[name]].price for name, quantity in cart.items())
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    # Display pricing information
    Label("Subtotal", column=3)
    Label(f"${subtotal:.2f}", column=4)
    row += 1
    Label("Tax (15%)", column=3)
    Label(f"${tax:.2f}", column=4)
    row += 1
    Label("Total", column=3)
    Label(f"${total:.2f}", column=4)
    row += 1

    # Navigation buttons
    Button("Back", lambda: order_page(), width=2, column=2)
    row += 1
    Button("Finalize", lambda: done(), width=2, column=2)

def done():
    """Terminate application"""
    app.quit()

# Application entry point
if __name__ == "__main__":
    order_page()  # Start with order page
    app.mainloop()  # Start GUI event loop