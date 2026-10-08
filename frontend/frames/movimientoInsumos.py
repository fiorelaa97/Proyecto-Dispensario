import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ==========================================================
# CONFIGURACIÓN DE LA API
# ==========================================================

API_URL = "http://localhost:3000"


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def crear_movimientoinsumo(parent):

    # ======================================================
    # COLORES
    # ======================================================

    COLOR_PRINCIPAL = "#006B6B"
    COLOR_SECUNDARIO = "#008C8C"
    COLOR_FONDO = "#F5FAFC"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_TEXTO = "#234052"
    COLOR_GRIS = "#6B7C85"
    COLOR_BORDE = "#D9E7EC"
    COLOR_ROJO = "#E74C3C"
    COLOR_VERDE = "#008C8C"

    # ======================================================
    # FRAME PRINCIPAL
    # ======================================================

    frame = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # ======================================================
    # ESTILOS
    # ======================================================

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=42,
        fieldbackground=COLOR_BLANCO,
        borderwidth=0,
        font=("Segoe UI", 9)
    )

    style.configure(
        "Treeview.Heading",
        background="#EAF5F8",
        foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#D8F0F0")
        ],
        foreground=[
            ("selected", COLOR_TEXTO)
        ]
    )

    style.configure(
        "TCombobox",
        padding=7,
        font=("Segoe UI", 9)
    )

    # ======================================================
    # VARIABLES
    # ======================================================

    movimientos = []
    insumos = []
    empleados = []

    pagina_actual = 1
    registros_por_pagina = 5

    # ======================================================
    # ENCABEZADO
    # ======================================================

    header = tk.Frame(
        frame,
        bg=COLOR_BLANCO,
        height=80
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    # Título

    titulo_frame = tk.Frame(
        header,
        bg=COLOR_BLANCO
    )

    titulo_frame.pack(
        side="left",
        padx=25,
        pady=12
    )

    titulo = tk.Label(
        titulo_frame,
        text="Movimientos de insumos",
        bg=COLOR_BLANCO,
        fg=COLOR_PRINCIPAL,
        font=("Segoe UI", 18, "bold")
    )

    titulo.pack(
        anchor="w"
    )

    subtitulo = tk.Label(
        titulo_frame,
        text="Registrá y consultá los movimientos de insumos del sistema.",
        bg=COLOR_BLANCO,
        fg=COLOR_GRIS,
        font=("Segoe UI", 9)
    )

    subtitulo.pack(
        anchor="w"
    )

    # ======================================================
    # CONTROLES SUPERIORES
    # ======================================================

    controles = tk.Frame(
        frame,
        bg=COLOR_FONDO
    )

    controles.pack(
        fill="x",
        padx=25,
        pady=(15, 10)
    )

    # --------------------------
    # BUSCADOR
    # --------------------------

    buscar_var = tk.StringVar()

    buscar_frame = tk.Frame(
        controles,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )

    buscar_frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10)
    )

    tk.Label(
        buscar_frame,
        text="🔍",
        bg=COLOR_BLANCO,
        fg=COLOR_GRIS,
        font=("Segoe UI", 10)
    ).pack(
        side="left",
        padx=(10, 5)
    )

    buscar_entry = tk.Entry(
        buscar_frame,
        textvariable=buscar_var,
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO,
        bd=0,
        relief="flat",
        font=("Segoe UI", 9)
    )

    buscar_entry.pack(
        side="left",
        fill="x",
        expand=True,
        pady=10
    )

    # --------------------------
    # FILTRO TIPO
    # --------------------------

    filtro_var = tk.StringVar(
        value="Todos los tipos"
    )

    filtro = ttk.Combobox(
        controles,
        textvariable=filtro_var,
        values=[
            "Todos los tipos",
            "Entrada",
            "Salida"
        ],
        state="readonly",
        width=18
    )

    filtro.pack(
        side="left",
        padx=(0, 10)
    )

    # --------------------------
    # BOTÓN NUEVO
    # --------------------------

    boton_nuevo = tk.Button(
        controles,
        text="+  Nuevo movimiento",
        bg=COLOR_PRINCIPAL,
        fg="white",
        activebackground=COLOR_SECUNDARIO,
        activeforeground="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2"
    )

    boton_nuevo.pack(
        side="right"
    )

    # ======================================================
    # CONTENEDOR TABLA
    # ======================================================

    tabla_frame = tk.Frame(
        frame,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )

    tabla_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 10)
    )

    # ======================================================
    # TABLA
    # ======================================================

    columnas = (
        "id",
        "fecha",
        "tipo",
        "insumo",
        "empleado",
        "cantidad",
        "motivo",
        "acciones"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "fecha",
        text="Fecha"
    )

    tabla.heading(
        "tipo",
        text="Tipo"
    )

    tabla.heading(
        "insumo",
        text="Insumo"
    )

    tabla.heading(
        "empleado",
        text="Empleado"
    )

    tabla.heading(
        "cantidad",
        text="Cantidad"
    )

    tabla.heading(
        "motivo",
        text="Motivo"
    )

    tabla.heading(
        "acciones",
        text=""
    )

    tabla.column(
        "id",
        width=45,
        anchor="center"
    )

    tabla.column(
        "fecha",
        width=95,
        anchor="center"
    )

    tabla.column(
        "tipo",
        width=80,
        anchor="center"
    )

    tabla.column(
        "insumo",
        width=140
    )

    tabla.column(
        "empleado",
        width=140
    )

    tabla.column(
        "cantidad",
        width=80,
        anchor="center"
    )

    tabla.column(
        "motivo",
        width=200
    )

    tabla.column(
        "acciones",
        width=100,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ======================================================
    # PIE DE TABLA
    # ======================================================

    pie = tk.Frame(
        frame,
        bg=COLOR_FONDO
    )

    pie.pack(
        fill="x",
        padx=25,
        pady=(0, 15)
    )

    info_registros = tk.Label(
        pie,
        text="Mostrando 0 movimientos",
        bg=COLOR_FONDO,
        fg=COLOR_GRIS,
        font=("Segoe UI", 8)
    )

    info_registros.pack(
        side="left"
    )

    # ======================================================
    # FUNCIONES AUXILIARES
    # ======================================================

    def obtener_nombre_insumo(id_insumo):
        for insumo in insumos:
            if str(insumo.get("id_insumo")) == str(id_insumo):
                return insumo.get("nombre", "Sin nombre")

        return f"ID {id_insumo}"

    def obtener_nombre_empleado(id_empleado):

        if id_empleado is None:
            return "Sin asignar"

        for empleado in empleados:

            if str(
                empleado.get("id_empleado")
            ) == str(id_empleado):

                nombre = empleado.get("nombre", "")
                apellido = empleado.get("apellido", "")

                nombre_completo = (
                    f"{nombre} {apellido}"
                ).strip()

                if nombre_completo:
                    return nombre_completo

                return str(id_empleado)

        return f"ID {id_empleado}"

    # ======================================================
    # CARGAR INSUMOS
    # ======================================================

    def cargar_insumos():

        nonlocal insumos

        try:

            respuesta = requests.get(
                f"{API_URL}/insumos",
                timeout=5
            )

            if respuesta.status_code == 200:

                insumos = respuesta.json()

        except requests.exceptions.RequestException as error:

            print(
                "Error cargando insumos:",
                error
            )

    # ======================================================
    # CARGAR EMPLEADOS
    # ======================================================

    def cargar_empleados():

        nonlocal empleados

        try:

            respuesta = requests.get(
                f"{API_URL}/empleados",
                timeout=5
            )

            if respuesta.status_code == 200:

                empleados = respuesta.json()

        except requests.exceptions.RequestException as error:

            print(
                "Error cargando empleados:",
                error
            )

    # ======================================================
    # CARGAR MOVIMIENTOS
    # ======================================================

    def cargar_movimientos():

        nonlocal movimientos

        try:

            respuesta = requests.get(
                f"{API_URL}/movimientos-insumos",
                timeout=5
            )

            if respuesta.status_code == 200:

                movimientos = respuesta.json()

                actualizar_tabla()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener los movimientos."
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{error}"
            )

    # ======================================================
    # FILTRAR MOVIMIENTOS
    # ======================================================

    def obtener_movimientos_filtrados():

        texto = buscar_var.get().lower().strip()
        tipo = filtro_var.get()

        resultado = []

        for movimiento in movimientos:

            nombre_insumo = obtener_nombre_insumo(
                movimiento.get("id_insumo")
            ).lower()

            nombre_empleado = obtener_nombre_empleado(
                movimiento.get("id_empleado")
            ).lower()

            motivo = str(
                movimiento.get("motivo", "")
            ).lower()

            tipo_movimiento = str(
                movimiento.get("tipo_movimiento", "")
            )

            coincide_busqueda = (
                texto == ""
                or texto in nombre_insumo
                or texto in nombre_empleado
                or texto in motivo
                or texto in tipo_movimiento.lower()
            )

            coincide_tipo = (
                tipo == "Todos los tipos"
                or tipo_movimiento.lower() == tipo.lower()
            )

            if coincide_busqueda and coincide_tipo:

                resultado.append(movimiento)

        return resultado

    # ======================================================
    # ACTUALIZAR TABLA
    # ======================================================

    def actualizar_tabla():

        nonlocal pagina_actual

        for item in tabla.get_children():

            tabla.delete(item)

        filtrados = obtener_movimientos_filtrados()

        total = len(filtrados)

        inicio = (
            pagina_actual - 1
        ) * registros_por_pagina

        fin = inicio + registros_por_pagina

        registros = filtrados[
            inicio:fin
        ]

        for movimiento in registros:

            id_movimiento = movimiento.get(
                "id_movimiento"
            )

            fecha = movimiento.get(
                "fecha",
                ""
            )

            tipo = movimiento.get(
                "tipo_movimiento",
                ""
            )

            nombre_insumo = obtener_nombre_insumo(
                movimiento.get("id_insumo")
            )

            nombre_empleado = obtener_nombre_empleado(
                movimiento.get("id_empleado")
            )

            cantidad = movimiento.get(
                "cantidad",
                0
            )

            motivo = movimiento.get(
                "motivo",
                ""
            )

            tabla.insert(
                "",
                "end",
                values=(
                    id_movimiento,
                    fecha,
                    tipo,
                    nombre_insumo,
                    nombre_empleado,
                    cantidad,
                    motivo,
                    "✎  🗑"
                )
            )

        if total == 0:

            info_registros.config(
                text="No se encontraron movimientos"
            )

        else:

            primero = inicio + 1
            ultimo = min(
                fin,
                total
            )

            info_registros.config(
                text=(
                    f"Mostrando {primero} - "
                    f"{ultimo} de {total} movimientos"
                )
            )

    # ======================================================
    # VENTANA CREAR / EDITAR
    # ======================================================

    def abrir_formulario(movimiento=None):

        editando = movimiento is not None

        ventana = tk.Toplevel(
            frame
        )

        ventana.title(
            "Editar movimiento"
            if editando
            else "Nuevo movimiento"
        )

        ventana.geometry(
            "500x560"
        )

        ventana.configure(
            bg=COLOR_BLANCO
        )

        ventana.resizable(
            False,
            False
        )

        # --------------------------
        # TÍTULO
        # --------------------------

        tk.Label(
            ventana,
            text=(
                "Editar movimiento"
                if editando
                else "Nuevo movimiento"
            ),
            bg=COLOR_BLANCO,
            fg=COLOR_PRINCIPAL,
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            ventana,
            text="Completá los datos del movimiento.",
            bg=COLOR_BLANCO,
            fg=COLOR_GRIS,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        formulario = tk.Frame(
            ventana,
            bg=COLOR_BLANCO
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # ==================================================
        # INSUMO
        # ==================================================

        tk.Label(
            formulario,
            text="Insumo *",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        insumos_dict = {}

        for insumo in insumos:

            texto = insumo.get(
                "nombre",
                f"ID {insumo.get('id_insumo')}"
            )

            insumos_dict[texto] = insumo.get(
                "id_insumo"
            )

        insumo_var = tk.StringVar()

        combo_insumo = ttk.Combobox(
            formulario,
            textvariable=insumo_var,
            values=list(insumos_dict.keys()),
            state="readonly"
        )

        combo_insumo.pack(
            fill="x",
            pady=(5, 15)
        )

        # ==================================================
        # EMPLEADO
        # ==================================================

        tk.Label(
            formulario,
            text="Empleado",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        empleados_dict = {
            "Sin asignar": None
        }

        for empleado in empleados:

            nombre = empleado.get(
                "nombre",
                ""
            )

            apellido = empleado.get(
                "apellido",
                ""
            )

            nombre_completo = (
                f"{nombre} {apellido}"
            ).strip()

            if not nombre_completo:

                nombre_completo = (
                    f"Empleado {empleado.get('id_empleado')}"
                )

            empleados_dict[
                nombre_completo
            ] = empleado.get(
                "id_empleado"
            )

        empleado_var = tk.StringVar()

        combo_empleado = ttk.Combobox(
            formulario,
            textvariable=empleado_var,
            values=list(empleados_dict.keys()),
            state="readonly"
        )

        combo_empleado.pack(
            fill="x",
            pady=(5, 15)
        )

        # ==================================================
        # TIPO
        # ==================================================

        tk.Label(
            formulario,
            text="Tipo de movimiento *",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        tipo_var = tk.StringVar()

        combo_tipo = ttk.Combobox(
            formulario,
            textvariable=tipo_var,
            values=[
                "Entrada",
                "Salida"
            ],
            state="readonly"
        )

        combo_tipo.pack(
            fill="x",
            pady=(5, 15)
        )

        # ==================================================
        # CANTIDAD
        # ==================================================

        tk.Label(
            formulario,
            text="Cantidad *",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        cantidad_var = tk.StringVar()

        entrada_cantidad = tk.Entry(
            formulario,
            textvariable=cantidad_var,
            font=("Segoe UI", 9),
            bd=1,
            relief="solid"
        )

        entrada_cantidad.pack(
            fill="x",
            pady=(5, 15),
            ipady=6
        )

        # ==================================================
        # FECHA
        # ==================================================

        tk.Label(
            formulario,
            text="Fecha *",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        fecha_var = tk.StringVar()

        entrada_fecha = tk.Entry(
            formulario,
            textvariable=fecha_var,
            font=("Segoe UI", 9),
            bd=1,
            relief="solid"
        )

        entrada_fecha.pack(
            fill="x",
            pady=(5, 15),
            ipady=6
        )

        # ==================================================
        # MOTIVO
        # ==================================================

        tk.Label(
            formulario,
            text="Motivo",
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        motivo_var = tk.StringVar()

        entrada_motivo = tk.Entry(
            formulario,
            textvariable=motivo_var,
            font=("Segoe UI", 9),
            bd=1,
            relief="solid"
        )

        entrada_motivo.pack(
            fill="x",
            pady=(5, 20),
            ipady=6
        )

        # ==================================================
        # CARGAR DATOS SI ES EDICIÓN
        # ==================================================

        if editando:

            id_insumo = movimiento.get(
                "id_insumo"
            )

            for nombre, id_i in insumos_dict.items():

                if str(id_i) == str(id_insumo):

                    insumo_var.set(nombre)

                    break

            id_empleado = movimiento.get(
                "id_empleado"
            )

            for nombre, id_e in empleados_dict.items():

                if (
                    id_e is not None
                    and str(id_e) == str(id_empleado)
                ):

                    empleado_var.set(nombre)

                    break

            if id_empleado is None:

                empleado_var.set("Sin asignar")

            tipo_var.set(
                movimiento.get(
                    "tipo_movimiento",
                    ""
                ).capitalize()
            )

            cantidad_var.set(
                str(
                    movimiento.get(
                        "cantidad",
                        ""
                    )
                )
            )

            fecha_var.set(
                str(
                    movimiento.get(
                        "fecha",
                        ""
                    )
                )
            )

            motivo_var.set(
                movimiento.get(
                    "motivo",
                    ""
                )
            )

        else:

            fecha_var.set(
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )

        # ==================================================
        # BOTONES
        # ==================================================

        botones = tk.Frame(
            ventana,
            bg=COLOR_BLANCO
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        def guardar():

            # ------------------------------
            # VALIDACIONES
            # ------------------------------

            if not insumo_var.get():

                messagebox.showwarning(
                    "Datos incompletos",
                    "Seleccioná un insumo."
                )

                return

            if not tipo_var.get():

                messagebox.showwarning(
                    "Datos incompletos",
                    "Seleccioná el tipo de movimiento."
                )

                return

            try:

                cantidad = int(
                    cantidad_var.get()
                )

                if cantidad <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Cantidad incorrecta",
                    "La cantidad debe ser un número mayor a 0."
                )

                return

            if not fecha_var.get():

                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá una fecha."
                )

                return

            # ------------------------------
            # DATOS
            # ------------------------------

            id_insumo = insumos_dict.get(
                insumo_var.get()
            )

            id_empleado = empleados_dict.get(
                empleado_var.get()
            )

            datos = {
                "id_insumo": id_insumo,
                "id_empleado": id_empleado,
                "tipo_movimiento": tipo_var.get(),
                "cantidad": cantidad,
                "fecha": fecha_var.get(),
                "motivo": motivo_var.get()
            }

            try:

                if editando:

                    id_movimiento = movimiento.get(
                        "id_movimiento"
                    )

                    respuesta = requests.put(
                        f"{API_URL}/movimientos-insumos/{id_movimiento}",
                        json=datos,
                        timeout=5
                    )

                else:

                    respuesta = requests.post(
                        f"{API_URL}/movimientos-insumos",
                        json=datos,
                        timeout=5
                    )

                if respuesta.status_code in (
                    200,
                    201
                ):

                    messagebox.showinfo(
                        "Correcto",
                        (
                            "Movimiento actualizado correctamente."
                            if editando
                            else
                            "Movimiento creado correctamente."
                        )
                    )

                    ventana.destroy()

                    cargar_movimientos()

                else:

                    try:
                        detalle = respuesta.json().get(
                            "detalle",
                            respuesta.text
                        )
                    except:
                        detalle = respuesta.text

                    messagebox.showerror(
                        "Error",
                        f"No se pudo guardar el movimiento.\n\n{detalle}"
                    )

            except requests.exceptions.RequestException as error:

                messagebox.showerror(
                    "Error de conexión",
                    f"No se pudo conectar con el servidor.\n\n{error}"
                )

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            bg="#EDF3F5",
            fg=COLOR_TEXTO,
            activebackground="#DDE8EB",
            bd=0,
            padx=20,
            pady=9,
            font=("Segoe UI", 9),
            cursor="hand2"
        ).pack(
            side="right",
            padx=(10, 0)
        )

        tk.Button(
            botones,
            text=(
                "Guardar cambios"
                if editando
                else "Guardar movimiento"
            ),
            command=guardar,
            bg=COLOR_PRINCIPAL,
            fg="white",
            activebackground=COLOR_SECUNDARIO,
            activeforeground="white",
            bd=0,
            padx=20,
            pady=9,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="right"
        )

    # ======================================================
    # EDITAR MOVIMIENTO
    # ======================================================

    def editar_movimiento(movimiento):

        abrir_formulario(
            movimiento
        )

    # ======================================================
    # ELIMINAR MOVIMIENTO
    # ======================================================

    def eliminar_movimiento(movimiento):

        id_movimiento = movimiento.get(
            "id_movimiento"
        )

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de que querés eliminar este movimiento?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/movimientos-insumos/{id_movimiento}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Movimiento eliminado correctamente."
                )

                cargar_movimientos()

            else:

                try:

                    detalle = respuesta.json().get(
                        "detalle",
                        respuesta.text
                    )

                except:

                    detalle = respuesta.text

                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el movimiento.\n\n{detalle}"
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{error}"
            )

    # ======================================================
    # CLICK EN LA TABLA
    # ======================================================

    def click_tabla(event):

        region = tabla.identify(
            "region",
            event.x,
            event.y
        )

        if region != "cell":
            return

        columna = tabla.identify_column(
            event.x
        )

        fila = tabla.identify_row(
            event.y
        )

        if not fila:
            return

        if columna != "#8":
            return

        valores = tabla.item(
            fila,
            "values"
        )

        if not valores:
            return

        id_movimiento = valores[0]

        movimiento_encontrado = None

        for movimiento in movimientos:

            if str(
                movimiento.get(
                    "id_movimiento"
                )
            ) == str(id_movimiento):

                movimiento_encontrado = movimiento

                break

        if movimiento_encontrado is None:
            return

        # --------------------------
        # MENÚ DE ACCIONES
        # --------------------------

        menu = tk.Menu(
            frame,
            tearoff=0
        )

        menu.add_command(
            label="✎  Editar",
            command=lambda: editar_movimiento(
                movimiento_encontrado
            )
        )

        menu.add_command(
            label="🗑  Eliminar",
            command=lambda: eliminar_movimiento(
                movimiento_encontrado
            )
        )

        menu.tk_popup(
            event.x_root,
            event.y_root
        )

    tabla.bind(
        "<Button-1>",
        click_tabla
    )

    # ======================================================
    # BÚSQUEDA
    # ======================================================

    buscar_var.trace_add(
        "write",
        lambda *args: actualizar_tabla()
    )

    filtro.bind(
        "<<ComboboxSelected>>",
        lambda event: actualizar_tabla()
    )

    # ======================================================
    # BOTÓN NUEVO
    # ======================================================

    boton_nuevo.config(
        command=lambda: abrir_formulario()
    )

    # ======================================================
    # CARGA INICIAL
    # ======================================================

    cargar_insumos()
    cargar_empleados()
    cargar_movimientos()

    return frame