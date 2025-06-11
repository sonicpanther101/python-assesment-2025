import customtkinter as ctk
from PIL import Image

app = ctk.CTk()
app.geometry("900x600")
app.title("Reseraunt App")

# Represents a menu item with name, price and image path
class item:
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
cartText = [ctk.StringVar(value="0") for _ in range(len(cart))]

# Updates all cart quantity displays
def updateVariables():
    for i, item in enumerate(cart):
        cartText[i].set(str(cart[item]))
    
# Available menu items
ITEMS = [
    item("hamburger", 5, "hamburger.jpg"),
    item("cheeseburger", 6, "cheeseburger.jpg"),
    item("veggie wrap", 4.5, "veggie wrap.jpg"),
    item("french fries", 2.5, "french fries.jpg"),
    item("soft drink", 1.5, "soft drink.jpg"),
]

# Maps item names to their index positions
ITEMS_INDEX = {
    "hamburger": 0,
    "cheeseburger": 1,
    "veggie wrap": 2,
    "french fries": 3,
    "soft drink": 4
}

TAX_RATE = 0.15

# Tracks current grid row in GUI
row = 0

# Adds item to cart (max 5)
def addToCart(item):
    if cart[item.name] == 5:
        return
    cart[item.name] += 1
    updateVariables()

# Removes item from cart (min 0)
def removeFromCart(item):
    if cart[item.name] == 0:
        return
    cart[item.name] -= 1
    updateVariables()

# Creates button widget with grid placement
class button:
    def __init__(self, text, command, width = 1, column = 0):
        global row
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.grid(column=column, row=row, columnspan=width, sticky="nsew")
        if column == 2 or width == 2:
            row += 1

# Displays menu item information (image, name, price)
class itemDisplay:
    def __init__(self, item, column = 1, flat = False):
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

# Label that automatically updates with StringVar changes
class reactiveLabel:
    def __init__(self, variable, column = 1):
        global row
        self.variable = variable
        self.label = ctk.CTkLabel(app, textvariable=variable)
        self.label.grid(column=column, row=row)

# Simple static text label
class label:
    def __init__(self, text, width = 1, column = 1):
        global row
        self.label = ctk.CTkLabel(app, text=text)
        self.label.grid(column=column, row=row, columnspan=width)

# Combined widget for item display with quantity controls
class itemWidget:
    def __init__(self, item, index, itemColumns):
        global row

        column = 3*(index % itemColumns)

        itemDisplay(item, column = column+1)
        decreaseButton = button("-", lambda: removeFromCart(item), column = column)
        reactiveLabel(cartText[index], column = column + 1)
        increaseButton = button("+", lambda: addToCart(item), column = column + 2)

        originalColor = increaseButton.button.cget("fg_color")

        # Updates button states based on quantity limits
        def updateButtonState():
            value = cartText[index].get()
            if int(value) == 0:
                decreaseButton.button.configure(state="disabled")
                decreaseButton.button.configure(fg_color="grey")
            elif int(value) == 5:
                increaseButton.button.configure(state="disabled")
                increaseButton.button.configure(fg_color="grey")
            else:
                increaseButton.button.configure(state="normal")
                increaseButton.button.configure(fg_color=originalColor)

                decreaseButton.button.configure(state="normal")
                decreaseButton.button.configure(fg_color=originalColor)

        cartText[index].trace_add("write", lambda *args: updateButtonState())

        if index % itemColumns == 0:
            row -= 3
            pass
        else:
            row += 1
            pass

# Clears all widgets from current page
def clearPage():
    global cartText
    cartText = [ctk.StringVar(value="0") for _ in range(len(cart))]
    updateVariables()
    for widget in app.winfo_children():
        widget.destroy()

# Main menu page with item selection
def orderPage():
    global row, traceIDs
    app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    clearPage()

    row = 0

    label("Menu", width = 2, column = 2)

    row += 1

    for item in ITEMS:
        itemWidget(item, ITEMS.index(item), 2)

    row += 3

    checkout = button("View Order", lambda: checkoutPage(), width = 2, column = 2)

    # Enables checkout button when items are in cart
    def updateCheckoutButtonState():
        for item in cart:
            if cart[item] > 0:
                checkout.button.configure(state="normal")
                checkout.button.configure(fg_color="green")
                break
            else:
                checkout.button.configure(state="disabled")
                checkout.button.configure(fg_color="grey")

    for i in range(len(cartText)):
        cartText[i].trace_add("write", lambda *args: updateCheckoutButtonState())
    updateVariables()

# Displays order summary with pricing
def checkoutPage():
    global row
    row = 0
    clearPage()

    label("Order Summary", width = 2, column = 1)

    row += 1

    label("Checkout", column = 0)
    label("Item", column = 1)
    label("Price", column = 2)
    label("Quantity", column = 3)
    label("Totals", column = 4)

    row += 1
    
    # Show only items with quantity > 0
    for item in cart:
        if cart[item] > 0:
            itemDisplay(ITEMS[ITEMS_INDEX[item]], column = 0, flat = True)
            reactiveLabel(cartText[ITEMS_INDEX[item]], column = 3)
            # quantity times price
            label(f"${cart[item] * ITEMS[ITEMS_INDEX[item]].price:.2f}", column = 4)

            row += 1
    
    # Calculate pricing
    subtotal = 0
    for item in cart:
        subtotal += cart[item] * ITEMS[ITEMS_INDEX[item]].price
    tax = subtotal * TAX_RATE
    total = subtotal + tax


    label("Subtotal", column = 3)
    label(f"${subtotal:.2f}", column = 4)
    row += 1
    label("Tax (15%)", column = 3)
    label(f"${tax:.2f}", column = 4)
    row += 1
    label("Total", column = 3)
    label(f"${total:.2f}", column = 4)
    row += 1

    button("Back", lambda: orderPage(), width = 2, column = 2)

    row += 1

    button("Finalise", lambda: Done(), width = 2, column = 2)

# Exits application
def Done():
    app.quit()

if __name__ == "__main__":
    orderPage()
    app.mainloop()