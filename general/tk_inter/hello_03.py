
from tkinter import *

root = Tk()
root.title("posicionar")
root.geometry("400x200")


def saludo():
    print("Hola te saludo")


def minimizar():
    root.iconify()


etiqueta = Label(root, text="Etiqueta")
etiqueta.place(x=30, y=40)

boton1 = Button(root, text="boton")
boton1.grid(row=0, column=1)

etiqueta1 = Label(root, text="Saluda desde aqui")
etiqueta1.place(x=30, y=60)

etiqueta2 = Label(root, text="Minimizar desde aqui")
etiqueta2.place(x=30, y=100)

boton1 = Button(root, text="Haz click aqui para saludar", command=saludo)
boton1.place(x=200, y=50)

boton2 = Button(root, text="Haz click aqui para minimizar", command=minimizar)
boton2.place(x=200, y=100)

root.mainloop()

