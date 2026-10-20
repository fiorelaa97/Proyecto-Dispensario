
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/empleados"


# ============================================================
# COLORES ORIGINALES
# ============================================================

COLOR_PRINCIPAL = "#087F80"
COLOR_PRINCIPAL_OSCURO = "#056667"
COLOR_SECUNDARIO = "#0B7475"
COLOR_FONDO = "#F4FAFB"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO = "#173B3F"
COLOR_GRIS = "#6C7D80"
COLOR_BORDE = "#D8E7E9"
COLOR_VERDE = "#DDF5E3"
COLOR_VERDE_TEXTO = "#159447"
COLOR_ROJO = "#FFE0E3"
COLOR_ROJO_TEXTO = "#E94A5A"


# ============================================================
# INTERFAZ DE EMPLEADOS - SIN CLASES
# ============================================================

def crear_empleado(parent):

    # Estado de la pantalla
    empleados = []
    empleado_seleccionado = {"datos": None}

    # --------------------------------------------------------
    # CONTENEDOR PRINCIPAL
    # --------------------------------------------------------

    contenido = tk.Frame(parent, bg=COLOR_FONDO)
    contenido.pack(fill="both", expand=True, padx=22, pady=18)

    # --------------------------------------------------------
    # FUNCIONES AUXILIARES
    # --------------------------------------------------------

    def crear_boton(parent_boton, texto, comando, color=COLOR_PRINCIPAL):
        return tk.Button(
            parent_boton,
            text=texto,
            command=comando,
            bg=color,
            fg=COLOR_BLANCO,
            activebackground=COLOR_PRINCIPAL_OSCURO,
            activeforeground=COLOR_BLANCO,
            font=("Arial", 9, "bold"),
            relief="flat",
            bd=0,
            padx=13,
            pady=9,
            cursor="hand2"
        )

    def mostrar_error_api(respuesta):
        try:
            datos = respuesta.json()
            mensaje = datos.get("error", "Ocurrió un error")
            detalle = datos.get("detalle", "")

            if detalle:
                mensaje += "\n\n" + detalle

        except (ValueError, requests.exceptions.JSONDecodeError):
            mensaje = f"Error HTTP {respuesta.status_code}"

        messagebox.showerror("Error", mensaje, parent=contenido)

    def obtener_id(empleado):
        # Compatible con las dos convenciones habituales de nombres.
        return empleado.get("id", empleado.get("id_empleado"))

    def convertir_fecha(fecha):
        if not fecha:
            return ""

        if isinstance(fecha, datetime):
            return fecha.strftime("%d/%m/%Y")

        fecha = str(fecha)

        try:
            return datetime.fromisoformat(fecha[:10]).strftime("%d/%m/%Y")
        except ValueError:
            return fecha

    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    encabezado = tk.Frame(contenido, bg=COLOR_FONDO)
    encabezado.pack(fill="x", pady=(0, 15))

    tk.Label(
        encabezado,
        text="●",
        font=("Arial", 28, "bold"),
        fg=COLOR_PRINCIPAL,
        bg=COLOR_FONDO
    ).pack(side="left", padx=(0, 12))

    textos = tk.Frame(encabezado, bg=COLOR_FONDO)
    textos.pack(side="left")

    tk.Label(
        textos,
        text="Registro de empleados",
        font=("Arial", 21, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    tk.Label(
        textos,
        text="Gestioná la información del personal del centro de salud.",
        font=("Arial", 10),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    botones_superiores = tk.Frame(encabezado, bg=COLOR_FONDO)
    botones_superiores.pack(side="right")

    # --------------------------------------------------------
    # BÚSQUEDA Y FILTRO
    # --------------------------------------------------------

    barra = tk.Frame(contenido, bg=COLOR_FONDO)
    barra.pack(fill="x", pady=(0, 10))

    buscar_frame = tk.Frame(
        barra,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    buscar_frame.pack(side="left", fill="x", expand=True)

    tk.Label(
        buscar_frame,
        text="⌕",
        font=("Arial", 19),
        fg=COLOR_GRIS,
        bg=COLOR_BLANCO
    ).pack(side="left", padx=(10, 4))

    buscar_var = tk.StringVar()

    buscar_entry = tk.Entry(
        buscar_frame,
        textvariable=buscar_var,
        font=("Arial", 10),
        relief="flat",
        bd=0,
        fg=COLOR_TEXTO
    )
    buscar_entry.pack(side="left", fill="x", expand=True, ipady=8)

    estado_filtro = ttk.Combobox(
        barra,
        values=["Todos los estados", "Activo", "Inactivo"],
        state="readonly",
        font=("Arial", 10),
        width=20
    )
    estado_filtro.set("Todos los estados")
    estado_filtro.pack(side="right", padx=(10, 0), ipady=5)

    # --------------------------------------------------------
    # TABLA
    # --------------------------------------------------------

    tabla_frame = tk.Frame(
        contenido,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    tabla_frame.pack(fill="both", expand=True)

    columnas = (
        "id",
        "nombre",
        "apellido",
        "dni",
        "telefono",
        "cargo",
        "fecha_ingreso",
        "estado"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    encabezados_tabla = {
        "id": "ID",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "dni": "DNI",
        "telefono": "Teléfono",
        "cargo": "Cargo",
        "fecha_ingreso": "Fecha de ingreso",
        "estado": "Estado"
    }

    anchos = {
        "id": 45,
        "nombre": 100,
        "apellido": 100,
        "dni": 105,
        "telefono": 120,
        "cargo": 140,
        "fecha_ingreso": 120,
        "estado": 90
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados_tabla[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            minwidth=45,
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )
    tabla.configure(yscrollcommand=scrollbar.set)

    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    estilo = ttk.Style()
    estilo.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=35,
        fieldbackground=COLOR_BLANCO,
        borderwidth=0,
        font=("Arial", 9)
    )
    estilo.configure(
        "Treeview.Heading",
        background="#EAF4F5",
        foreground=COLOR_TEXTO,
        font=("Arial", 9, "bold"),
        relief="flat"
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#D9F0F0")],
        foreground=[("selected", COLOR_TEXTO)]
    )

    info_label = tk.Label(
        contenido,
        text="Mostrando 0 empleados",
        font=("Arial", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    )
    info_label.pack(anchor="w", pady=(7, 5))

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    formulario = tk.Frame(
        contenido,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    formulario.pack(fill="x", pady=(5, 0))

    titulo_formulario = tk.Frame(formulario, bg="#EAF4F5")
    titulo_formulario.pack(fill="x")

    tk.Label(
        titulo_formulario,
        text="＋",
        font=("Arial", 18, "bold"),
        fg=COLOR_PRINCIPAL,
        bg="#EAF4F5"
    ).pack(side="left", padx=(10, 5))

    titulo_formulario_label = tk.Label(
        titulo_formulario,
        text="Nuevo / Editar empleado",
        font=("Arial", 11, "bold"),
        fg=COLOR_TEXTO,
        bg="#EAF4F5"
    )
    titulo_formulario_label.pack(side="left", pady=9)

    campos = tk.Frame(formulario, bg=COLOR_BLANCO)
    campos.pack(fill="x", padx=14, pady=12)

    nombre_var = tk.StringVar()
    apellido_var = tk.StringVar()
    dni_var = tk.StringVar()
    telefono_var = tk.StringVar()
    cargo_var = tk.StringVar()
    fecha_var = tk.StringVar()
    estado_var = tk.StringVar(value="Activo")

    def crear_campo(parent_campo, titulo, variable, fila, columna):
        tk.Label(
            parent_campo,
            text=titulo,
            font=("Arial", 9, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            pady=(0, 4)
        )

        entrada = tk.Entry(
            parent_campo,
            textvariable=variable,
            font=("Arial", 9),
            relief="solid",
            bd=1,
            fg=COLOR_TEXTO
        )
        entrada.grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=(0, 12),
            ipady=6
        )
        return entrada

    crear_campo(campos, "Nombre *", nombre_var, 0, 0)
    crear_campo(campos, "Apellido *", apellido_var, 0, 1)
    crear_campo(campos, "DNI *", dni_var, 0, 2)
    crear_campo(campos, "Teléfono *", telefono_var, 0, 3)

    tk.Label(
        campos,
        text="Cargo *",
        font=("Arial", 9, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    ).grid(row=2, column=0, sticky="w", pady=(12, 4))

    cargo_combo = ttk.Combobox(
        campos,
        textvariable=cargo_var,
        values=[
            "Enfermera",
            "Médico",
            "Administrativa",
            "Personal de limpieza",
            "Recepcionista",
            "Director",
            "Otro"
        ],
        state="readonly"
    )
    cargo_combo.grid(row=3, column=0, sticky="ew", padx=(0, 12))

    crear_campo(campos, "Fecha de ingreso *", fecha_var, 2, 1)

    tk.Label(
        campos,
        text="Estado *",
        font=("Arial", 9, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_BLANCO
    ).grid(row=2, column=2, sticky="w", pady=(12, 4))

    estado_combo = ttk.Combobox(
        campos,
        textvariable=estado_var,
        values=["Activo", "Inactivo"],
        state="readonly"
    )
    estado_combo.grid(row=3, column=2, sticky="ew", padx=(0, 12))

    for i in range(4):
        campos.columnconfigure(i, weight=1)

    botones_formulario = tk.Frame(campos, bg=COLOR_BLANCO)
    botones_formulario.grid(row=3, column=3, sticky="e")

    # --------------------------------------------------------
    # FUNCIONES DE LA INTERFAZ
    # --------------------------------------------------------

    def mostrar_empleados(lista):
        for item in tabla.get_children():
            tabla.delete(item)

        for empleado in lista:
            id_empleado = obtener_id(empleado)

            if id_empleado is None:
                continue

            fecha = convertir_fecha(empleado.get("fecha_ingreso", ""))

            tabla.insert(
                "",
                "end",
                iid=str(id_empleado),
                values=(
                    id_empleado,
                    empleado.get("nombre", ""),
                    empleado.get("apellido", ""),
                    empleado.get("dni", ""),
                    empleado.get("telefono", ""),
                    empleado.get("cargo", ""),
                    fecha,
                    empleado.get("estado", "")
                )
            )

        info_label.config(text=f"Mostrando {len(lista)} empleados")

    def filtrar_empleados(event=None):
        texto = buscar_var.get().lower().strip()
        estado = estado_filtro.get()
        filtrados = []

        for empleado in empleados:
            texto_empleado = " ".join([
                str(empleado.get("nombre", "")),
                str(empleado.get("apellido", "")),
                str(empleado.get("dni", "")),
                str(empleado.get("telefono", "")),
                str(empleado.get("cargo", ""))
            ]).lower()

            coincide_texto = not texto or texto in texto_empleado
            coincide_estado = (
                estado == "Todos los estados"
                or str(empleado.get("estado", "")).lower() == estado.lower()
            )

            if coincide_texto and coincide_estado:
                filtrados.append(empleado)

        mostrar_empleados(filtrados)

    def cargar_empleados(mostrar_error=True):
        nonlocal empleados

        try:
            respuesta = requests.get(API_URL, timeout=5)

            if respuesta.status_code == 200:
                datos = respuesta.json()

                if not isinstance(datos, list):
                    messagebox.showerror(
                        "Error",
                        "La API no devolvió una lista de empleados.",
                        parent=contenido
                    )
                    return

                empleados = datos
                filtrar_empleados()
            else:
                if mostrar_error:
                    mostrar_error_api(respuesta)

        except requests.exceptions.ConnectionError:
            if mostrar_error:
                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con el backend.\n\n"
                    "Verificá que el servidor Express esté ejecutándose.",
                    parent=contenido
                )

        except requests.exceptions.Timeout:
            if mostrar_error:
                messagebox.showerror(
                    "Tiempo agotado",
                    "El servidor tardó demasiado en responder.",
                    parent=contenido
                )

        except Exception as error:
            if mostrar_error:
                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=contenido
                )

    def limpiar_formulario():
        empleado_seleccionado["datos"] = None

        nombre_var.set("")
        apellido_var.set("")
        dni_var.set("")
        telefono_var.set("")
        cargo_var.set("")
        fecha_var.set("")
        estado_var.set("Activo")

        titulo_formulario_label.config(text="Nuevo / Editar empleado")

        seleccion = tabla.selection()
        if seleccion:
            tabla.selection_remove(*seleccion)

    def nuevo_empleado():
        limpiar_formulario()
        titulo_formulario_label.config(text="Nuevo empleado")

    def seleccionar_empleado(event=None):
        seleccion = tabla.selection()

        if not seleccion:
            empleado_seleccionado["datos"] = None
            return

        try:
            id_seleccionado = int(seleccion[0])
        except ValueError:
            return

        for empleado in empleados:
            if str(obtener_id(empleado)) == str(id_seleccionado):
                empleado_seleccionado["datos"] = empleado
                return

        empleado_seleccionado["datos"] = None

    def editar_empleado():
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Editar empleado",
                "Seleccioná un empleado de la tabla.",
                parent=contenido
            )
            return

        seleccionar_empleado()

        empleado = empleado_seleccionado["datos"]

        if not empleado:
            messagebox.showerror(
                "Error",
                "No se pudo encontrar el empleado seleccionado.",
                parent=contenido
            )
            return

        nombre_var.set(empleado.get("nombre", ""))
        apellido_var.set(empleado.get("apellido", ""))
        dni_var.set(empleado.get("dni", ""))
        telefono_var.set(empleado.get("telefono", ""))
        cargo_var.set(empleado.get("cargo", ""))
        fecha_var.set(convertir_fecha(empleado.get("fecha_ingreso", "")))
        estado_var.set(empleado.get("estado", "Activo"))

        titulo_formulario_label.config(text="Editar empleado")

    def guardar_empleado():
        nombre = nombre_var.get().strip()
        apellido = apellido_var.get().strip()
        dni = dni_var.get().strip()
        telefono = telefono_var.get().strip()
        cargo = cargo_var.get().strip()
        fecha = fecha_var.get().strip()
        estado = estado_var.get().strip()

        if not nombre or not apellido or not dni:
            messagebox.showwarning(
                "Validación",
                "Completá el nombre, apellido y DNI.",
                parent=contenido
            )
            return

        if not telefono or not cargo or not fecha or not estado:
            messagebox.showwarning(
                "Validación",
                "Completá todos los campos obligatorios.",
                parent=contenido
            )
            return

        try:
            fecha_mysql = datetime.strptime(
                fecha,
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Fecha incorrecta",
                "La fecha debe tener el formato DD/MM/AAAA.\n"
                "Por ejemplo: 20/10/2026.",
                parent=contenido
            )
            return

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "telefono": telefono,
            "cargo": cargo,
            "fecha_ingreso": fecha_mysql,
            "estado": estado
        }

        empleado = empleado_seleccionado["datos"]

        try:
            if empleado is None:
                respuesta = requests.post(
                    API_URL,
                    json=datos,
                    timeout=5
                )

                mensaje_exito = "Empleado agregado correctamente."

            else:
                id_empleado = obtener_id(empleado)

                if id_empleado is None:
                    messagebox.showerror(
                        "Error",
                        "El empleado seleccionado no tiene un ID válido.",
                        parent=contenido
                    )
                    return

                respuesta = requests.put(
                    f"{API_URL}/{id_empleado}",
                    json=datos,
                    timeout=5
                )

                mensaje_exito = "Empleado actualizado correctamente."

            # Acepta cualquier respuesta HTTP exitosa (200, 201, 202 o 204).
            if respuesta.ok:
                messagebox.showinfo(
                    "Éxito",
                    mensaje_exito,
                    parent=contenido
                )
                limpiar_formulario()
                cargar_empleados()
            else:
                mostrar_error_api(respuesta)

        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor Express.",
                parent=contenido
            )

        except requests.exceptions.Timeout:
            messagebox.showerror(
                "Tiempo agotado",
                "El servidor tardó demasiado en responder.",
                parent=contenido
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=contenido
            )

    def eliminar_empleado():
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Eliminar empleado",
                "Seleccioná un empleado de la tabla.",
                parent=contenido
            )
            return

        seleccionar_empleado()
        empleado = empleado_seleccionado["datos"]

        if not empleado:
            messagebox.showerror(
                "Error",
                "No se pudo encontrar el empleado seleccionado.",
                parent=contenido
            )
            return

        nombre_completo = (
            f"{empleado.get('nombre', '')} "
            f"{empleado.get('apellido', '')}"
        ).strip()

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que querés eliminar a\n{nombre_completo}?",
            parent=contenido
        )

        if not confirmar:
            return

        id_empleado = obtener_id(empleado)
        if id_empleado is None:
            messagebox.showerror(
                "Error",
                "El empleado seleccionado no tiene un ID válido.",
                parent=contenido
            )
            return

        try:
            respuesta = requests.delete(
                f"{API_URL}/{id_empleado}",
                timeout=5
            )

            # DELETE puede responder 200 o 204, según cómo esté hecho Express.
            if respuesta.ok:
                messagebox.showinfo(
                    "Éxito",
                    "Empleado eliminado correctamente.",
                    parent=contenido
                )
                limpiar_formulario()
                cargar_empleados()
            else:
                mostrar_error_api(respuesta)

        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor Express.",
                parent=contenido
            )

        except requests.exceptions.Timeout:
            messagebox.showerror(
                "Tiempo agotado",
                "El servidor tardó demasiado en responder.",
                parent=contenido
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=contenido
            )

    # --------------------------------------------------------
    # BOTONES
    # --------------------------------------------------------

    crear_boton(
        botones_superiores,
        "＋  Agregar empleado",
        nuevo_empleado
    ).pack(side="left", padx=4)

    crear_boton(
        botones_superiores,
        "✎  Modificar",
        editar_empleado,
        "#117B7C"
    ).pack(side="left", padx=4)

    crear_boton(
        botones_superiores,
        "▣  Eliminar",
        eliminar_empleado,
        "#117B7C"
    ).pack(side="left", padx=4)

    crear_boton(
        botones_formulario,
        "✕  Cancelar",
        limpiar_formulario,
        "#6C7D80"
    ).pack(side="left", padx=5)

    crear_boton(
        botones_formulario,
        "▣  Guardar",
        guardar_empleado
    ).pack(side="left")

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    buscar_entry.bind("<KeyRelease>", filtrar_empleados)
    estado_filtro.bind("<<ComboboxSelected>>", filtrar_empleados)
    tabla.bind("<<TreeviewSelect>>", seleccionar_empleado)
    tabla.bind("<Double-1>", lambda event: editar_empleado())

    # Cargar datos iniciales
    cargar_empleados()

    return contenido



