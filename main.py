import customtkinter as ctk
from PIL import Image


app = ctk.CTk()
app.geometry("900x600")
app.title("Restaurant App")


class Item:
    """Represents a menu item with name, price and image path."""
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = "images/" + image


# Tracks quantities of items in shopping cart
cart = {
    "hamburger": 0,
    "cheeseburger": 0,
    "veggie wrap": 0,
    "french fries": 0,
    "soft drink": 0
}

# String variables for dynamic cart quantity display
cart_text = [ctk.StringVar(value="0") for _ in range(len(cart))]

# Available menu items
ITEMS = [
    Item("hamburger", 5, "hamburger.jpg"),
    Item("cheeseburger", 6, "cheeseburger.jpg"),
    Item("veggie wrap", 4.5, "veggie wrap.jpg"),
    Item("french fries", 2.5, "french fries.jpg"),
    Item("soft drink", 1.5, "soft drink.jpg"),
]

# Maps item names to their index positions
ITEMS_INDEX = {item.name: idx for idx, item in enumerate(ITEMS)}

TAX_RATE = 0.15

# Tracks current grid row in GUI
row = 0


def update_variables():
    """Updates all cart quantity displays."""
    for i, item_name in enumerate(cart):
        cart_text[i].set(str(cart[item_name]))


def add_to_cart(item):
    """Adds item to cart (max 5)."""
    if cart[item.name] < 5:
        cart[item.name] += 1
        update_variables()


def remove_from_cart(item):
    """Removes item from cart (min 0)."""
    if cart[item.name] > 0:
        cart[item.name] -= 1
        update_variables()


def clear_page():
    """Clears all widgets from current page."""
    global cart_text
    cart_text = [ctk.StringVar(value="0") for _ in range(len(cart))]
    update_variables()
    for widget in app.winfo_children():
        widget.destroy()


class Button:
    """Creates button widget with grid placement."""
    def __init__(self, text, command, width=1, column=0):
        global row
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.grid(column=column, row=row, columnspan=width, sticky="nsew")
        if column == 2 or width == 2:
            row += 1


class ItemDisplay:
    """Displays menu item information (image, name, price)."""
    def __init__(self, item, column=1, flat=False):
        global row
        self.image = ctk.CTkImage(Image.open(item.image), size=(100, 100))
        self.label = ctk.CTkLabel(app, image=self.image, text="")
        self.label.grid(column=column, row=row)
        
        if not flat:
            row += 1
            
        self.label = ctk.CTkLabel(app, text=item.name)
        self.label.grid(column=(column+1 if flat else column), row=row)
        
        self.label = ctk.CTkLabel(app, text=f"${item.price:.2f}")
        self.label.grid(column=(column+2 if flat else column+1), row=row)
        
        if not flat:
            row += 1


class ReactiveLabel:
    """Label that automatically updates with StringVar changes."""
    def __init__(self, variable, column=1):
        global row
        self.variable = variable
        self.label = ctk.CTkLabel(app, textvariable=variable)
        self.label.grid(column=column, row=row)


class Label:
    """Simple static text label."""
    def __init__(self, text, width=1, column=1):
        global row
        self.label = ctk.CTkLabel(app, text=text)
        self.label.grid(column=column, row=row, columnspan=width)


class ItemWidget:
    """Combined widget for item display with quantity controls."""
    def __init__(self, item, index, item_columns):
        global row

        column = 3 * (index % item_columns)
        ItemDisplay(item, column=column+1)
        decrease_button = Button("-", lambda: remove_from_cart(item), column=column)
        ReactiveLabel(cart_text[index], column=column + 1)
        increase_button = Button("+", lambda: add_to_cart(item), column=column + 2)

        original_color = increase_button.button.cget("fg_color")

        def update_button_state():
            """Updates button states based on quantity limits."""
            value = cart_text[index].get()
            if int(value) == 0:
                decrease_button.button.configure(state="disabled", fg_color="grey")
            else:
                decrease_button.button.configure(state="normal", fg_color=original_color)
                
            if int(value) == 5:
                increase_button.button.configure(state="disabled", fg_color="grey")
            else:
                increase_button.button.configure(state="normal", fg_color=original_color)

        cart_text[index].trace_add("write", lambda *args: update_button_state())

        if index % item_columns == 0:
            row -= 3
        else:
            row += 1

def order_page():
    """Main menu page with item selection."""
    global row
    app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    clear_page()
    row = 0

    Label("Menu", width=2, column=2)
    row += 1

    for item in ITEMS:
        ItemWidget(item, ITEMS.index(item), 2)

    row += 3
    checkout = Button("View Order", lambda: checkout_page(), width=2, column=2)

    def update_checkout_button_state():
        """Enables checkout button when items are in cart."""
        if any(cart.values()):
            checkout.button.configure(state="normal", fg_color="green")
        else:
            checkout.button.configure(state="disabled", fg_color="grey")

    for text_var in cart_text:
        text_var.trace_add("write", lambda *args: update_checkout_button_state())
    update_variables()


def checkout_page():
    """Displays order summary with pricing."""
    global row
    row = 0
    clear_page()

    Label("Order Summary", width=2, column=1)
    row += 1

    Label("Checkout", column=0)
    Label("Item", column=1)
    Label("Price", column=2)
    Label("Quantity", column=3)
    Label("Totals", column=4)
    row += 1
    
    # Show only items with quantity > 0
    for item_name, quantity in cart.items():
        if quantity > 0:
            item = ITEMS[ITEMS_INDEX[item_name]]
            ItemDisplay(item, column=0, flat=True)
            ReactiveLabel(cart_text[ITEMS_INDEX[item_name]], column=3)
            Label(f"${quantity * item.price:.2f}", column=4)
            row += 1
    
    # Calculate pricing
    subtotal = sum(quantity * ITEMS[ITEMS_INDEX[name]].price for name, quantity in cart.items())
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    Label("Subtotal", column=3)
    Label(f"${subtotal:.2f}", column=4)
    row += 1
    Label("Tax (15%)", column=3)
    Label(f"${tax:.2f}", column=4)
    row += 1
    Label("Total", column=3)
    Label(f"${total:.2f}", column=4)
    row += 1

    Button("Back", lambda: order_page(), width=2, column=2)
    row += 1
    Button("Finalize", lambda: done(), width=2, column=2)


def done():
    """Exits application."""
    app.quit()


if __name__ == "__main__":
    order_page()
    app.mainloop()