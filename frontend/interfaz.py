import tkinter as tk
from tkinter import messagebox


# ============================================================
# CONFIGURACIÓN
# ============================================================

COLOR_FONDO = "#344054"
COLOR_VERDE = "#147A78"
COLOR_VERDE_CLARO = "#9ED9D6"
COLOR_BLANCO = "#FFFFFF"
COLOR_FONDO_DERECHO = "#F7F9FA"
COLOR_TEXTO = "#172B3A"
COLOR_TEXTO_SECUNDARIO = "#60758D"
COLOR_BORDE = "#DDE5EB"
COLOR_PLACEHOLDER = "#8A9BAD"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, fill="white",
                      outline="", width=1):
    """
    Dibuja un rectángulo con esquinas redondeadas usando Canvas.
    """
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        fill=fill,
        outline=outline,
        width=width
    )


def dibujar_icono_corazon(canvas, x, y, escala=1):
    """
    Dibuja un icono sencillo de corazón + electrocardiograma.
    """
    color = "#BDEBE8"

    # Corazón
    canvas.create_line(
        x - 30 * escala, y - 5 * escala,
        x - 35 * escala, y - 15 * escala,
        x - 35 * escala, y - 27 * escala,
        x - 30 * escala, y - 38 * escala,
        x - 20 * escala, y - 44 * escala,
        x - 10 * escala, y - 43 * escala,
        x, y - 34 * escala,
        x + 10 * escala, y - 43 * escala,
        x + 20 * escala, y - 44 * escala,
        x + 30 * escala, y - 38 * escala,
        x + 35 * escala, y - 27 * escala,
        x + 35 * escala, y - 15 * escala,
        x + 30 * escala, y - 5 * escala,
        x, y + 30 * escala,
        x - 30 * escala, y - 5 * escala,
        fill=color,
        width=5 * escala,
        smooth=True
    )

    # Línea tipo electrocardiograma
    canvas.create_line(
        x - 30 * escala, y - 5 * escala,
        x - 15 * escala, y - 5 * escala,
        x - 8 * escala, y - 18 * escala,
        x, y + 8 * escala,
        x + 9 * escala, y - 23 * escala,
        x + 16 * escala, y - 5 * escala,
        x + 30 * escala, y - 5 * escala,
        fill=color,
        width=4 * escala,
        smooth=False
    )


def dibujar_icono_usuario(canvas, x, y):
    """
    Icono de usuario.
    """
    color = "#8EA4BC"

    canvas.create_oval(
        x - 4, y - 8,
        x + 4, y,
        outline=color,
        width=1.8
    )

    canvas.create_arc(
        x - 8, y + 1,
        x + 8, y + 13,
        start=0,
        extent=180,
        style="arc",
        outline=color,
        width=1.8
    )


def dibujar_icono_candado(canvas, x, y):
    """
    Icono de candado.
    """
    color = "#8EA4BC"

    # Cuerpo
    canvas.create_rectangle(
        x - 8, y,
        x + 8, y + 11,
        outline=color,
        width=1.8
    )

    # Arco
    canvas.create_arc(
        x - 5, y - 8,
        x + 5, y + 5,
        start=0,
        extent=180,
        outline=color,
        width=1.8
    )


# ============================================================
# APLICACIÓN
# ============================================================

class CentroSaludLogin:

    def __init__(self, root):

        self.root = root

        self.root.title("Prototipo Centro de Salud")
        self.root.geometry("1440x820")
        self.root.minsize(1000, 650)

        self.root.configure(bg=COLOR_FONDO)

        # ----------------------------------------------------
        # BARRA SUPERIOR
        # ----------------------------------------------------

        self.topbar = tk.Frame(
            root,
            bg="#242424",
            height=52
        )

        self.topbar.pack(
            side="top",
            fill="x"
        )

        self.topbar.pack_propagate(False)

        # Logo / símbolo
        logo = tk.Label(
            self.topbar,
            text="◈",
            bg="#242424",
            fg="white",
            font=("Arial", 16)
        )
        logo.pack(side="left", padx=(18, 5))

        # IA
        ia = tk.Label(
            self.topbar,
            text="IA",
            bg="#242424",
            fg="#D0D5DD",
            font=("Arial", 9)
        )
        ia.pack(side="left")

        # Título central
        titulo = tk.Label(
            self.topbar,
            text="Prototipo Centro de Salud ⌄",
            bg="#242424",
            fg="white",
            font=("Arial", 12, "bold")
        )

        titulo.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Botón compartir
        compartir = tk.Button(
            self.topbar,
            text="Compartir",
            bg="#4B3AFF",
            fg="white",
            activebackground="#3D2FE0",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=8,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

        compartir.pack(
            side="right",
            padx=10
        )

        # ----------------------------------------------------
        # ÁREA PRINCIPAL
        # ----------------------------------------------------

        self.main = tk.Frame(
            root,
            bg=COLOR_FONDO
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        # Canvas principal
        self.canvas = tk.Canvas(
            self.main,
            bg=COLOR_FONDO,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<Configure>",
            self.redibujar
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.usuario = None
        self.password = None
        self.recordar = None

    # ========================================================
    # DIBUJAR INTERFAZ
    # ========================================================

    def redibujar(self, event=None):

        canvas = self.canvas

        canvas.delete("all")

        ancho = canvas.winfo_width()
        alto = canvas.winfo_height()

        if ancho < 700 or alto < 450:
            return

        # ----------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------------

        margen = 60

        x1 = margen
        y1 = 20

        x2 = ancho - margen
        y2 = alto - 20

        radio = 18

        # Fondo general
        rounded_rectangle(
            canvas,
            x1,
            y1,
            x2,
            y2,
            radius=radio,
            fill="#F5F7F8"
        )

        # ----------------------------------------------------
        # PANEL IZQUIERDO
        # ----------------------------------------------------

        division = x1 + (x2 - x1) * 0.51

        # Panel verde
        canvas.create_rectangle(
            x1,
            y1,
            division,
            y2,
            fill=COLOR_VERDE,
            outline=""
        )

        # Intentar cubrir la esquina superior izquierda
        canvas.create_arc(
            x1,
            y1,
            x1 + radio * 2,
            y1 + radio * 2,
            start=90,
            extent=90,
            fill=COLOR_VERDE,
            outline=COLOR_VERDE
        )

        # Esquina inferior izquierda
        canvas.create_arc(
            x1,
            y2 - radio * 2,
            x1 + radio * 2,
            y2,
            start=180,
            extent=90,
            fill=COLOR_VERDE,
            outline=COLOR_VERDE
        )

        # ----------------------------------------------------
        # ICONO
        # ----------------------------------------------------

        centro_x = (x1 + division) / 2
        icono_y = y1 + (y2 - y1) * 0.31

        rounded_rectangle(
            canvas,
            centro_x - 70,
            icono_y - 70,
            centro_x + 70,
            icono_y + 70,
            radius=25,
            fill="#378D8B",
            outline="#6AAEAC",
            width=1
        )

        dibujar_icono_corazon(
            canvas,
            centro_x,
            icono_y + 5,
            escala=1.0
        )

        # ----------------------------------------------------
        # TEXTO IZQUIERDO
        # ----------------------------------------------------

        canvas.create_text(
            centro_x,
            icono_y + 145,
            text="Mi Dispensario",
            fill="white",
            font=("Arial", 36, "bold"),
            anchor="center"
        )

        canvas.create_text(
            centro_x,
            icono_y + 192,
            text="Centro de Salud",
            fill=COLOR_VERDE_CLARO,
            font=("Arial", 22, "bold"),
            anchor="center"
        )

        # Línea
        canvas.create_line(
            centro_x - 30,
            icono_y + 244,
            centro_x + 30,
            icono_y + 244,
            fill="#65B4B0",
            width=6,
            capstyle="round"
        )

        # Eslogan
        canvas.create_text(
            centro_x,
            icono_y + 305,
            text='"Tu salud, nuestra prioridad"',
            fill="#B6E1DE",
            font=("Arial", 16, "italic"),
            anchor="center"
        )

        # ----------------------------------------------------
        # PANEL DERECHO
        # ----------------------------------------------------

        canvas.create_rectangle(
            division,
            y1,
            x2,
            y2,
            fill="#F7F9FA",
            outline=""
        )

        # ----------------------------------------------------
        # TARJETA LOGIN
        # ----------------------------------------------------

        tarjeta_ancho = min(450, (x2 - division) - 90)
        tarjeta_alto = 580

        tarjeta_x1 = division + ((x2 - division) - tarjeta_ancho) / 2
        tarjeta_y1 = y1 + ((y2 - y1) - tarjeta_alto) / 2

        tarjeta_x2 = tarjeta_x1 + tarjeta_ancho
        tarjeta_y2 = tarjeta_y1 + tarjeta_alto

        # Sombra simulada
        rounded_rectangle(
            canvas,
            tarjeta_x1 + 5,
            tarjeta_y1 + 7,
            tarjeta_x2 + 5,
            tarjeta_y2 + 7,
            radius=32,
            fill="#E9EEF0"
        )

        rounded_rectangle(
            canvas,
            tarjeta_x1,
            tarjeta_y1,
            tarjeta_x2,
            tarjeta_y2,
            radius=32,
            fill="white"
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        padding = 50

        canvas.create_text(
            tarjeta_x1 + padding,
            tarjeta_y1 + 65,
            text="Iniciar sesión",
            fill=COLOR_TEXTO,
            font=("Arial", 28, "bold"),
            anchor="w"
        )

        canvas.create_text(
            tarjeta_x1 + padding,
            tarjeta_y1 + 108,
            text="Ingresa tus credenciales para acceder al\nsistema.",
            fill=COLOR_TEXTO_SECUNDARIO,
            font=("Arial", 13),
            anchor="w",
            justify="left"
        )

        # ----------------------------------------------------
        # USUARIO
        # ----------------------------------------------------

        usuario_label_y = tarjeta_y1 + 202

        canvas.create_text(
            tarjeta_x1 + padding,
            usuario_label_y,
            text="Usuario",
            fill=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        usuario_y = usuario_label_y + 20

        rounded_rectangle(
            canvas,
            tarjeta_x1 + padding,
            usuario_y,
            tarjeta_x2 - padding,
            usuario_y + 57,
            radius=15,
            fill="#FBFCFD",
            outline=COLOR_BORDE,
            width=1
        )

        dibujar_icono_usuario(
            canvas,
            tarjeta_x1 + padding + 27,
            usuario_y + 28
        )

        # Entry usuario
        self.usuario = tk.Entry(
            self.canvas,
            bd=0,
            relief="flat",
            bg="#FBFCFD",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            font=("Arial", 12)
        )

        self.usuario.insert(0, "admin")

        self.canvas.create_window(
            tarjeta_x1 + padding + 50,
            usuario_y + 28,
            window=self.usuario,
            width=tarjeta_ancho - 130,
            height=38,
            anchor="w"
        )

        # ----------------------------------------------------
        # CONTRASEÑA
        # ----------------------------------------------------

        password_label_y = usuario_y + 87

        canvas.create_text(
            tarjeta_x1 + padding,
            password_label_y,
            text="Contraseña",
            fill=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        password_y = password_label_y + 20

        rounded_rectangle(
            canvas,
            tarjeta_x1 + padding,
            password_y,
            tarjeta_x2 - padding,
            password_y + 57,
            radius=15,
            fill="#FBFCFD",
            outline=COLOR_BORDE,
            width=1
        )

        dibujar_icono_candado(
            canvas,
            tarjeta_x1 + padding + 27,
            password_y + 22
        )

        self.password = tk.Entry(
            self.canvas,
            bd=0,
            relief="flat",
            bg="#FBFCFD",
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            font=("Arial", 12),
            show="•"
        )

        self.password.insert(0, "password")

        self.canvas.create_window(
            tarjeta_x1 + padding + 50,
            password_y + 28,
            window=self.password,
            width=tarjeta_ancho - 130,
            height=38,
            anchor="w"
        )

        # ----------------------------------------------------
        # RECORDARME
        # ----------------------------------------------------

        recordar_y = password_y + 103

        self.recordar = tk.BooleanVar(value=False)

        checkbox = tk.Checkbutton(
            self.canvas,
            text="Recordarme",
            variable=self.recordar,
            bg="white",
            activebackground="white",
            fg="#42566E",
            activeforeground="#42566E",
            selectcolor="white",
            font=("Arial", 11),
            cursor="hand2"
        )

        self.canvas.create_window(
            tarjeta_x1 + padding,
            recordar_y,
            window=checkbox,
            anchor="w"
        )

        # ----------------------------------------------------
        # PROBLEMAS
        # ----------------------------------------------------

        problemas = tk.Label(
            self.canvas,
            text="¿Problemas?",
            bg="white",
            fg="#087B78",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )

        problemas.bind(
            "<Button-1>",
            self.problemas
        )

        self.canvas.create_window(
            tarjeta_x2 - padding,
            recordar_y,
            window=problemas,
            anchor="e"
        )

        # ----------------------------------------------------
        # BOTÓN INGRESAR
        # ----------------------------------------------------

        boton_y = recordar_y + 72

        boton = tk.Button(
            self.canvas,
            text="Ingresar   →",
            command=self.ingresar,
            bg=COLOR_VERDE,
            fg="white",
            activebackground="#0E6967",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )

        self.canvas.create_window(
            (tarjeta_x1 + tarjeta_x2) / 2,
            boton_y,
            window=boton,
            width=tarjeta_ancho - 100,
            height=60
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def ingresar(self):

        usuario = self.usuario.get()
        password = self.password.get()

        # Credenciales de ejemplo
        if usuario == "admin" and password == "password":

            messagebox.showinfo(
                "Centro de Salud",
                "Inicio de sesión correcto."
            )

            # Aquí puedes abrir la ventana principal
            self.abrir_sistema()

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

    # ========================================================
    # PROBLEMAS
    # ========================================================

    def problemas(self, event=None):

        messagebox.showinfo(
            "Ayuda",
            "Si tienes problemas para ingresar,\n"
            "contacta al administrador del sistema."
        )

    # ========================================================
    # SISTEMA PRINCIPAL
    # ========================================================

    def abrir_sistema(self):

        ventana = tk.Toplevel(self.root)

        ventana.title("Centro de Salud")
        ventana.geometry("900x600")
        ventana.configure(bg="#F5F7F8")

        titulo = tk.Label(
            ventana,
            text="Centro de Salud",
            bg="#F5F7F8",
            fg=COLOR_TEXTO,
            font=("Arial", 26, "bold")
        )

        titulo.pack(
            pady=50
        )

        mensaje = tk.Label(
            ventana,
            text="Bienvenido al sistema.",
            bg="#F5F7F8",
            fg=COLOR_TEXTO_SECUNDARIO,
            font=("Arial", 14)
        )

        mensaje.pack()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CentroSaludLogin(root)

    root.mainloop()
