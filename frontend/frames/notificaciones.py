
import tkinter as tk


def mostrar_toast(parent, titulo, mensaje, tipo="exito"):

    colores = {
        "exito": ("#16A34A", "✓"),
        "error": ("#DC2626", "✕"),
        "advertencia": ("#D97706", "!")
    }

    color, icono = colores.get(tipo, colores["exito"])

    ventana = tk.Toplevel(parent)
    ventana.overrideredirect(True)
    ventana.configure(bg="#FFFFFF")
    ventana.attributes("-topmost", True)

    marco = tk.Frame(
        ventana,
        bg="#FFFFFF",
        highlightbackground="#DDDDDD",
        highlightthickness=1
    )
    marco.pack(fill="both", expand=True)

    # Barra lateral de color
    tk.Frame(
        marco,
        bg=color,
        width=5
    ).pack(side="left", fill="y")

    # Icono
    tk.Label(
        marco,
        text=icono,
        font=("Segoe UI", 20, "bold"),
        fg=color,
        bg="#FFFFFF"
    ).pack(side="left", padx=15)

    # Contenedor del texto
    contenido = tk.Frame(marco, bg="#FFFFFF")
    contenido.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=12)

    # Título
    tk.Label(
        contenido,
        text=titulo,
        font=("Segoe UI", 10, "bold"),
        fg="#333333",
        bg="#FFFFFF",
        anchor="w"
    ).pack(fill="x")

    # Descripción
    tk.Label(
        contenido,
        text=mensaje,
        font=("Segoe UI", 9),
        fg="#666666",
        bg="#FFFFFF",
        wraplength=280,
        justify="left",
        anchor="w"
    ).pack(fill="x", pady=(3, 0))

    ventana.update_idletasks()

    # Posición de la notificación
    parent.update_idletasks()

    x = parent.winfo_rootx() + parent.winfo_width() - ventana.winfo_width() - 20
    y = parent.winfo_rooty() + 60

    ventana.geometry(f"+{x}+{y}")

    # Cierre automático
    ventana.after(3500, ventana.destroy)
