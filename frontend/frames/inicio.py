
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime, timedelta
import requests

from frames.insumos import crear_insumo
from frames.empleados import crear_empleado
from frames.usuario import usuarios
from frames.movimientoInsumos import crear_movimientoinsumo
from frames.reportes import crear_reportes


API_URL = "http://localhost:3000/api/reportes"


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
        menu,
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

    def crear_boton_menu(texto, comando):
        tk.Button(
            menu,
            text=texto,
            command=comando,
            font=("Arial", 10),
            bg=VERDE_OSCURO,
            fg=BLANCO,
            activebackground=VERDE,
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=25,
            pady=12
        ).pack(fill="x", padx=8, pady=2)

    crear_boton_menu("⌂   Inicio", volver_inicio)
    crear_boton_menu(
        "●   Empleados",
        lambda: mostrar_vista(crear_empleado)
    )
    crear_boton_menu(
        "◆   Insumos",
        lambda: mostrar_vista(crear_insumo)
    )
    crear_boton_menu(
        "↔   Movimientos",
        lambda: mostrar_vista(crear_movimientoinsumo)
    )
    crear_boton_menu(
        "▤   Reportes",
        lambda: mostrar_vista(crear_reportes)
    )
    crear_boton_menu(
        "⚙   Configuración",
        lambda: mostrar_vista(usuarios)
    )

    def cerrar_sesion():
        if messagebox.askyesno(
            "Cerrar sesión",
            "¿Deseás cerrar sesión?"
        ):
            frame.destroy()

    crear_boton_menu("↪   Cerrar sesión", cerrar_sesion)

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
