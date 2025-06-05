import customtkinter as ctk
from PIL import Image

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

cartText = [""] * len(cart)

def updateVariables():
    cartText[0] = "x" + str(cart["hamburger"])
    cartText[1] = "x" + str(cart["cheeseburger"])
    cartText[2] = "x" + str(cart["veggie wrap"])
    cartText[3] = "x" + str(cart["french fries"])
    cartText[4] = "x" + str(cart["soft drink"])
    
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
    cart.item += 1
    updateVariables()

def removeFromCart(item):
    cart.item -= 1
    updateVariables()

app = ctk.CTk()
app.geometry("900x600")
app.title("Reseraunt App")

class button:
    def __init__(self, text, command, width = 1, column = 0):
        global row
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.grid(column=column, row=row, columnspan=width, sticky="nsew")
        if column == 2 or width == 2:
            row += 1

class image:
    def __init__(self, path, text, column = 1):
        global row
        self.image = ctk.CTkImage(Image.open(path), size=(100, 100))
        self.label = ctk.CTkLabel(app, image=self.image, text="")
        self.label.grid(column=column, row=row)
        row += 1
        self.label = ctk.CTkLabel(app, text=text)
        self.label.grid(column=column, row=row)
        row += 1

class reactiveLabel:
    def __init__(self, variable, column = 1):
        global row
        self.variable = variable
        self.label = ctk.CTkLabel(app, textvariable=variable)
        self.label.grid(column=column, row=row)

class itemWidget:
    def __init__(self, item, index, itemColumns):
        global row

        column = 3*(index % itemColumns)

        image(item.image, item.name, column = column+1)
        button("-", lambda: removeFromCart(item), column = column)
        reactiveLabel(cartText[index], column = column + 1)
        button("+", lambda: addToCart(item), column = column + 2)

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

    button("Cart", lambda: print(cart), width = 2, column = 2)

orderPage()

app.mainloop()