
from tkinter import *

root = Tk()

root.title("Mi primer ventana")
root.geometry("500x300")

texto = Label(root, text="Hola mundo")
texto.pack()

boton1 = Button(root, text="Minimizar", command=root.iconify, bg="red")
boton1.pack(side=LEFT)

def imprimir():
    label1 = Label(root, text="imprimiendo...")
    label1.pack()

boton2 = Button(root, text="imprimir", command=imprimir, bg="blue")
boton2.pack(side=RIGHT)

root.mainloop()

