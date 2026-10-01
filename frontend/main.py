import tkinter as tk
from tkinter import messagebox


# =========================
# CONFIGURACIÓN PRINCIPAL
# =========================

ventana = tk.Tk()
ventana.title("Cuidar para Vivir - Inicio de sesión")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg="white")


# Colores
TURQUESA_OSCURO = "#006B6B"
TURQUESA = "#009999"
TURQUESA_CLARO = "#E8F7F7"
BLANCO = "#FFFFFF"
GRIS = "#6B7C85"
GRIS_CLARO = "#D9E7EA"
NEGRO = "#17343A"


# =========================
# FUNCIONES
# =========================

def mostrar_ocultar_password():
    """Muestra u oculta la contraseña."""
    if entrada_password.cget("show") == "":
        entrada_password.config(show="•")
        boton_ojo.config(text="👁")
    else:
        entrada_password.config(show="")
        boton_ojo.config(text="◉")


def iniciar_sesion():
    usuario = entrada_usuario.get()
    password = entrada_password.get()

    # Cambiá estos datos por los de tu sistema
    if usuario == "admin" and password == "1234":
        messagebox.showinfo(
            "Inicio de sesión",
            "¡Bienvenido a Cuidar para Vivir!"
        )

        # Acá podés abrir la pantalla principal
        # Por ejemplo:
        # ventana.destroy()
        # crear_empleado()

    elif usuario == "" or password == "":
        messagebox.showwarning(
            "Campos vacíos",
            "Completá el usuario y la contraseña."
        )

    else:
        messagebox.showerror(
            "Error",
            "El usuario o la contraseña son incorrectos."
        )


def recuperar_password():
    messagebox.showinfo(
        "Recuperar contraseña",
        "Contactá al administrador para recuperar tu contraseña."
    )


# =========================
# PANEL IZQUIERDO
# =========================

panel_izquierdo = tk.Frame(
    ventana,
    bg=TURQUESA_OSCURO,
    width=330,
    height=550
)

panel_izquierdo.pack(side="left", fill="y")
panel_izquierdo.pack_propagate(False)


# Logo médico
logo = tk.Canvas(
    panel_izquierdo,
    width=90,
    height=90,
    bg=TURQUESA_OSCURO,
    highlightthickness=0
)
logo.pack(pady=(55, 5))

# Círculo del logo
logo.create_oval(
    10, 10, 80, 80,
    fill="#D9FFFF",
    outline=""
)

# Cruz
logo.create_rectangle(
    37, 20, 53, 70,
    fill=TURQUESA_OSCURO,
    outline=""
)

logo.create_rectangle(
    20, 37, 70, 53,
    fill=TURQUESA_OSCURO,
    outline=""
)

# Línea de pulso
logo.create_line(
    18, 57,
    30, 57,
    35, 47,
    42, 65,
    49, 40,
    56, 57,
    72, 57,
    fill=TURQUESA,
    width=3,
    smooth=True
)


# Nombre
tk.Label(
    panel_izquierdo,
    text="Cuidar para Vivir",
    font=("Arial", 20, "bold"),
    fg=BLANCO,
    bg=TURQUESA_OSCURO
).pack(pady=(5, 0))


tk.Label(
    panel_izquierdo,
    text="Centro de Salud",
    font=("Arial", 12),
    fg="#D5FFFF",
    bg=TURQUESA_OSCURO
).pack()


# Frase
tk.Label(
    panel_izquierdo,
    text="Tu salud, nuestra prioridad.",
    font=("Arial", 10),
    fg="#C8EEEE",
    bg=TURQUESA_OSCURO
).pack(pady=(45, 20))


# Corazón / pulso decorativo
pulso = tk.Canvas(
    panel_izquierdo,
    width=270,
    height=80,
    bg=TURQUESA_OSCURO,
    highlightthickness=0
)
pulso.pack()

pulso.create_line(
    5, 50,
    35, 50,
    43, 25,
    51, 65,
    60, 40,
    70, 50,
    90, 50,
    fill="#35BABA",
    width=3,
    smooth=True
)

# Corazón
pulso.create_line(
    90, 42,
    105, 25,
    120, 25,
    135, 40,
    150, 25,
    170, 25,
    185, 42,
    185, 55,
    138, 76,
    90, 42,
    fill="#35BABA",
    width=3,
    smooth=True
)


# =========================
# PANEL DERECHO
# =========================

panel_derecho = tk.Frame(
    ventana,
    bg=BLANCO,
    width=570,
    height=550
)

panel_derecho.pack(side="right", fill="both", expand=True)


# Contenedor del formulario
formulario = tk.Frame(
    panel_derecho,
    bg=BLANCO
)

formulario.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=400
)


# =========================
# TÍTULO
# =========================

tk.Label(
    formulario,
    text="Bienvenido",
    font=("Arial", 22, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(fill="x")


tk.Label(
    formulario,
    text="Iniciá sesión para continuar",
    font=("Arial", 10),
    fg=GRIS,
    bg=BLANCO,
    anchor="w"
).pack(fill="x", pady=(3, 25))


# =========================
# USUARIO
# =========================

tk.Label(
    formulario,
    text="Usuario",
    font=("Arial", 9, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(fill="x", pady=(0, 5))


contenedor_usuario = tk.Frame(
    formulario,
    bg=GRIS_CLARO,
    height=40
)

contenedor_usuario.pack(fill="x")
contenedor_usuario.pack_propagate(False)


tk.Label(
    contenedor_usuario,
    text="♙",
    font=("Arial", 15),
    fg=GRIS,
    bg=GRIS_CLARO
).pack(side="left", padx=(10, 5))


entrada_usuario = tk.Entry(
    contenedor_usuario,
    font=("Arial", 10),
    bd=0,
    relief="flat",
    bg=GRIS_CLARO,
    fg=NEGRO
)

entrada_usuario.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)


# =========================
# CONTRASEÑA
# =========================

tk.Label(
    formulario,
    text="Contraseña",
    font=("Arial", 9, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(fill="x", pady=(18, 5))


contenedor_password = tk.Frame(
    formulario,
    bg=GRIS_CLARO,
    height=40
)

contenedor_password.pack(fill="x")
contenedor_password.pack_propagate(False)


tk.Label(
    contenedor_password,
    text="🔒",
    font=("Arial", 11),
    fg=GRIS,
    bg=GRIS_CLARO
).pack(side="left", padx=(10, 5))


entrada_password = tk.Entry(
    contenedor_password,
    font=("Arial", 10),
    bd=0,
    relief="flat",
    bg=GRIS_CLARO,
    fg=NEGRO,
    show="•"
)

entrada_password.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)


boton_ojo = tk.Button(
    contenedor_password,
    text="👁",
    font=("Arial", 10),
    bd=0,
    bg=GRIS_CLARO,
    activebackground=GRIS_CLARO,
    cursor="hand2",
    command=mostrar_ocultar_password
)

boton_ojo.pack(side="right", padx=8)


# =========================
# RECORDAR + RECUPERAR
# =========================

fila_opciones = tk.Frame(
    formulario,
    bg=BLANCO
)

fila_opciones.pack(
    fill="x",
    pady=(12, 20)
)


recordar = tk.BooleanVar(value=True)


tk.Checkbutton(
    fila_opciones,
    text="Recordar usuario",
    variable=recordar,
    font=("Arial", 9),
    fg=NEGRO,
    bg=BLANCO,
    activebackground=BLANCO,
    selectcolor=BLANCO,
    cursor="hand2"
).pack(side="left")


tk.Button(
    fila_opciones,
    text="¿Olvidaste tu contraseña?",
    font=("Arial", 8, "bold"),
    fg=TURQUESA,
    bg=BLANCO,
    activeforeground=TURQUESA_OSCURO,
    activebackground=BLANCO,
    bd=0,
    cursor="hand2",
    command=recuperar_password
).pack(side="right")


# =========================
# BOTÓN INICIAR SESIÓN
# =========================

tk.Button(
    formulario,
    text="Iniciar sesión",
    font=("Arial", 10, "bold"),
    fg=BLANCO,
    bg=TURQUESA,
    activeforeground=BLANCO,
    activebackground=TURQUESA_OSCURO,
    bd=0,
    relief="flat",
    cursor="hand2",
    height=2,
    command=iniciar_sesion
).pack(fill="x")


# =========================
# ENTER PARA INICIAR SESIÓN
# =========================

ventana.bind("<Return>", lambda event: iniciar_sesion())

entrada_usuario.focus()


# =========================
# INICIAR PROGRAMA
# =========================

ventana.mainloop()