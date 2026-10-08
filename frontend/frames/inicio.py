import tkinter as tk
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

    frame = tk.Frame(
        parent,
        bg=FONDO
    )
    def abrir_movimientoInsumos():
        vent = tk.Toplevel(parent)
        vent.title("Cuidar para Vivir - Insumos")
        vent.geometry("1100x700")
        vent.resizable(False, False)

        frame_insumos = crear_movimientoinsumo(vent)

        frame_insumos.pack(
            fill="both",
            expand=True
        )
    abrir_movimientoInsumos()
    # =========================
    # BARRA LATERAL
    # =========================

    menu = tk.Frame(
        frame,
        bg=VERDE_OSCURO,
        width=220
    )

    menu.pack(
        side="left",
        fill="y"
    )

    menu.pack_propagate(False)

    # -------------------------
    # Logo
    # -------------------------

    logo_frame = tk.Frame(
        menu,
        bg=VERDE_OSCURO
    )

    logo_frame.pack(
        fill="x",
        pady=(20, 10)
    )

    tk.Label(
        logo_frame,
        text="✚",
        font=("Arial", 25, "bold"),
        fg=BLANCO,
        bg=VERDE_OSCURO
    ).pack(side="left", padx=(18, 7))

    nombre_logo = tk.Frame(
        logo_frame,
        bg=VERDE_OSCURO
    )

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
    # OPCIONES DEL MENÚ
    # =========================

    def crear_boton_menu(texto, icono, comando=None):

        boton = tk.Frame(
            menu,
            bg=VERDE_OSCURO,
            height=42
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
            width=3
        )

        etiqueta_icono.pack(side="left")

        etiqueta_texto = tk.Label(
            boton,
            text=texto,
            font=("Arial", 9),
            fg=BLANCO,
            bg=VERDE_OSCURO
        )

        etiqueta_texto.pack(side="left")

        if comando:
            boton.bind("<Button-1>", lambda event: comando())
            etiqueta_icono.bind("<Button-1>", lambda event: comando())
            etiqueta_texto.bind("<Button-1>", lambda event: comando())

        return boton

    # Inicio seleccionado
    inicio_boton = tk.Frame(
        menu,
        bg=VERDE,
        height=42
    )

    inicio_boton.pack(
        fill="x",
        padx=8,
        pady=(5, 2)
    )

    inicio_boton.pack_propagate(False)

    tk.Label(
        inicio_boton,
        text="⌂",
        font=("Arial", 15, "bold"),
        fg=BLANCO,
        bg=VERDE
    ).pack(
        side="left",
        padx=(10, 10)
    )

    tk.Label(
        inicio_boton,
        text="Inicio",
        font=("Arial", 9, "bold"),
        fg=BLANCO,
        bg=VERDE
    ).pack(side="left")

    # crear_boton_menu("Empleados", "●")
    # crear_boton_menu("Insumos", "◆")
    # crear_boton_menu("Reportes", "▤")
    # crear_boton_menu("Configuración", "⚙")

    crear_boton_menu("Empleados", "●")
    crear_boton_menu("Insumos", "◆", abrir_insumos)
    crear_boton_menu("Reportes", "▤")
    crear_boton_menu("Configuración", "⚙")

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

    # Cerrar sesión
    crear_boton_menu("Cerrar sesión", "↪")

    # =========================
    # CONTENIDO PRINCIPAL
    # =========================

    contenido = tk.Frame(
        frame,
        bg=FONDO
    )

    contenido.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # CABECERA
    # =========================

    cabecera = tk.Frame(
        contenido,
        bg=FONDO,
        height=75
    )

    cabecera.pack(
        fill="x",
        padx=25,
        pady=(15, 0)
    )

    cabecera.pack_propagate(False)

    # Título
    titulo = tk.Frame(
        cabecera,
        bg=FONDO
    )

    titulo.pack(
        side="left",
        anchor="nw"
    )

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

    # Información derecha
    usuario = tk.Frame(
        cabecera,
        bg=FONDO
    )

    usuario.pack(
        side="right",
        anchor="ne"
    )

    tk.Label(
        usuario,
        text="▣  18 de mayo de 2025",
        font=("Arial", 8),
        fg=GRIS,
        bg=FONDO
    ).pack(
        side="left",
        padx=20
    )

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
    ).pack(
        side="left",
        padx=5
    )

    # =========================
    # TARJETAS DE ESTADÍSTICAS
    # =========================

    estadisticas = tk.Frame(
        contenido,
        bg=FONDO
    )

    estadisticas.pack(
        fill="x",
        padx=25,
        pady=(5, 10)
    )

    def crear_estadistica(parent, icono, numero, texto, color):

        tarjeta = tk.Frame(
            parent,
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

        # Icono
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
        contenido,
        bg=FONDO
    )

    inferiores.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    # -------------------------
    # Registro de empleados
    # -------------------------

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

    info_empleados = tk.Frame(
        empleados,
        bg=BLANCO
    )

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
        pady=5
    ).pack(anchor="w")

    # -------------------------
    # Control de insumos
    # -------------------------

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

    info_insumos = tk.Frame(
        insumos,
        bg=BLANCO
    )

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
        pady=5
    ).pack(anchor="w")

    return frame