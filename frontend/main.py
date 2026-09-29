import tkinter as tk
from frames.empleados import crear_empleado
ventana = tk.Tk()
ventana.title ("Mi dispensario")
ventana.geometry("800x500")

def mostrar_frame (function_frame): 
    for widget in contenedor. winfo_children(): widget.destroy()


def mostrar_menu():
    menu=tk.Frame(ventana, bg="red", height=60)
    menu.pack(side="top", fill="x")

    global Contenedor  
    contenedor = tk.Frame(ventana, bg="white")
    contenedor.pack (fill="both", expand=True)

    tk.Button(menu, text="empleados", command=lambda: mostrar_frame (crear_empleado)).pack (side="left", padx=10, pady=10)

mostrar_menu()
ventana.mainloop()

    










    