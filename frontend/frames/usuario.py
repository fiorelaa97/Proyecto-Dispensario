
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Dirección de tu API de Express
API_URL = "http://localhost:3000/api"


def usuarios(parent):
    """Interfaz de administración de usuarios."""

    ventana = tk.Frame(parent, bg="#F5F7F8")
    ventana.pack(fill="both", expand=True)

    COLOR_PRINCIPAL = "#005B5B"
    COLOR_SECUNDARIO = "#087F83"
    COLOR_CLARO = "#E4F3F8"
    COLOR_FONDO = "#F5F7F8"
    COLOR_TEXTO = "#123B4A"
    COLOR_ROJO = "#E53945"
    COLOR_BLANCO = "#FFFFFF"

    usuario_seleccionado = {"id": None}
    empleados = []

    # ---------------- ESTILOS ----------------

    estilo = ttk.Style()
    estilo.configure(
        "Usuarios.Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=36,
        font=("Arial", 10),
        fieldbackground=COLOR_BLANCO
    )
    estilo.configure(
        "Usuarios.Treeview.Heading",
        background=COLOR_CLARO,
        foreground=COLOR_TEXTO,
        font=("Arial", 10, "bold"),
        padding=9
    )
    estilo.map(
        "Usuarios.Treeview",
        background=[("selected", "#B8E3E0")],
        foreground=[("selected", COLOR_TEXTO)]
    )

    # ---------------- FUNCIONES DE LA API ----------------

    def obtener_lista(datos, clave):
        """Acepta respuestas JSON en forma de lista o de objeto."""
        if isinstance(datos, list):
            return datos
        if isinstance(datos, dict):
            resultado = datos.get(clave, [])
            if isinstance(resultado, list):
                return resultado
        return []

    def consultar_empleados():
        nonlocal empleados

        try:
            respuesta = requests.get(
                f"{API_URL}/empleados", timeout=5
            )
            respuesta.raise_for_status()

            empleados = obtener_lista(
                respuesta.json(), "empleados"
            )

            opciones = []
            for empleado in empleados:
                identificador = empleado.get("id_empleado")
                nombre = empleado.get("nombre", "")
                apellido = empleado.get("apellido", "")
                opciones.append(
                    f"{identificador} - {nombre} {apellido}".strip()
                )

            combo_empleado["values"] = opciones

        except requests.RequestException as error:
            empleados = []
            combo_empleado["values"] = []
            messagebox.showwarning(
                "Empleados",
                "No se pudieron cargar los empleados.\n\n"
                f"Verificá la API de Express.\n{error}",
                parent=ventana
            )

    def cargar_usuarios():
        tabla.delete(*tabla.get_children())

        try:
            respuesta = requests.get(
                f"{API_URL}/usuarios", timeout=5
            )
            respuesta.raise_for_status()

            lista = obtener_lista(
                respuesta.json(), "usuarios"
            )

            filtro_texto = entrada_busqueda.get().strip().lower()
            filtro_rol = combo_filtro.get()

            cantidad = 0

            for usuario in lista:
                nombre = str(
                    usuario.get("nombre_usuario", "")
                )
                rol = str(usuario.get("rol") or "")
                id_empleado = usuario.get("id_empleado")

                empleado_nombre = "Sin empleado"
                for empleado in empleados:
                    if str(empleado.get("id_empleado")) == str(id_empleado):
                        empleado_nombre = (
                            f"{empleado.get('nombre', '')} "
                            f"{empleado.get('apellido', '')}"
                        ).strip()
                        break

                texto_busqueda = (
                    nombre + " " + rol + " " + empleado_nombre
                ).lower()

                if filtro_texto and filtro_texto not in texto_busqueda:
                    continue

                if filtro_rol != "Todos los roles" and rol != filtro_rol:
                    continue

                tabla.insert(
                    "",
                    "end",
                    iid=str(usuario["id_usuario"]),
                    values=(
                        usuario["id_usuario"],
                        nombre,
                        rol,
                        empleado_nombre,
                    )
                )
                cantidad += 1

            etiqueta_total.config(
                text=f"Mostrando {cantidad} usuarios"
            )

        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los usuarios.\n\n"
                f"{error}",
                parent=ventana
            )

    def limpiar_formulario():
        usuario_seleccionado["id"] = None
        entrada_nombre.delete(0, "end")
        entrada_contrasena.delete(0, "end")
        combo_rol.set("")
        combo_empleado.set("")
        etiqueta_formulario.config(text="Nuevo usuario")

    def seleccionar_usuario(event=None):
        seleccion = tabla.selection()
        if not seleccion:
            return

        fila = tabla.item(seleccion[0], "values")
        usuario_seleccionado["id"] = fila[0]

        entrada_nombre.delete(0, "end")
        entrada_nombre.insert(0, fila[1])

        # La contraseña nunca se obtiene de la tabla.
        entrada_contrasena.delete(0, "end")

        combo_rol.set(fila[2])

        id_actual = None
        for empleado in empleados:
            nombre_completo = (
                f"{empleado.get('nombre', '')} "
                f"{empleado.get('apellido', '')}"
            ).strip()

            if nombre_completo == fila[3]:
                id_actual = empleado.get("id_empleado")
                break

        if id_actual is not None:
            for opcion in combo_empleado["values"]:
                if opcion.startswith(f"{id_actual} -"):
                    combo_empleado.set(opcion)
                    break
        else:
            combo_empleado.set("")

        etiqueta_formulario.config(
            text=f"Editar usuario #{fila[0]}"
        )

    def guardar_usuario():
        nombre = entrada_nombre.get().strip()
        contrasena = entrada_contrasena.get()
        rol = combo_rol.get().strip()
        empleado_seleccion = combo_empleado.get().strip()

        if not nombre or not rol:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingresá el nombre de usuario y seleccioná un rol.",
                parent=ventana
            )
            return

        if not usuario_seleccionado["id"] and not contrasena:
            messagebox.showwarning(
                "Contraseña requerida",
                "Ingresá una contraseña para el nuevo usuario.",
                parent=ventana
            )
            return

        id_empleado = None
        if empleado_seleccion:
            try:
                id_empleado = int(
                    empleado_seleccion.split(" - ", 1)[0]
                )
            except ValueError:
                messagebox.showwarning(
                    "Empleado",
                    "Seleccioná un empleado válido.",
                    parent=ventana
                )
                return

        datos = {
            "nombre_usuario": nombre,
            "rol": rol,
            "id_empleado": id_empleado
        }

        # En edición, una contraseña vacía significa no modificarla.
        if contrasena:
            datos["contrasena"] = contrasena

        try:
            if usuario_seleccionado["id"]:
                url = (
                    f"{API_URL}/usuarios/"
                    f"{usuario_seleccionado['id']}"
                )
                respuesta = requests.put(
                    url, json=datos, timeout=5
                )
            else:
                url = f"{API_URL}/usuarios"
                respuesta = requests.post(
                    url, json=datos, timeout=5
                )

            if not respuesta.ok:
                messagebox.showerror(
                    "Error al guardar",
                    f"El servidor respondió {respuesta.status_code}.\n"
                    f"{respuesta.text}",
                    parent=ventana
                )
                return

            messagebox.showinfo(
                "Usuarios",
                "Usuario guardado correctamente.",
                parent=ventana
            )
            limpiar_formulario()
            cargar_usuarios()

        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con la API.\n{error}",
                parent=ventana
            )

    def eliminar_usuario():
        identificador = usuario_seleccionado["id"]

        if not identificador:
            messagebox.showwarning(
                "Seleccionar usuario",
                "Seleccioná un usuario de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Eliminar usuario",
            "¿Estás segura de que querés eliminar este usuario?\n"
            "Esta acción no se puede deshacer.",
            parent=ventana
        )

        if not confirmar:
            return

        try:
            respuesta = requests.delete(
                f"{API_URL}/usuarios/{identificador}",
                timeout=5
            )

            if not respuesta.ok:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el usuario.\n"
                    f"{respuesta.text}",
                    parent=ventana
                )
                return

            messagebox.showinfo(
                "Usuarios",
                "Usuario eliminado correctamente.",
                parent=ventana
            )
            limpiar_formulario()
            cargar_usuarios()

        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                str(error),
                parent=ventana
            )

    def nuevo_usuario():
        tabla.selection_remove(tabla.selection())
        limpiar_formulario()
        entrada_nombre.focus_set()

    # ---------------- ENCABEZADO ----------------

    encabezado = tk.Frame(ventana, bg=COLOR_FONDO)
    encabezado.pack(fill="x", padx=30, pady=(24, 15))

    tk.Label(
        encabezado,
        text="♟  Usuarios del sistema",
        font=("Arial", 22, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    ).pack(side="left")

    tk.Label(
        encabezado,
        text="Gestioná los usuarios y sus permisos",
        font=("Arial", 10),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(side="left", padx=15, pady=(10, 0))

    # ---------------- BOTONES SUPERIORES ----------------

    barra_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    barra_botones.pack(fill="x", padx=30, pady=(0, 12))

    def boton(texto, comando, color=COLOR_PRINCIPAL):
        return tk.Button(
            barra_botones,
            text=texto,
            command=comando,
            bg=color,
            fg=COLOR_BLANCO,
            activebackground=COLOR_SECUNDARIO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            cursor="hand2",
            font=("Arial", 10, "bold"),
            padx=14,
            pady=8
        )

    boton("+ Nuevo usuario", nuevo_usuario).pack(
        side="left", padx=(0, 8)
    )
    boton("✎ Editar", seleccionar_usuario, COLOR_SECUNDARIO).pack(
        side="left", padx=5
    )
    boton("Eliminar", eliminar_usuario, COLOR_ROJO).pack(
        side="left", padx=5
    )

    boton("Actualizar", lambda: (
        consultar_empleados(), cargar_usuarios()
    ), COLOR_SECUNDARIO).pack(side="right")

    # ---------------- BÚSQUEDA Y FILTRO ----------------

    filtros = tk.Frame(ventana, bg=COLOR_FONDO)
    filtros.pack(fill="x", padx=30, pady=(0, 12))

    entrada_busqueda = tk.Entry(
        filtros,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )
    entrada_busqueda.pack(
        side="left", fill="x", expand=True, ipady=9, padx=(0, 12)
    )
    entrada_busqueda.insert(
        0, "Buscar por nombre de usuario, rol o empleado..."
    )

    def al_escribir(event=None):
        if entrada_busqueda.get() == \
                "Buscar por nombre de usuario, rol o empleado...":
            return
        cargar_usuarios()

    def al_entrar(event):
        if entrada_busqueda.get() == \
                "Buscar por nombre de usuario, rol o empleado...":
            entrada_busqueda.delete(0, "end")

    def al_salir(event):
        if not entrada_busqueda.get().strip():
            entrada_busqueda.insert(
                0, "Buscar por nombre de usuario, rol o empleado..."
            )
            cargar_usuarios()

    entrada_busqueda.bind("<KeyRelease>", al_escribir)
    entrada_busqueda.bind("<FocusIn>", al_entrar)
    entrada_busqueda.bind("<FocusOut>", al_salir)

    combo_filtro = ttk.Combobox(
        filtros,
        values=[
            "Todos los roles",
            "Administrador",
            "Empleado"
        ],
        state="readonly",
        width=20,
        font=("Arial", 10)
    )
    combo_filtro.set("Todos los roles")
    combo_filtro.pack(side="right", ipady=7)
    combo_filtro.bind(
        "<<ComboboxSelected>>",
        lambda event: cargar_usuarios()
    )

    # ---------------- TABLA DE USUARIOS ----------------

    marco_tabla = tk.Frame(
        ventana,
        bg=COLOR_BLANCO,
        highlightbackground="#C6DFE9",
        highlightthickness=1
    )
    marco_tabla.pack(
        fill="both", expand=True, padx=30, pady=(0, 15)
    )

    columnas = (
        "id", "nombre_usuario", "rol", "empleado"
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        style="Usuarios.Treeview",
        selectmode="browse"
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre_usuario", text="Nombre de usuario")
    tabla.heading("rol", text="Rol")
    tabla.heading("empleado", text="Empleado asociado")

    tabla.column("id", width=60, anchor="center")
    tabla.column("nombre_usuario", width=190)
    tabla.column("rol", width=170)
    tabla.column("empleado", width=230)

    barra_vertical = ttk.Scrollbar(
        marco_tabla, orient="vertical", command=tabla.yview
    )
    tabla.configure(yscrollcommand=barra_vertical.set)

    tabla.pack(side="left", fill="both", expand=True, padx=4, pady=4)
    barra_vertical.pack(side="right", fill="y")

    tabla.bind("<<TreeviewSelect>>", seleccionar_usuario)

    # ---------------- FORMULARIO ----------------

    marco_form = tk.LabelFrame(
        ventana,
        text="  Información del usuario seleccionado  ",
        font=("Arial", 12, "bold"),
        bg=COLOR_CLARO,
        fg=COLOR_PRINCIPAL,
        padx=15,
        pady=12
    )
    marco_form.pack(fill="x", padx=30, pady=(0, 25))

    marco_form.columnconfigure(1, weight=1)
    marco_form.columnconfigure(3, weight=1)

    etiqueta_formulario = tk.Label(
        marco_form,
        text="Nuevo usuario",
        bg=COLOR_CLARO,
        fg=COLOR_PRINCIPAL,
        font=("Arial", 10, "bold")
    )
    etiqueta_formulario.grid(
        row=0, column=0, columnspan=4, sticky="w", pady=(0, 10)
    )

    tk.Label(
        marco_form, text="Nombre de usuario:",
        bg=COLOR_CLARO, fg=COLOR_TEXTO
    ).grid(row=1, column=0, sticky="w", padx=5, pady=6)

    entrada_nombre = ttk.Entry(marco_form, font=("Arial", 10))
    entrada_nombre.grid(
        row=1, column=1, sticky="ew", padx=5, pady=6
    )

    tk.Label(
        marco_form, text="Contraseña:",
        bg=COLOR_CLARO, fg=COLOR_TEXTO
    ).grid(row=1, column=2, sticky="w", padx=5, pady=6)

    entrada_contrasena = ttk.Entry(
        marco_form, show="*", font=("Arial", 10)
    )
    entrada_contrasena.grid(
        row=1, column=3, sticky="ew", padx=5, pady=6
    )

    tk.Label(
        marco_form, text="Rol:",
        bg=COLOR_CLARO, fg=COLOR_TEXTO
    ).grid(row=2, column=0, sticky="w", padx=5, pady=6)

    combo_rol = ttk.Combobox(
        marco_form,
        values=["Administrador", "Empleado"],
        state="readonly",
        font=("Arial", 10)
    )
    combo_rol.grid(
        row=2, column=1, sticky="ew", padx=5, pady=6
    )

    tk.Label(
        marco_form, text="Empleado asociado:",
        bg=COLOR_CLARO, fg=COLOR_TEXTO
    ).grid(row=2, column=2, sticky="w", padx=5, pady=6)

    combo_empleado = ttk.Combobox(
        marco_form, state="readonly", font=("Arial", 10)
    )
    combo_empleado.grid(
        row=2, column=3, sticky="ew", padx=5, pady=6
    )

    botones_form = tk.Frame(marco_form, bg=COLOR_CLARO)
    botones_form.grid(
        row=3, column=0, columnspan=4,
        sticky="e", padx=5, pady=(12, 0)
    )

    tk.Button(
        botones_form,
        text="Cancelar",
        command=limpiar_formulario,
        bg=COLOR_BLANCO,
        fg=COLOR_TEXTO,
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=8
    ).pack(side="left", padx=5)

    tk.Button(
        botones_form,
        text="Guardar cambios",
        command=guardar_usuario,
        bg=COLOR_PRINCIPAL,
        fg=COLOR_BLANCO,
        activebackground=COLOR_SECUNDARIO,
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold"),
        padx=18,
        pady=8
    ).pack(side="left", padx=5)

    etiqueta_total = tk.Label(
        ventana,
        text="Mostrando usuarios",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Arial", 9)
    )
    etiqueta_total.pack(anchor="w", padx=30, pady=(0, 10))

    # Cargar información inicial
    consultar_empleados()
    cargar_usuarios()

    return ventana
