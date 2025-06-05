import customtkinter as ctk
from PIL import Image

global cart
cart = []

global ITEMS
ITEMS = [
    item("hamburger", 5, "hamburger.jpg"),
    item("cheeseburger", 6, "cheeseburger.jpg"),
    item("veggie wrap", 4.5, "veggie wrap.jpg"),
    item("french fries", 2.5, "french fries.jpg"),
    item("soft drink", 1.5, "soft drink.jpg"),
]

class item:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = "images/" + image

def addToCart(item):
    cart.append(item)

def removeFromCart(item):
    cart.remove(item)

app = ctk.CTk()
app.geometry("900x600")
app.title("Reseraunt App")

class button:
    def __init__(self, text, command):
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.pack()

class image:
    def __init__(self, path):
        self.image = 
        self.label = 
        self.label.pack()

# Hamburger
image(ITEMS[0].image)
button("+", lambda: addToCart(ITEMS[0]))
button("-", lambda: removeFromCart(ITEMS[0]))

# Cheeseburger
button("+", lambda: addToCart(ITEMS[1]))
button("-", lambda: removeFromCart(ITEMS[1]))

# Veggie Wrap
button("+", lambda: addToCart(ITEMS[2]))
button("-", lambda: removeFromCart(ITEMS[2]))

# French Fries
button("+", lambda: addToCart(ITEMS[3]))
button("-", lambda: removeFromCart(ITEMS[3]))

# Soft Drink
button("+", lambda: addToCart(ITEMS[4]))
button("-", lambda: removeFromCart(ITEMS[4]))

button("Cart", lambda: print(cart))

app.mainloop()