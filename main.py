import customtkinter as ctk
from PIL import Image

app = ctk.CTk()
app.geometry("900x600")
app.title("Reseraunt App")

class item:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = "images/" + image

global cart
cart = {
    "hamburger": 0,
    "cheeseburger": 0,
    "veggie wrap": 0,
    "french fries": 0,
    "soft drink": 0
}

cartText = [ctk.StringVar(value="0") for _ in range(len(cart))]

def updateVariables():
    for i, item in enumerate(cart):
        cartText[i].set(str(cart[item]))
    
global ITEMS
ITEMS = [
    item("hamburger", 5, "hamburger.jpg"),
    item("cheeseburger", 6, "cheeseburger.jpg"),
    item("veggie wrap", 4.5, "veggie wrap.jpg"),
    item("french fries", 2.5, "french fries.jpg"),
    item("soft drink", 1.5, "soft drink.jpg"),
]

row = 0

def addToCart(item):
    if cart[item.name] == 5:
        return
    cart[item.name] += 1
    updateVariables()

def removeFromCart(item):
    if cart[item.name] == 0:
        return
    cart[item.name] -= 1
    updateVariables()

class button:
    def __init__(self, text, command, width = 1, column = 0):
        global row
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.grid(column=column, row=row, columnspan=width, sticky="nsew")
        if column == 2 or width == 2:
            row += 1

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

class reactiveLabel:
    def __init__(self, variable, column = 1):
        global row
        self.variable = variable
        self.label = ctk.CTkLabel(app, textvariable=variable)
        self.label.grid(column=column, row=row)

class label:
    def __init__(self, text, column = 1):
        global row
        self.label = ctk.CTkLabel(app, text=text)
        self.label.grid(column=column, row=row)

class itemWidget:
    def __init__(self, item, index, itemColumns):
        global row

        column = 3*(index % itemColumns)

        itemDisplay(item, column = column+1)
        decreaseButton = button("-", lambda: removeFromCart(item), column = column)
        decreaseButton.button.configure(state="disabled")
        decreaseButton.button.configure(fg_color="grey")
        reactiveLabel(cartText[index], column = column + 1)
        increaseButton = button("+", lambda: addToCart(item), column = column + 2)

        originalColor = increaseButton.button.cget("fg_color")

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

def clearPage():
    for widget in app.winfo_children():
        widget.destroy()

def orderPage():
    global row
    app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    clearPage()
    updateVariables()

    row = 0

    for item in ITEMS:
        itemWidget(item, ITEMS.index(item), 2)

    row += 3

    checkout = button("Checkout", lambda: checkoutPage(), width = 2, column = 2)
    checkout.button.configure(state="disabled")
    checkout.button.configure(fg_color="grey")

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

def checkoutPage():
    global row
    row = 0
    clearPage()
    
    for item in cart:
        if cart[item] > 0:
            itemDisplay(ITEMS[ITEMS.index(item)], column = 0, flat = True)
            label(cartText[ITEMS.index(item)], column = 4)


orderPage()

app.mainloop()