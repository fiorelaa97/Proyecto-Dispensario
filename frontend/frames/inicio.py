
import tkinter as tk
from tkinter import messagebox

from frames.insumos import crear_insumo
from frames.empleados import crear_empleado
from frames.usuario import usuarios
from frames.movimientoInsumos import crear_movimientoinsumo


def crear_inicio(parent):

    # =========================
    # COLORES
    # =========================
    VERDE_OSCURO = "#006B6B"
    VERDE = "#009999"
    VERDE_CLARO = "#E5F7F7"
    BLANCO = "#FFFFFF"
    FONDO = "#F5FAFB"
    GRIS = "#64777D"
    GRIS_CLARO = "#DDEBED"
    TEXTO = "#17343A"
    ROJO = "#E94B4B"

    # =========================
    # FRAME PRINCIPAL
    # =========================
    frame = tk.Frame(parent, bg=FONDO)

    # =========================
    # BARRA LATERAL
    # =========================
    menu = tk.Frame(
        frame,
        bg=VERDE_OSCURO,
        width=220
    )
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    # Logo
    logo_frame = tk.Frame(menu, bg=VERDE_OSCURO)
    logo_frame.pack(fill="x", pady=(20, 10))

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
        text="Cuidar para Vivir",
        font=("Arial", 11, "bold"),
        fg=BLANCO,
        bg=VERDE_OSCURO
    ).pack(anchor="w")

    tk.Label(
        nombre_logo,
        text="Centro de Salud",
        font=("Arial", 8),
        fg="#BFE5E5",
        bg=VERDE_OSCURO
    ).pack(anchor="w")

    # =========================
    # CONTENIDO PRINCIPAL
    # =========================
    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(
        side="right",
        fill="both",
        expand=True
    )

    # Panel que conserva la pantalla de inicio
    panel_inicio = tk.Frame(contenido, bg=FONDO)
    panel_inicio.pack(fill="both", expand=True)

    # Referencia a la vista actualmente abierta
    vista_activa = None

    # =========================
    # CAMBIAR VISTAS
    # =========================
    def mostrar_vista(funcion_vista):

        nonlocal vista_activa

        # Ocultar el panel de inicio
        panel_inicio.pack_forget()

        # Cerrar la vista anterior
        if vista_activa is not None:
            vista_activa.destroy()
            vista_activa = None

        # Crear un contenedor para la nueva vista
        vista_activa = tk.Frame(
            contenido,
            bg=FONDO
        )
        vista_activa.pack(
            fill="both",
            expand=True
        )

        try:
            # La vista recibe el contenedor como parent
            resultado = funcion_vista(vista_activa)

            # Si devuelve otro widget, mostrarlo
            if (
                isinstance(resultado, tk.Widget)
                and resultado is not vista_activa
                and not resultado.winfo_manager()
            ):
                resultado.pack(
                    fill="both",
                    expand=True
                )

        except Exception as error:
            # Evitar dejar la pantalla vacía si falla la vista
            vista_activa.destroy()
            vista_activa = None

            panel_inicio.pack(
                fill="both",
                expand=True
            )

            messagebox.showerror(
                "Error al abrir la vista",
                "No se pudo abrir la pantalla seleccionada.\n\n"
                f"Detalle: {error}"
            )

    def volver_inicio():
        nonlocal vista_activa

        if vista_activa is not None:
            vista_activa.destroy()
            vista_activa = None

        panel_inicio.pack(
            fill="both",
            expand=True
        )

    # =========================
    # BOTONES DEL MENÚ
    # =========================
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

        etiqueta_icono = tk.Label(
            boton,
            text=icono,
            font=("Arial", 13),
            fg=BLANCO,
            bg=VERDE_OSCURO,
            width=3,
            cursor="hand2"
        )
        etiqueta_icono.pack(side="left")

        etiqueta_texto = tk.Label(
            boton,
            text=texto,
            font=("Arial", 9),
            fg=BLANCO,
            bg=VERDE_OSCURO,
            cursor="hand2"
        )
        etiqueta_texto.pack(side="left")

        if comando is not None:

            def ejecutar(event=None):
                comando()

            boton.bind("<Button-1>", ejecutar)
            etiqueta_icono.bind("<Button-1>", ejecutar)
            etiqueta_texto.bind("<Button-1>", ejecutar)

            # Efecto visual al pasar el mouse
            def entrar(event):
                boton.configure(bg=VERDE)
                etiqueta_icono.configure(bg=VERDE)
                etiqueta_texto.configure(bg=VERDE)

            def salir(event):
                boton.configure(bg=VERDE_OSCURO)
                etiqueta_icono.configure(bg=VERDE_OSCURO)
                etiqueta_texto.configure(bg=VERDE_OSCURO)

            for widget in (boton, etiqueta_icono, etiqueta_texto):
                widget.bind("<Enter>", entrar)
                widget.bind("<Leave>", salir)

        return boton

    # Inicio
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

    inicio_icono = tk.Label(
        inicio_boton,
        text="⌂",
        font=("Arial", 15, "bold"),
        fg=BLANCO,
        bg=VERDE,
        cursor="hand2"
    )
    inicio_icono.pack(side="left", padx=(10, 10))

    inicio_texto = tk.Label(
        inicio_boton,
        text="Inicio",
        font=("Arial", 9, "bold"),
        fg=BLANCO,
        bg=VERDE,
        cursor="hand2"
    )
    inicio_texto.pack(side="left")

    inicio_boton.bind(
        "<Button-1>",
        lambda event: volver_inicio()
    )
    inicio_icono.bind(
        "<Button-1>",
        lambda event: volver_inicio()
    )
    inicio_texto.bind(
        "<Button-1>",
        lambda event: volver_inicio()
    )

    # Opciones del menú
    crear_boton_menu(
        "Empleados",
        "●",
        lambda: mostrar_vista(crear_empleado)
    )

    crear_boton_menu(
        "Insumos",
        "◆",
        lambda: mostrar_vista(crear_insumo)
    )

    crear_boton_menu(
        "Movimientos",
        "↔",
        lambda: mostrar_vista(crear_movimientoinsumo)
    )

    crear_boton_menu(
        "Reportes",
        "▤",
        lambda: mostrar_vista(vista_reportes)
    )

    crear_boton_menu(
        "Configuración",
        "⚙",
        lambda: mostrar_vista(usuarios)
    )

    # Separador
    tk.Frame(
        menu,
        bg="#238888",
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=(150, 15)
    )

    # =========================
    # CERRAR SESIÓN
    # =========================
    def cerrar_sesion():

        confirmar = messagebox.askyesno(
            "Cerrar sesión",
            "¿Estás seguro de que querés cerrar sesión?"
        )

        if confirmar:
            # Destruye esta pantalla.
            # El controlador principal debe mostrar el login.
            frame.destroy()

    crear_boton_menu(
        "Cerrar sesión",
        "↪",
        cerrar_sesion
    )

    # =========================
    # VISTA DE REPORTES
    # =========================
    def vista_reportes(parent_vista):

        reportes = tk.Frame(
            parent_vista,
            bg=FONDO
        )
        reportes.pack(fill="both", expand=True)

        tk.Label(
            reportes,
            text="Reportes",
            font=("Arial", 20, "bold"),
            fg=TEXTO,
            bg=FONDO
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        tk.Label(
            reportes,
            text="La sección de reportes está pendiente de implementar.",
            font=("Arial", 11),
            fg=GRIS,
            bg=FONDO
        ).pack(
            anchor="w",
            padx=25
        )

        return reportes

    

    # =========================
    # CABECERA DEL INICIO
    # =========================
    cabecera = tk.Frame(
        panel_inicio,
        bg=FONDO,
        height=75
    )
    cabecera.pack(
        fill="x",
        padx=25,
        pady=(15, 0)
    )
    cabecera.pack_propagate(False)

    titulo = tk.Frame(cabecera, bg=FONDO)
    titulo.pack(side="left", anchor="nw")

    tk.Label(
        titulo,
        text="Hola, Administrador",
        font=("Arial", 16, "bold"),
        fg=TEXTO,
        bg=FONDO
    ).pack(anchor="w")

    tk.Label(
        titulo,
        text="Aquí encontrarás un resumen del sistema.",
        font=("Arial", 9),
        fg=GRIS,
        bg=FONDO
    ).pack(anchor="w", pady=(3, 0))

    usuario = tk.Frame(cabecera, bg=FONDO)
    usuario.pack(side="right", anchor="ne")

    tk.Label(
        usuario,
        text="▣  20 de octubre de 2026",
        font=("Arial", 8),
        fg=GRIS,
        bg=FONDO
    ).pack(side="left", padx=20)

    tk.Label(
        usuario,
        text="●",
        font=("Arial", 20),
        fg="#6C9299",
        bg=FONDO
    ).pack(side="left")

    tk.Label(
        usuario,
        text="Administrador ⌄",
        font=("Arial", 8, "bold"),
        fg=TEXTO,
        bg=FONDO
    ).pack(side="left", padx=5)

    # =========================
    # TARJETAS DE ESTADÍSTICAS
    # =========================
    estadisticas = tk.Frame(
        panel_inicio,
        bg=FONDO
    )
    estadisticas.pack(
        fill="x",
        padx=25,
        pady=(5, 10)
    )

    def crear_estadistica(parent_tarjeta, icono, numero, texto, color):

        tarjeta = tk.Frame(
            parent_tarjeta,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )
        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=4
        )

        tk.Label(
            tarjeta,
            text=icono,
            font=("Arial", 18),
            fg=color,
            bg=BLANCO
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 0)
        )

        tk.Label(
            tarjeta,
            text=numero,
            font=("Arial", 18, "bold"),
            fg=TEXTO,
            bg=BLANCO
        ).pack(
            anchor="w",
            padx=12
        )

        tk.Label(
            tarjeta,
            text=texto,
            font=("Arial", 7),
            fg=GRIS,
            bg=BLANCO,
            justify="left"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )

    crear_estadistica(
        estadisticas,
        "●●",
        "12",
        "Empleados\nregistrados",
        VERDE
    )

    crear_estadistica(
        estadisticas,
        "◆",
        "28",
        "Insumos\nen stock",
        "#168CA0"
    )

    crear_estadistica(
        estadisticas,
        "▲",
        "3",
        "Insumos con\nstock bajo",
        ROJO
    )

    crear_estadistica(
        estadisticas,
        "▣",
        "2",
        "Vencimientos\npróximos",
        VERDE
    )

    # =========================
    # TARJETAS INFERIORES
    # =========================
    inferiores = tk.Frame(
        panel_inicio,
        bg=FONDO
    )
    inferiores.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    # Tarjeta de empleados
    empleados = tk.Frame(
        inferiores,
        bg=BLANCO,
        highlightbackground=GRIS_CLARO,
        highlightthickness=1
    )
    empleados.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    tk.Label(
        empleados,
        text="●",
        font=("Arial", 22),
        fg=VERDE,
        bg=BLANCO
    ).pack(
        side="left",
        padx=(15, 10),
        pady=20
    )

    info_empleados = tk.Frame(empleados, bg=BLANCO)
    info_empleados.pack(
        side="left",
        fill="both",
        expand=True,
        pady=15
    )

    tk.Label(
        info_empleados,
        text="Registro de empleados",
        font=("Arial", 9, "bold"),
        fg=TEXTO,
        bg=BLANCO
    ).pack(anchor="w")

    tk.Label(
        info_empleados,
        text="Gestioná la información del\npersonal del centro de salud.",
        font=("Arial", 7),
        fg=GRIS,
        bg=BLANCO,
        justify="left"
    ).pack(
        anchor="w",
        pady=(5, 8)
    )

    tk.Button(
        info_empleados,
        text="Ver empleados  →",
        font=("Arial", 7, "bold"),
        fg=BLANCO,
        bg=VERDE,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=12,
        pady=5,
        command=lambda: mostrar_vista(crear_empleado)
    ).pack(anchor="w")

    # Tarjeta de insumos
    insumos = tk.Frame(
        inferiores,
        bg=BLANCO,
        highlightbackground=GRIS_CLARO,
        highlightthickness=1
    )
    insumos.pack(
        side="right",
        fill="both",
        expand=True,
        padx=4
    )

    tk.Label(
        insumos,
        text="◆",
        font=("Arial", 22),
        fg="#168CA0",
        bg=BLANCO
    ).pack(
        side="left",
        padx=(15, 10),
        pady=20
    )

    info_insumos = tk.Frame(insumos, bg=BLANCO)
    info_insumos.pack(
        side="left",
        fill="both",
        expand=True,
        pady=15
    )

    tk.Label(
        info_insumos,
        text="Control de insumos",
        font=("Arial", 9, "bold"),
        fg=TEXTO,
        bg=BLANCO
    ).pack(anchor="w")

    tk.Label(
        info_insumos,
        text="Administrá el stock y movimientos\nde insumos.",
        font=("Arial", 7),
        fg=GRIS,
        bg=BLANCO,
        justify="left"
    ).pack(
        anchor="w",
        pady=(5, 8)
    )

    tk.Button(
        info_insumos,
        text="Ver insumos  →",
        font=("Arial", 7, "bold"),
        fg=BLANCO,
        bg=VERDE,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=12,
        pady=5,
        command=lambda: mostrar_vista(crear_insumo)
    ).pack(anchor="w")

    return frame
