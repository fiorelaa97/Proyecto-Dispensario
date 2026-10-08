import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ==========================================================
# CONFIGURACIÓN DE LA API
# ==========================================================

API_URL = "http://localhost:3000/api/insumos"


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def crear_insumo(parent):

    # ------------------------------------------------------
    # COLORES
    # ------------------------------------------------------

    COLOR_PRINCIPAL = "#006B70"
    COLOR_PRINCIPAL_OSCURO = "#00565A"
    COLOR_FONDO = "#F5FAFA"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_TEXTO = "#23434A"
    COLOR_GRIS = "#6B858A"
    COLOR_BORDE = "#DCEBEC"
    COLOR_VERDE = "#D8F5DF"
    COLOR_VERDE_TEXTO = "#2B9A4B"
    COLOR_AMARILLO = "#FFF0C2"
    COLOR_AMARILLO_TEXTO = "#B57A00"

    # ------------------------------------------------------
    # LIMPIAR CONTENEDOR
    # ------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=COLOR_FONDO)

    # ======================================================
    # ENCABEZADO
    # ======================================================

    encabezado = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )
    encabezado.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )

    # Icono
    icono = tk.Label(
        encabezado,
        text="⬡",
        font=("Segoe UI", 25, "bold"),
        fg=COLOR_PRINCIPAL,
        bg=COLOR_FONDO
    )
    icono.pack(side="left", padx=(0, 10))

    titulo_frame = tk.Frame(
        encabezado,
        bg=COLOR_FONDO
    )
    titulo_frame.pack(side="left")

    tk.Label(
        titulo_frame,
        text="Control de insumos",
        font=("Segoe UI", 19, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    tk.Label(
        titulo_frame,
        text="Administración y control de insumos médicos",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    # Botón nuevo insumo
    btn_nuevo = tk.Button(
        encabezado,
        text="＋  Nuevo insumo",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=COLOR_PRINCIPAL,
        activebackground=COLOR_PRINCIPAL_OSCURO,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=8
    )
    btn_nuevo.pack(side="right")

    # ======================================================
    # BARRA DE BÚSQUEDA Y FILTRO
    # ======================================================

    controles = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )
    controles.pack(
        fill="x",
        padx=25,
        pady=10
    )

    # Búsqueda
    busqueda_frame = tk.Frame(
        controles,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    busqueda_frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 12)
    )

    tk.Label(
        busqueda_frame,
        text="⌕",
        font=("Segoe UI", 18),
        fg="#7C9A9F",
        bg=COLOR_BLANCO
    ).pack(
        side="left",
        padx=(10, 3)
    )

    entrada_busqueda = tk.Entry(
        busqueda_frame,
        font=("Segoe UI", 10),
        bd=0,
        relief="flat",
        fg=COLOR_TEXTO
    )
    entrada_busqueda.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=9
    )

    entrada_busqueda.insert(
        0,
        "Buscar por nombre o categoría..."
    )
    entrada_busqueda.configure(
        fg="#8BA1A5"
    )

    def limpiar_placeholder(event):
        if entrada_busqueda.get() == "Buscar por nombre o categoría...":
            entrada_busqueda.delete(0, tk.END)
            entrada_busqueda.configure(fg=COLOR_TEXTO)

    def colocar_placeholder(event):
        if entrada_busqueda.get().strip() == "":
            entrada_busqueda.insert(
                0,
                "Buscar por nombre o categoría..."
            )
            entrada_busqueda.configure(fg="#8BA1A5")

    entrada_busqueda.bind("<FocusIn>", limpiar_placeholder)
    entrada_busqueda.bind("<FocusOut>", colocar_placeholder)

    # Filtro de categoría
    categoria_var = tk.StringVar()
    combo_categoria = ttk.Combobox(
        controles,
        textvariable=categoria_var,
        state="readonly",
        width=22,
        font=("Segoe UI", 10)
    )
    combo_categoria["values"] = (
        "Todas las categorías",
        "Higiene",
        "Protección",
        "Curaciones",
        "Material médico",
        "Equipamiento"
    )
    combo_categoria.current(0)
    combo_categoria.pack(
        side="right",
        ipady=7
    )

    # ======================================================
    # ESTILOS DEL TREEVIEW
    # ======================================================

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except:
        pass

    estilo.configure(
        "Insumos.Treeview",
        background=COLOR_BLANCO,
        fieldbackground=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=42,
        font=("Segoe UI", 9),
        borderwidth=0
    )

    estilo.configure(
        "Insumos.Treeview.Heading",
        background="#F8FBFB",
        foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        padding=8
    )

    estilo.map(
        "Insumos.Treeview",
        background=[
            ("selected", "#D9F0F1")
        ],
        foreground=[
            ("selected", COLOR_TEXTO)
        ]
    )

    # ======================================================
    # TABLA
    # ======================================================

    tabla_frame = tk.Frame(
        parent,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    tabla_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(5, 0)
    )

    columnas = (
        "id",
        "nombre",
        "categoria",
        "cantidad",
        "stock_minimo",
        "vencimiento",
        "estado",
        "acciones"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        style="Insumos.Treeview"
    )

    # Encabezados
    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("categoria", text="Categoría")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("stock_minimo", text="Stock mínimo")
    tabla.heading("vencimiento", text="Vencimiento")
    tabla.heading("estado", text="Estado")
    tabla.heading("acciones", text="Acciones")

    # Anchos
    tabla.column("id", width=45, anchor="center")
    tabla.column("nombre", width=170, anchor="w")
    tabla.column("categoria", width=140, anchor="w")
    tabla.column("cantidad", width=90, anchor="center")
    tabla.column("stock_minimo", width=110, anchor="center")
    tabla.column("vencimiento", width=120, anchor="center")
    tabla.column("estado", width=110, anchor="center")
    tabla.column("acciones", width=110, anchor="center")

    # Scroll
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
    # PIE
    # ======================================================

    pie = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )
    pie.pack(
        fill="x",
        padx=25,
        pady=10
    )

    lbl_total = tk.Label(
        pie,
        text="Mostrando 0 insumos",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    )
    lbl_total.pack(anchor="w")

    # ======================================================
    # FUNCIONES
    # ======================================================

    insumos_data = []

    def cargar_insumos():

        nonlocal insumos_data

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code != 200:
                raise Exception(
                    f"Error HTTP {respuesta.status_code}"
                )

            insumos_data = respuesta.json()

            actualizar_tabla()

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                "Verificá que Node.js esté ejecutándose."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los insumos.\n\n{error}"
            )

    # ------------------------------------------------------
    # ACTUALIZAR TABLA
    # ------------------------------------------------------

    def actualizar_tabla():

        for item in tabla.get_children():
            tabla.delete(item)

        texto_busqueda = entrada_busqueda.get().lower().strip()

        if texto_busqueda == "buscar por nombre o categoría...":
            texto_busqueda = ""

        categoria_seleccionada = categoria_var.get()

        cantidad_mostrada = 0

        for insumo in insumos_data:

            nombre = str(
                insumo.get("nombre", "")
            )

            categoria = str(
                insumo.get("categoria", "")
            )

            # Filtro de búsqueda
            if texto_busqueda:

                if (
                    texto_busqueda not in nombre.lower()
                    and
                    texto_busqueda not in categoria.lower()
                ):
                    continue

            # Filtro categoría
            if (
                categoria_seleccionada
                != "Todas las categorías"
                and
                categoria != categoria_seleccionada
            ):
                continue

            cantidad = insumo.get("cantidad", 0)
            stock_minimo = insumo.get("stock_minimo", 0)

            estado = insumo.get(
                "estado",
                "Disponible"
            )

            # Si la cantidad es menor al stock mínimo
            # mostramos Stock bajo
            if cantidad <= stock_minimo:
                estado_mostrar = "Stock bajo"
            else:
                estado_mostrar = estado

            fecha = insumo.get(
                "fecha_vencimiento",
                ""
            )

            if fecha:
                fecha = str(fecha)[:10]

            tabla.insert(
                "",
                "end",
                values=(
                    insumo.get("id_insumo", ""),
                    nombre,
                    categoria,
                    cantidad,
                    stock_minimo,
                    fecha,
                    estado_mostrar,
                    "✎    🗑"
                ),
                tags=(
                    "stock_bajo"
                    if cantidad <= stock_minimo
                    else "disponible"
                )
            )

            cantidad_mostrada += 1

        lbl_total.configure(
            text=f"Mostrando {cantidad_mostrada} insumo"
                 f"{'s' if cantidad_mostrada != 1 else ''}"
        )

    # ======================================================
    # VENTANA NUEVO / EDITAR
    # ======================================================

    def abrir_formulario(insumo=None):

        editar = insumo is not None

        ventana = tk.Toplevel(parent)
        ventana.title(
            "Editar insumo" if editar else "Nuevo insumo"
        )
        ventana.geometry("480x560")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_BLANCO)

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        tk.Label(
            ventana,
            text=(
                "Editar insumo"
                if editar
                else "Nuevo insumo"
            ),
            font=("Segoe UI", 18, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 20)
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

        # Variables
        nombre_var = tk.StringVar()
        categoria_var_form = tk.StringVar()
        cantidad_var = tk.StringVar()
        stock_var = tk.StringVar()
        fecha_var = tk.StringVar()
        estado_var = tk.StringVar()

        if editar:

            nombre_var.set(
                insumo.get("nombre", "")
            )

            categoria_var_form.set(
                insumo.get("categoria", "")
            )

            cantidad_var.set(
                insumo.get("cantidad", "")
            )

            stock_var.set(
                insumo.get("stock_minimo", "")
            )

            fecha_var.set(
                str(
                    insumo.get(
                        "fecha_vencimiento",
                        ""
                    )
                )[:10]
            )

            estado_var.set(
                insumo.get(
                    "estado",
                    "Disponible"
                )
            )

        else:

            categoria_var_form.set("Higiene")
            estado_var.set("Disponible")

        # --------------------------------------------------
        # CAMPOS
        # --------------------------------------------------

        def campo(texto, variable):

            tk.Label(
                formulario,
                text=texto,
                font=("Segoe UI", 9, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_BLANCO
            ).pack(
                anchor="w",
                pady=(5, 4)
            )

            entrada = tk.Entry(
                formulario,
                textvariable=variable,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entrada.pack(
                fill="x",
                ipady=7
            )

            return entrada

        campo(
            "Nombre",
            nombre_var
        )

        tk.Label(
            formulario,
            text="Categoría",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).pack(
            anchor="w",
            pady=(12, 4)
        )

        combo_form_categoria = ttk.Combobox(
            formulario,
            textvariable=categoria_var_form,
            values=(
                "Higiene",
                "Protección",
                "Curaciones",
                "Material médico",
                "Equipamiento"
            ),
            state="readonly",
            font=("Segoe UI", 10)
        )

        combo_form_categoria.pack(
            fill="x",
            ipady=5
        )

        campo(
            "Cantidad",
            cantidad_var
        )

        campo(
            "Stock mínimo",
            stock_var
        )

        campo(
            "Fecha de vencimiento",
            fecha_var
        )

        tk.Label(
            formulario,
            text="Estado",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).pack(
            anchor="w",
            pady=(12, 4)
        )

        combo_estado = ttk.Combobox(
            formulario,
            textvariable=estado_var,
            values=(
                "Disponible",
                "No disponible"
            ),
            state="readonly",
            font=("Segoe UI", 10)
        )

        combo_estado.pack(
            fill="x",
            ipady=5
        )

        # --------------------------------------------------
        # GUARDAR
        # --------------------------------------------------

        def guardar():

            nombre = nombre_var.get().strip()
            categoria = categoria_var_form.get().strip()
            cantidad = cantidad_var.get().strip()
            stock = stock_var.get().strip()
            fecha = fecha_var.get().strip()
            estado = estado_var.get().strip()

            if not nombre:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá el nombre del insumo.",
                    parent=ventana
                )
                return

            if not cantidad or not stock:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresá cantidad y stock mínimo.",
                    parent=ventana
                )
                return

            try:
                cantidad = int(cantidad)
                stock = int(stock)
            except ValueError:

                messagebox.showwarning(
                    "Datos incorrectos",
                    "Cantidad y stock mínimo deben ser números.",
                    parent=ventana
                )
                return

            datos = {
                "nombre": nombre,
                "categoria": categoria,
                "cantidad": cantidad,
                "stock_minimo": stock,
                "fecha_vencimiento": fecha,
                "estado": estado
            }

            try:

                if editar:

                    id_insumo = insumo.get(
                        "id_insumo"
                    )

                    respuesta = requests.put(
                        f"{API_URL}/{id_insumo}",
                        json=datos,
                        timeout=5
                    )

                else:

                    respuesta = requests.post(
                        API_URL,
                        json=datos,
                        timeout=5
                    )

                if respuesta.status_code in (200, 201):

                    messagebox.showinfo(
                        "Correcto",
                        (
                            "Insumo actualizado correctamente."
                            if editar
                            else
                            "Insumo agregado correctamente."
                        ),
                        parent=ventana
                    )

                    ventana.destroy()
                    cargar_insumos()

                else:

                    try:
                        error = respuesta.json()
                    except:
                        error = respuesta.text

                    messagebox.showerror(
                        "Error",
                        f"No se pudo guardar el insumo.\n\n{error}",
                        parent=ventana
                    )

            except requests.exceptions.ConnectionError:

                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con el servidor.",
                    parent=ventana
                )

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        botones = tk.Frame(
            ventana,
            bg=COLOR_BLANCO
        )
        botones.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            font=("Segoe UI", 10),
            bg="#EEF3F3",
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=(10, 0)
        )

        tk.Button(
            botones,
            text="Guardar",
            command=guardar,
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PRINCIPAL,
            fg="white",
            activebackground=COLOR_PRINCIPAL_OSCURO,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(
            side="right"
        )

    # ======================================================
    # EDITAR / ELIMINAR
    # ======================================================

    def obtener_insumo_por_id(id_insumo):

        for insumo in insumos_data:

            if str(
                insumo.get("id_insumo")
            ) == str(id_insumo):

                return insumo

        return None

    def eliminar_insumo(id_insumo):

        insumo = obtener_insumo_por_id(
            id_insumo
        )

        if not insumo:
            return

        confirmar = messagebox.askyesno(
            "Eliminar insumo",
            f"¿Querés eliminar el insumo "
            f"'{insumo.get('nombre')}'?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_insumo}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Insumo eliminado correctamente."
                )

                cargar_insumos()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo eliminar el insumo."
                )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor."
            )

    # ------------------------------------------------------
    # CLICK EN ACCIONES
    # ------------------------------------------------------

    def click_tabla(event):

        region = tabla.identify(
            "region",
            event.x,
            event.y
        )

        if region != "cell":
            return

        fila = tabla.identify_row(event.y)
        columna = tabla.identify_column(event.x)

        if not fila:
            return

        valores = tabla.item(
            fila,
            "values"
        )

        if not valores:
            return

        id_insumo = valores[0]

        # Columna Acciones
        if columna == "#8":

            # mitad izquierda = editar
            x_fila = tabla.bbox(
                fila,
                "#8"
            )

            if not x_fila:
                return

            inicio_x = x_fila[0]
            ancho = x_fila[2]

            posicion = event.x - inicio_x

            if posicion < ancho / 2:

                insumo = obtener_insumo_por_id(
                    id_insumo
                )

                if insumo:
                    abrir_formulario(insumo)

            else:

                eliminar_insumo(
                    id_insumo
                )

    tabla.bind(
        "<Button-1>",
        click_tabla
    )

    # ======================================================
    # BUSCADOR
    # ======================================================

    entrada_busqueda.bind(
        "<KeyRelease>",
        lambda event: actualizar_tabla()
    )

    combo_categoria.bind(
        "<<ComboboxSelected>>",
        lambda event: actualizar_tabla()
    )

    # ======================================================
    # BOTÓN NUEVO
    # ======================================================

    btn_nuevo.configure(
        command=lambda: abrir_formulario()
    )

    # ======================================================
    # CARGAR DATOS AL INICIAR
    # ======================================================

    cargar_insumos()

    return parent