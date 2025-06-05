import customtkinter as ctk
from PIL import Image

class item:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = "images/" + image

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

def addToCart(item):
    cart.append(item)

def removeFromCart(item):
    cart.remove(item)

app = ctk.CTk()
app.geometry("900x600")
app.title("Reseraunt App")

class button:
    def __init__(self, text, command, width):
        self.button = ctk.CTkButton(app, text=text, command=command)
        self.button.pack()

class image:
    def __init__(self, path, text):
        self.image = ctk.CTkImage(Image.open(path), size=(100, 100))
        self.label = ctk.CTkLabel(app, image=self.image, text="", columnspan=2)
        self.label.pack()
        self.label = ctk.CTkLabel(app, text=text)
        self.label.pack()

# Hamburger
image(ITEMS[0].image, ITEMS[0].name)
button("+", lambda: addToCart(ITEMS[0]), 1)
button("-", lambda: removeFromCart(ITEMS[0]), 1)

# Cheeseburger
button("+", lambda: addToCart(ITEMS[1]), 1)
button("-", lambda: removeFromCart(ITEMS[1]), 1)

# Veggie Wrap
button("+", lambda: addToCart(ITEMS[2]), 1)
button("-", lambda: removeFromCart(ITEMS[2]), 1)

# French Fries
button("+", lambda: addToCart(ITEMS[3]), 1)
button("-", lambda: removeFromCart(ITEMS[3]), 1)

# Soft Drink
button("+", lambda: addToCart(ITEMS[4]), 1)
button("-", lambda: removeFromCart(ITEMS[4]), 1)

button("Cart", lambda: print(cart))

app.mainloop()