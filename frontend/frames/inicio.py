
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import date, datetime, timedelta
import requests

from frames.insumos import crear_insumo
from frames.empleados import crear_empleado
from frames.usuario import usuarios
from frames.movimientoInsumos import crear_movimientoinsumo
from frames.reportes import crear_reportes


API_URL = "http://localhost:3000/api/reportes"

ICONOS = {}

CARPETA_ICONOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "iconos"
)

def cargar_icono(nombre):

    if nombre not in ICONOS:

        ruta = os.path.join(
            CARPETA_ICONOS,
            nombre + ".png"
        )

        imagen = Image.open(ruta).convert("RGBA")

        imagen = imagen.resize(
            (22, 22),
            Image.Resampling.LANCZOS
        )

        ICONOS[nombre] = ImageTk.PhotoImage(imagen)

    return ICONOS[nombre]


def crear_inicio(parent):

    # =========================
    # COLORES
    # =========================
    VERDE_OSCURO = "#006B6B"
    VERDE = "#009999"
    BLANCO = "#FFFFFF"
    FONDO = "#F5FAFB"
    GRIS = "#64777D"
    BORDE = "#DDEBED"
    TEXTO = "#17343A"
    ROJO = "#E94B4B"

    frame = tk.Frame(parent, bg=FONDO)

    # =========================
    # MENÚ LATERAL
    # =========================
    menu = tk.Frame(frame, bg=VERDE_OSCURO, width=220)
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    tk.Label(
        menu,
        text="✚  Cuidar para Vivir",
        font=("Arial", 13, "bold"),
        bg=VERDE_OSCURO,
        fg=BLANCO
    ).pack(pady=(25, 5))

    tk.Label(
        logo_frame,
        text="✚",
        font=("Arial", 25, "bold"),
        fg=BLANCO,
        bg=VERDE_OSCURO
    ).pack(side="left", padx=(18, 7))

    nombre_logo = tk.Frame(logo_frame, bg=VERDE_OSCURO)
    nombre_logo.pack(side="left")

    tk.Label(
        nombre_logo,
        text="Mi dispensario",
        font=("Arial", 11, "bold"),
        fg=BLANCO,
        bg=VERDE_OSCURO
    ).pack(anchor="w")

    tk.Label(
        nombre_logo,
        text="Centro de Salud",
        font=("Arial", 9),
        bg=VERDE_OSCURO,
        fg="#BFE5E5"
    ).pack(pady=(0, 30))

    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(side="right", fill="both", expand=True)

    panel_inicio = tk.Frame(contenido, bg=FONDO)
    panel_inicio.pack(fill="both", expand=True)

    vista_activa = None

    # =========================
    # CONEXIÓN CON LA API
    # =========================
    def consultar(ruta, clave):
        respuesta = requests.get(
            f"{API_URL}/{ruta}",
            timeout=8
        )
        respuesta.raise_for_status()

        datos = respuesta.json()
        if isinstance(datos, list):
            return datos
        return datos.get(clave, [])

    def convertir_fecha(valor):
        try:
            if not valor:
                return None
            return date.fromisoformat(str(valor)[:10])
        except (ValueError, TypeError):
            return None

    def actualizar_estadisticas():
        try:
            empleados = consultar("empleados", "empleados")
            insumos = consultar("insumos", "insumos")

            hoy = date.today()
            limite = hoy + timedelta(days=30)

            stock_bajo = 0
            vencimientos = 0

            for insumo in insumos:
                cantidad = float(insumo.get("cantidad") or 0)
                minimo = float(insumo.get("stock_minimo") or 0)

                if cantidad <= minimo:
                    stock_bajo += 1

                fecha = convertir_fecha(
                    insumo.get("fecha_vencimiento")
                )

                if fecha and hoy <= fecha <= limite:
                    vencimientos += 1

            lbl_empleados.config(text=str(len(empleados)))
            lbl_insumos.config(text=str(len(insumos)))
            lbl_stock.config(text=str(stock_bajo))
            lbl_vencimientos.config(text=str(vencimientos))

        except (requests.RequestException, ValueError, TypeError) as error:
            for etiqueta in (
                lbl_empleados,
                lbl_insumos,
                lbl_stock,
                lbl_vencimientos
            ):
                etiqueta.config(text="--")

            messagebox.showwarning(
                "Error de conexión",
                f"No se pudieron cargar las estadísticas.\n{error}"
            )

    # =========================
    # NAVEGACIÓN
    # =========================
    def mostrar_vista(funcion):
        nonlocal vista_activa

        panel_inicio.pack_forget()

        if vista_activa:
            vista_activa.destroy()

        vista_activa = tk.Frame(contenido, bg=FONDO)
        vista_activa.pack(fill="both", expand=True)

        try:
            resultado = funcion(vista_activa)

            if isinstance(resultado, tk.Widget):
                if not resultado.winfo_manager():
                    resultado.pack(fill="both", expand=True)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir la pantalla:\n{error}"
            )

    def volver_inicio():
        nonlocal vista_activa

        if vista_activa:
            vista_activa.destroy()
            vista_activa = None

        panel_inicio.pack(fill="both", expand=True)
        actualizar_estadisticas()

    # =========================
    # BOTONES DEL MENÚ
    # =========================
    # def crear_boton_menu(texto, icono, comando=None):

    #     boton = tk.Frame(
    #         menu,
    #         bg=VERDE_OSCURO,
    #         height=42,
    #         cursor="hand2"
    #     )
    #     boton.pack(
    #         fill="x",
    #         padx=8,
    #         pady=2
    #     )
    #     boton.pack_propagate(False)

    #     etiqueta_icono = tk.Label(
    #         boton,
    #         text=icono,
    #         font=("Arial", 13),
    #         fg=BLANCO,
    #         bg=VERDE_OSCURO,
    #         width=3,
    #         cursor="hand2"
    #     )
    #     etiqueta_icono.pack(side="left")

    #     etiqueta_texto = tk.Label(
    #         boton,
    #         text=texto,
    #         font=("Arial", 9),
    #         fg=BLANCO,
    #         bg=VERDE_OSCURO,
    #         cursor="hand2"
    #     )
    #     etiqueta_texto.pack(side="left")

    #     if comando is not None:

    #         def ejecutar(event=None):
    #             comando()

    #         boton.bind("<Button-1>", ejecutar)
    #         etiqueta_icono.bind("<Button-1>", ejecutar)
    #         etiqueta_texto.bind("<Button-1>", ejecutar)

    #         # Efecto visual al pasar el mouse
    #         def entrar(event):
    #             boton.configure(bg=VERDE)
    #             etiqueta_icono.configure(bg=VERDE)
    #             etiqueta_texto.configure(bg=VERDE)

    #         def salir(event):
    #             boton.configure(bg=VERDE_OSCURO)
    #             etiqueta_icono.configure(bg=VERDE_OSCURO)
    #             etiqueta_texto.configure(bg=VERDE_OSCURO)

    #         for widget in (boton, etiqueta_icono, etiqueta_texto):
    #             widget.bind("<Enter>", entrar)
    #             widget.bind("<Leave>", salir)

    #     return boton

    def crear_boton_menu(texto, icono, comando=None):

        boton = tk.Frame(
            menu,
            bg=VERDE_OSCURO,
            height=42,
            cursor="hand2"
        )

        boton.pack(
            fill="x",
            padx=8,
            pady=2
        )

        boton.pack_propagate(False)

        # Icono moderno
        imagen_icono = cargar_icono(icono)

        etiqueta_icono = tk.Label(
            boton,
            image=imagen_icono,
            bg=VERDE_OSCURO,
            width=35,
            cursor="hand2"
        )

        etiqueta_icono.image = imagen_icono
        etiqueta_icono.pack(side="left", padx=(5, 5))

        # Texto
        etiqueta_texto = tk.Label(
            boton,
            text=texto,
            font=("Segoe UI", 10),
            fg=BLANCO,
            bg=VERDE_OSCURO,
            cursor="hand2"
        )

        etiqueta_texto.pack(side="left")

        if comando is not None:

            def ejecutar(event=None):
                comando()

            def entrar(event):
                for widget in (boton, etiqueta_icono, etiqueta_texto):
                    widget.configure(bg=VERDE)

            def salir(event):
                for widget in (boton, etiqueta_icono, etiqueta_texto):
                    widget.configure(bg=VERDE_OSCURO)

            for widget in (boton, etiqueta_icono, etiqueta_texto):

                widget.bind("<Button-1>", ejecutar)
                widget.bind("<Enter>", entrar)
                widget.bind("<Leave>", salir)

        return boton

    # Inicio
    # inicio_boton = tk.Frame(
    #     menu,
    #     bg=VERDE,
    #     height=42,
    #     cursor="hand2"
    # )
    # inicio_boton.pack(
    #     fill="x",
    #     padx=8,
    #     pady=(5, 2)
    # )
    # inicio_boton.pack_propagate(False)

    # inicio_icono = tk.Label(
    #     inicio_boton,
    #     text="⌂",
    #     font=("Arial", 15, "bold"),
    #     fg=BLANCO,
    #     bg=VERDE,
    #     cursor="hand2"
    # )
    # inicio_icono.pack(side="left", padx=(10, 10))

    # inicio_texto = tk.Label(
    #     inicio_boton,
    #     text="Inicio",
    #     font=("Arial", 9, "bold"),
    #     fg=BLANCO,
    #     bg=VERDE,
    #     cursor="hand2"
    # )
    # inicio_texto.pack(side="left")

    # inicio_boton.bind(
    #     "<Button-1>",
    #     lambda event: volver_inicio()
    # )
    # inicio_icono.bind(
    #     "<Button-1>",
    #     lambda event: volver_inicio()
    # )
    # inicio_texto.bind(
    #     "<Button-1>",
    #     lambda event: volver_inicio()
    # )
    # =========================
    # BOTÓN INICIO
    # =========================

    inicio_boton = tk.Frame(
        menu,
        bg=VERDE,
        height=42,
        cursor="hand2"
    )

    inicio_boton.pack(
        fill="x",
        padx=8,
        pady=(5, 2)
    )

    inicio_boton.pack_propagate(False)

    # Icono PNG
    inicio_imagen = cargar_icono("house")

    inicio_icono = tk.Label(
        inicio_boton,
        image=inicio_imagen,
        bg=VERDE,
        cursor="hand2",
        width=35
    )

    inicio_icono.image = inicio_imagen

    inicio_icono.pack(
        side="left",
        padx=(5, 5)
    )

    # Texto
    inicio_texto = tk.Label(
        inicio_boton,
        text="Inicio",
        font=("Segoe UI", 10, "bold"),
        fg=BLANCO,
        bg=VERDE,
        cursor="hand2"
    )

    inicio_texto.pack(side="left")


    # Acción del botón
    def ejecutar_inicio(event=None):
        volver_inicio()


    inicio_boton.bind("<Button-1>", ejecutar_inicio)
    inicio_icono.bind("<Button-1>", ejecutar_inicio)
    inicio_texto.bind("<Button-1>", ejecutar_inicio)

    # Opciones del menú
    # crear_boton_menu(
    #     "Empleados",
    #     "●",
    #     lambda: mostrar_vista(crear_empleado)
    # )

    # crear_boton_menu(
    #     "Insumos",
    #     "◆",
    #     lambda: mostrar_vista(crear_insumo)
    # )

    # crear_boton_menu(
    #     "Movimientos",
    #     "↔",
    #     lambda: mostrar_vista(crear_movimientoinsumo)
    # )

    # crear_boton_menu(
    #     "Reportes",
    #     "▤",
    #     lambda: mostrar_vista(vista_reportes)
    # )

    # crear_boton_menu(
    #     "Configuración",
    #     "⚙",
    #     lambda: mostrar_vista(usuarios)
    # )
    
    # Empleados
    crear_boton_menu(
        "Empleados",
        "users",
        lambda: mostrar_vista(crear_empleado)
    )

    # Insumos
    crear_boton_menu(
        "Insumos",
        "box",
        lambda: mostrar_vista(crear_insumo)
    )

    # Movimientos
    crear_boton_menu(
        "Movimientos",
        "arrow-left-right",
        lambda: mostrar_vista(crear_movimientoinsumo)
    )

    # Reportes
    crear_boton_menu(
        "Reportes",
        "chart-no-axes-combined",
        lambda: mostrar_vista(vista_reportes)
    )

    # Configuración
    crear_boton_menu(
        "Configuración",
        "settings",
        lambda: mostrar_vista(usuarios)
    )

    def cerrar_sesion():
        if messagebox.askyesno(
            "Cerrar sesión",
            "¿Deseás cerrar sesión?"
        ):
            frame.destroy()

    crear_boton_menu(
        "Cerrar sesión",
        "log-out",
        cerrar_sesion
    )

    # =========================
    # ENCABEZADO
    # =========================
    cabecera = tk.Frame(panel_inicio, bg=FONDO)
    cabecera.pack(fill="x", padx=25, pady=(25, 15))

    tk.Label(
        cabecera,
        text="Hola, Administrador",
        font=("Arial", 19, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        cabecera,
        text="Aquí encontrarás un resumen actualizado del sistema.",
        font=("Arial", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=5)

    tk.Label(
        cabecera,
        text=date.today().strftime("%d/%m/%Y"),
        font=("Arial", 9),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="e")

    # =========================
    # TARJETAS DE ESTADÍSTICAS
    # =========================
    estadisticas = tk.Frame(panel_inicio, bg=FONDO)
    estadisticas.pack(fill="x", padx=25, pady=15)

    def tarjeta(icono, descripcion, color):
        contenedor = tk.Frame(
            estadisticas,
            bg=BLANCO,
            highlightbackground=BORDE,
            highlightthickness=1
        )
        contenedor.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            contenedor,
            text=icono,
            font=("Arial", 20),
            bg=BLANCO,
            fg=color
        ).pack(anchor="w", padx=15, pady=(12, 0))

        numero = tk.Label(
            contenedor,
            text="--",
            font=("Arial", 23, "bold"),
            bg=BLANCO,
            fg=TEXTO
        )
        numero.pack(anchor="w", padx=15)

        tk.Label(
            contenedor,
            text=descripcion,
            font=("Arial", 9),
            bg=BLANCO,
            fg=GRIS,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(5, 15))

        return numero

    lbl_empleados = tarjeta(
        "●●", "Empleados registrados", VERDE
    )

    lbl_insumos = tarjeta(
        "◆", "Insumos registrados", "#168CA0"
    )

    lbl_stock = tarjeta(
        "▲", "Insumos con stock bajo", ROJO
    )

    lbl_vencimientos = tarjeta(
        "▣", "Vencimientos próximos", VERDE
    )

    # =========================
    # ACCESOS RÁPIDOS
    # =========================
    inferiores = tk.Frame(panel_inicio, bg=FONDO)
    inferiores.pack(
        fill="x",
        padx=25,
        pady=15
    )

    def acceso_rapido(titulo, descripcion, comando):
        tarjeta = tk.Frame(
            inferiores,
            bg=BLANCO,
            highlightbackground=BORDE,
            highlightthickness=1
        )
        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg=BLANCO,
            fg=TEXTO
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(
            tarjeta,
            text=descripcion,
            font=("Arial", 9),
            bg=BLANCO,
            fg=GRIS
        ).pack(anchor="w", padx=20)

        tk.Button(
            tarjeta,
            text="Ver registros  →",
            command=comando,
            bg=VERDE,
            fg=BLANCO,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(anchor="w", padx=20, pady=20)

    acceso_rapido(
        "Registro de empleados",
        "Gestioná los empleados del centro de salud.",
        lambda: mostrar_vista(crear_empleado)
    )

    acceso_rapido(
        "Control de insumos",
        "Administrá el stock y los insumos registrados.",
        lambda: mostrar_vista(crear_insumo)
    )

    # =========================
    # ACTUALIZAR DATOS INICIALES
    # =========================
    actualizar_estadisticas()

    return frame
