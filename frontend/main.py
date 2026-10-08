import tkinter as tk
from tkinter import messagebox
import requests

from frames.inicio import crear_inicio


# =========================================================
# COLORES
# =========================================================

TURQUESA_OSCURO = "#006B6B"
TURQUESA = "#009999"
TURQUESA_CLARO = "#E8F7F7"
BLANCO = "#FFFFFF"
GRIS = "#6B7C85"
GRIS_CLARO = "#D9E7EA"
NEGRO = "#17343A"


# =========================================================
# FUNCIONES
# =========================================================

def mostrar_inicio():
    """
    Oculta la pantalla de login y muestra la pantalla principal.
    """

    global contenedor

    # Ocultar el login completo
    login_frame.pack_forget()

    # Crear contenedor de la pantalla principal
    contenedor = tk.Frame(
        ventana,
        bg="#eef1f5"
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # Crear pantalla de inicio
    try:
        frame_inicio = crear_inicio(contenedor)

        frame_inicio.pack(
            fill="both",
            expand=True
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo cargar la pantalla de inicio:\n\n{error}"
        )


def iniciar_sesion():
    """
    Envía usuario y contraseña al servidor.
    """

    usuario = entrada_usuario.get().strip()
    contraseña = entrada_password.get()

    # Validar campos
    if not usuario or not contraseña:
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese usuario y contraseña."
        )
        return

    datos = {
        "nombre_usuario": usuario,
        "contrasena": contraseña
    }

    try:

        respuesta = requests.post(
            "http://localhost:3000/api/login",
            json=datos,
            timeout=10
        )

        if respuesta.status_code == 200:

            messagebox.showinfo(
                "Inicio de sesión",
                "¡Bienvenido!"
            )

            mostrar_inicio()

        elif respuesta.status_code == 401:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

        else:

            messagebox.showerror(
                "Error",
                f"Ocurrió un error al iniciar sesión.\n"
                f"Código: {respuesta.status_code}"
            )

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Error de conexión",
            "No se pudo conectar con el servidor.\n\n"
            "Verifique que el servidor esté ejecutándose."
        )

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Tiempo agotado",
            "El servidor tardó demasiado en responder."
        )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(
            "Error",
            f"Ocurrió un error al comunicarse con el servidor:\n\n{error}"
        )


def mostrar_ocultar_password():
    """
    Muestra u oculta la contraseña.
    """

    if entrada_password.cget("show") == "":
        entrada_password.config(show="•")
        boton_ojo.config(text="👁")
    else:
        entrada_password.config(show="")
        boton_ojo.config(text="◉")


def recuperar_password():
    """
    Muestra información para recuperar la contraseña.
    """

    messagebox.showinfo(
        "Recuperar contraseña",
        "Contactá al administrador para recuperar tu contraseña."
    )


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

ventana = tk.Tk()

ventana.title(
    "Mi dispensario - Inicio de sesión"
)

ventana.geometry(
    "900x550"
)

ventana.resizable(
    False,
    False
)

ventana.configure(
    bg=BLANCO
)


# =========================================================
# FRAME PRINCIPAL DEL LOGIN
# =========================================================

login_frame = tk.Frame(
    ventana,
    bg=BLANCO
)

login_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# PANEL IZQUIERDO
# =========================================================

panel_izquierdo = tk.Frame(
    login_frame,
    bg=TURQUESA_OSCURO,
    width=330,
    height=550
)

panel_izquierdo.pack(
    side="left",
    fill="y"
)

panel_izquierdo.pack_propagate(False)


# =========================================================
# LOGO MÉDICO
# =========================================================

logo = tk.Canvas(
    panel_izquierdo,
    width=90,
    height=90,
    bg=TURQUESA_OSCURO,
    highlightthickness=0
)

logo.pack(
    pady=(55, 5)
)


# Círculo
logo.create_oval(
    10, 10,
    80, 80,
    fill="#D9FFFF",
    outline=""
)


# Cruz vertical
logo.create_rectangle(
    37, 20,
    53, 70,
    fill=TURQUESA_OSCURO,
    outline=""
)


# Cruz horizontal
logo.create_rectangle(
    20, 37,
    70, 53,
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


# =========================================================
# NOMBRE DEL CENTRO
# =========================================================

tk.Label(
    panel_izquierdo,
    text="Cuidar para Vivir",
    font=("Arial", 20, "bold"),
    fg=BLANCO,
    bg=TURQUESA_OSCURO
).pack(
    pady=(5, 0)
)


tk.Label(
    panel_izquierdo,
    text="Centro de Salud",
    font=("Arial", 12),
    fg="#D5FFFF",
    bg=TURQUESA_OSCURO
).pack()


# =========================================================
# FRASE
# =========================================================

tk.Label(
    panel_izquierdo,
    text="Tu salud, nuestra prioridad.",
    font=("Arial", 10),
    fg="#C8EEEE",
    bg=TURQUESA_OSCURO
).pack(
    pady=(45, 20)
)


# =========================================================
# PULSO DECORATIVO
# =========================================================

pulso = tk.Canvas(
    panel_izquierdo,
    width=270,
    height=80,
    bg=TURQUESA_OSCURO,
    highlightthickness=0
)

pulso.pack()


# Línea de pulso
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


# =========================================================
# PANEL DERECHO
# =========================================================

panel_derecho = tk.Frame(
    login_frame,
    bg=BLANCO,
    width=570,
    height=550
)

panel_derecho.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================================================
# FORMULARIO
# =========================================================

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


# =========================================================
# TÍTULO
# =========================================================

tk.Label(
    formulario,
    text="Bienvenido",
    font=("Arial", 22, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(
    fill="x"
)


tk.Label(
    formulario,
    text="Iniciá sesión para continuar",
    font=("Arial", 10),
    fg=GRIS,
    bg=BLANCO,
    anchor="w"
).pack(
    fill="x",
    pady=(3, 25)
)


# =========================================================
# USUARIO
# =========================================================

tk.Label(
    formulario,
    text="Usuario",
    font=("Arial", 9, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(
    fill="x",
    pady=(0, 5)
)


contenedor_usuario = tk.Frame(
    formulario,
    bg=GRIS_CLARO,
    height=40
)

contenedor_usuario.pack(
    fill="x"
)

contenedor_usuario.pack_propagate(False)


tk.Label(
    contenedor_usuario,
    text="♙",
    font=("Arial", 15),
    fg=GRIS,
    bg=GRIS_CLARO
).pack(
    side="left",
    padx=(10, 5)
)


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


# =========================================================
# CONTRASEÑA
# =========================================================

tk.Label(
    formulario,
    text="Contraseña",
    font=("Arial", 9, "bold"),
    fg=NEGRO,
    bg=BLANCO,
    anchor="w"
).pack(
    fill="x",
    pady=(18, 5)
)


contenedor_password = tk.Frame(
    formulario,
    bg=GRIS_CLARO,
    height=40
)

contenedor_password.pack(
    fill="x"
)

contenedor_password.pack_propagate(False)


tk.Label(
    contenedor_password,
    text="🔒",
    font=("Arial", 11),
    fg=GRIS,
    bg=GRIS_CLARO
).pack(
    side="left",
    padx=(10, 5)
)


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


# =========================================================
# BOTÓN MOSTRAR CONTRASEÑA
# =========================================================

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

boton_ojo.pack(
    side="right",
    padx=8
)


# =========================================================
# RECORDAR + RECUPERAR
# =========================================================

fila_opciones = tk.Frame(
    formulario,
    bg=BLANCO
)

fila_opciones.pack(
    fill="x",
    pady=(12, 20)
)


recordar = tk.BooleanVar(
    value=True
)


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
).pack(
    side="left"
)


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
).pack(
    side="right"
)


# =========================================================
# BOTÓN INICIAR SESIÓN
# =========================================================

boton_login = tk.Button(
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
)

boton_login.pack(
    fill="x"
)


# =========================================================
# ENTER PARA INICIAR SESIÓN
# =========================================================

ventana.bind(
    "<Return>",
    lambda event: iniciar_sesion()
)


# =========================================================
# FOCUS INICIAL
# =========================================================

entrada_usuario.focus()


# =========================================================
# INICIAR PROGRAMA
# =========================================================

ventana.mainloop()