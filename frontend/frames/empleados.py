import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/empleados"


# ============================================================
# COLORES
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
# CLASE PRINCIPAL
# ============================================================

class EmpleadosFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=COLOR_FONDO
        )

        self.empleados = []
        self.empleado_seleccionado = None

        self.crear_interfaz()
        self.cargar_empleados()


    # ========================================================
    # INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        # ----------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------------

        contenido = tk.Frame(
            self,
            bg=COLOR_FONDO
        )
        contenido.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=18
        )


        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        encabezado = tk.Frame(
            contenido,
            bg=COLOR_FONDO
        )
        encabezado.pack(
            fill="x",
            pady=(0, 15)
        )

        icono = tk.Label(
            encabezado,
            text="●",
            font=("Arial", 28, "bold"),
            fg=COLOR_PRINCIPAL,
            bg=COLOR_FONDO
        )
        icono.pack(
            side="left",
            padx=(0, 12)
        )

        textos = tk.Frame(
            encabezado,
            bg=COLOR_FONDO
        )
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


        # ----------------------------------------------------
        # BOTONES SUPERIORES
        # ----------------------------------------------------

        botones = tk.Frame(
            encabezado,
            bg=COLOR_FONDO
        )
        botones.pack(side="right")

        self.boton_nuevo = self.crear_boton(
            botones,
            "＋  Nuevo empleado",
            self.nuevo_empleado,
            COLOR_PRINCIPAL
        )
        self.boton_nuevo.pack(
            side="left",
            padx=4
        )

        self.boton_editar = self.crear_boton(
            botones,
            "✎  Editar",
            self.editar_empleado,
            "#117B7C"
        )
        self.boton_editar.pack(
            side="left",
            padx=4
        )

        self.boton_eliminar = self.crear_boton(
            botones,
            "▣  Eliminar",
            self.eliminar_empleado,
            "#117B7C"
        )
        self.boton_eliminar.pack(
            side="left",
            padx=4
        )


        # ----------------------------------------------------
        # BARRA DE BÚSQUEDA
        # ----------------------------------------------------

        barra = tk.Frame(
            contenido,
            bg=COLOR_FONDO
        )
        barra.pack(
            fill="x",
            pady=(0, 10)
        )

        buscar_frame = tk.Frame(
            barra,
            bg=COLOR_BLANCO,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        buscar_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            buscar_frame,
            text="⌕",
            font=("Arial", 19),
            fg=COLOR_GRIS,
            bg=COLOR_BLANCO
        ).pack(
            side="left",
            padx=(10, 4)
        )

        self.buscar_var = tk.StringVar()

        self.buscar_entry = tk.Entry(
            buscar_frame,
            textvariable=self.buscar_var,
            font=("Arial", 10),
            relief="flat",
            bd=0,
            fg=COLOR_TEXTO
        )
        self.buscar_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.buscar_entry.bind(
            "<KeyRelease>",
            lambda event: self.filtrar_empleados()
        )


        # ----------------------------------------------------
        # FILTRO ESTADO
        # ----------------------------------------------------

        self.estado_filtro = ttk.Combobox(
            barra,
            values=[
                "Todos los estados",
                "Activo",
                "Inactivo"
            ],
            state="readonly",
            font=("Arial", 10),
            width=20
        )
        self.estado_filtro.set("Todos los estados")
        self.estado_filtro.pack(
            side="right",
            padx=(10, 0),
            ipady=5
        )

        self.estado_filtro.bind(
            "<<ComboboxSelected>>",
            lambda event: self.filtrar_empleados()
        )


        # ----------------------------------------------------
        # TABLA
        # ----------------------------------------------------

        tabla_frame = tk.Frame(
            contenido,
            bg=COLOR_BLANCO,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        tabla_frame.pack(
            fill="both",
            expand=True
        )


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

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        encabezados = {
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

            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )


        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_empleado
        )

        self.tabla.bind(
            "<Double-1>",
            lambda event: self.editar_empleado()
        )


        # ----------------------------------------------------
        # ESTILOS TABLA
        # ----------------------------------------------------

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=COLOR_BLANCO,
            foreground=COLOR_TEXTO,
            rowheight=38,
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
            background=[
                ("selected", "#D9F0F0")
            ],
            foreground=[
                ("selected", COLOR_TEXTO)
            ]
        )


        # ----------------------------------------------------
        # INFORMACIÓN INFERIOR DE TABLA
        # ----------------------------------------------------

        self.info_label = tk.Label(
            contenido,
            text="Mostrando 0 empleados",
            font=("Arial", 9),
            fg=COLOR_GRIS,
            bg=COLOR_FONDO
        )

        self.info_label.pack(
            anchor="w",
            pady=(7, 5)
        )


        # ----------------------------------------------------
        # FORMULARIO
        # ----------------------------------------------------

        self.crear_formulario(contenido)


    # ========================================================
    # FORMULARIO
    # ========================================================

    def crear_formulario(self, parent):

        self.formulario = tk.Frame(
            parent,
            bg=COLOR_BLANCO,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )

        self.formulario.pack(
            fill="x",
            pady=(5, 0)
        )


        # Título

        titulo = tk.Frame(
            self.formulario,
            bg="#EAF4F5"
        )
        titulo.pack(
            fill="x"
        )

        tk.Label(
            titulo,
            text="＋",
            font=("Arial", 18, "bold"),
            fg=COLOR_PRINCIPAL,
            bg="#EAF4F5"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.titulo_formulario = tk.Label(
            titulo,
            text="Nuevo / Editar empleado",
            font=("Arial", 11, "bold"),
            fg=COLOR_TEXTO,
            bg="#EAF4F5"
        )

        self.titulo_formulario.pack(
            side="left",
            pady=9
        )


        # Contenedor

        campos = tk.Frame(
            self.formulario,
            bg=COLOR_BLANCO
        )
        campos.pack(
            fill="x",
            padx=14,
            pady=12
        )


        # Variables

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Activo")


        # Fila 1

        self.crear_campo(
            campos,
            "Nombre *",
            self.nombre_var,
            0,
            0
        )

        self.crear_campo(
            campos,
            "Apellido *",
            self.apellido_var,
            0,
            1
        )

        self.crear_campo(
            campos,
            "DNI *",
            self.dni_var,
            0,
            2
        )

        self.crear_campo(
            campos,
            "Teléfono *",
            self.telefono_var,
            0,
            3
        )


        # Fila 2

        tk.Label(
            campos,
            text="Cargo *",
            font=("Arial", 9, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(12, 4)
        )

        self.cargo_combo = ttk.Combobox(
            campos,
            textvariable=self.cargo_var,
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

        self.cargo_combo.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 12)
        )


        self.crear_campo(
            campos,
            "Fecha de ingreso *",
            self.fecha_var,
            2,
            1
        )


        tk.Label(
            campos,
            text="Estado *",
            font=("Arial", 9, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).grid(
            row=2,
            column=2,
            sticky="w",
            pady=(12, 4)
        )

        self.estado_combo = ttk.Combobox(
            campos,
            textvariable=self.estado_var,
            values=[
                "Activo",
                "Inactivo"
            ],
            state="readonly"
        )

        self.estado_combo.grid(
            row=3,
            column=2,
            sticky="ew",
            padx=(0, 12)
        )


        for i in range(4):
            campos.columnconfigure(
                i,
                weight=1
            )


        # Botones

        botones = tk.Frame(
            campos,
            bg=COLOR_BLANCO
        )

        botones.grid(
            row=3,
            column=3,
            sticky="e"
        )

        tk.Button(
            botones,
            text="✕  Cancelar",
            command=self.limpiar_formulario,
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            font=("Arial", 9),
            relief="solid",
            bd=1,
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            botones,
            text="▣  Guardar",
            command=self.guardar_empleado,
            bg=COLOR_PRINCIPAL,
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left"
        )


    # ========================================================
    # CREAR CAMPO
    # ========================================================

    def crear_campo(
        self,
        parent,
        titulo,
        variable,
        fila,
        columna
    ):

        tk.Label(
            parent,
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

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 9),
            relief="solid",
            bd=1,
            fg=COLOR_TEXTO
        )

        entry.grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=(0, 12),
            ipady=6
        )


    # ========================================================
    # BOTÓN
    # ========================================================

    def crear_boton(
        self,
        parent,
        texto,
        comando,
        color
    ):

        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            bd=0,
            padx=13,
            pady=9,
            cursor="hand2"
        )


    # ========================================================
    # OBTENER EMPLEADOS
    # ========================================================

    def cargar_empleados(self):

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code == 200:

                self.empleados = respuesta.json()

                self.mostrar_empleados(
                    self.empleados
                )

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener los empleados."
                )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el backend.\n\n"
                "Verificá que el servidor Express esté ejecutándose."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )


    # ========================================================
    # MOSTRAR EMPLEADOS
    # ========================================================

    def mostrar_empleados(self, empleados):

        for item in self.tabla.get_children():
            self.tabla.delete(item)


        for empleado in empleados:

            fecha = empleado.get(
                "fecha_ingreso",
                ""
            )

            # MySQL puede devolver la fecha como string
            if isinstance(fecha, str):
                try:
                    fecha_obj = datetime.fromisoformat(
                        fecha[:10]
                    )
                    fecha = fecha_obj.strftime(
                        "%d/%m/%Y"
                    )
                except:
                    pass


            self.tabla.insert(
                "",
                "end",
                iid=str(empleado["id"]),
                values=(
                    empleado.get("id", ""),
                    empleado.get("nombre", ""),
                    empleado.get("apellido", ""),
                    empleado.get("dni", ""),
                    empleado.get("telefono", ""),
                    empleado.get("cargo", ""),
                    fecha,
                    empleado.get("estado", "")
                )
            )


        self.info_label.config(
            text=f"Mostrando {len(empleados)} empleados"
        )


    # ========================================================
    # BUSCAR / FILTRAR
    # ========================================================

    def filtrar_empleados(self):

        texto = self.buscar_var.get().lower().strip()

        estado = self.estado_filtro.get()

        filtrados = []

        for empleado in self.empleados:

            contenido = " ".join([
                str(empleado.get("nombre", "")),
                str(empleado.get("apellido", "")),
                str(empleado.get("dni", "")),
                str(empleado.get("cargo", ""))
            ]).lower()

            coincide_texto = (
                texto == ""
                or texto in contenido
            )

            coincide_estado = (
                estado == "Todos los estados"
                or empleado.get("estado") == estado
            )

            if coincide_texto and coincide_estado:
                filtrados.append(empleado)


        self.mostrar_empleados(filtrados)


    # ========================================================
    # SELECCIONAR EMPLEADO
    # ========================================================

    def seleccionar_empleado(self, event=None):

        seleccion = self.tabla.selection()

        if not seleccion:
            self.empleado_seleccionado = None
            return

        id_empleado = int(
            seleccion[0]
        )

        for empleado in self.empleados:

            if empleado["id"] == id_empleado:

                self.empleado_seleccionado = empleado

                break


    # ========================================================
    # NUEVO EMPLEADO
    # ========================================================

    def nuevo_empleado(self):

        self.empleado_seleccionado = None

        self.limpiar_formulario()

        self.nombre_var.set("")
        self.apellido_var.set("")
        self.dni_var.set("")
        self.telefono_var.set("")
        self.cargo_var.set("")
        self.fecha_var.set("")
        self.estado_var.set("Activo")

        self.titulo_formulario.config(
            text="Nuevo empleado"
        )


    # ========================================================
    # EDITAR EMPLEADO
    # ========================================================

    def editar_empleado(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Editar",
                "Seleccioná un empleado de la tabla."
            )

            return


        id_empleado = int(
            seleccion[0]
        )

        empleado = next(
            (
                e for e in self.empleados
                if e["id"] == id_empleado
            ),
            None
        )

        if not empleado:
            return


        self.empleado_seleccionado = empleado


        self.nombre_var.set(
            empleado.get("nombre", "")
        )

        self.apellido_var.set(
            empleado.get("apellido", "")
        )

        self.dni_var.set(
            empleado.get("dni", "")
        )

        self.telefono_var.set(
            empleado.get("telefono", "")
        )

        self.cargo_var.set(
            empleado.get("cargo", "")
        )

        fecha = empleado.get(
            "fecha_ingreso",
            ""
        )

        if isinstance(fecha, str):

            try:

                fecha = datetime.fromisoformat(
                    fecha[:10]
                ).strftime(
                    "%d/%m/%Y"
                )

            except:
                pass


        self.fecha_var.set(fecha)

        self.estado_var.set(
            empleado.get(
                "estado",
                "Activo"
            )
        )

        self.titulo_formulario.config(
            text="Editar empleado"
        )


    # ========================================================
    # GUARDAR
    # ========================================================

    def guardar_empleado(self):

        nombre = self.nombre_var.get().strip()
        apellido = self.apellido_var.get().strip()
        dni = self.dni_var.get().strip()
        telefono = self.telefono_var.get().strip()
        cargo = self.cargo_var.get().strip()
        fecha = self.fecha_var.get().strip()
        estado = self.estado_var.get().strip()


        # Validaciones

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "Ingresá el nombre."
            )
            return

        if not apellido:
            messagebox.showwarning(
                "Validación",
                "Ingresá el apellido."
            )
            return

        if not dni:
            messagebox.showwarning(
                "Validación",
                "Ingresá el DNI."
            )
            return

        if not telefono:
            messagebox.showwarning(
                "Validación",
                "Ingresá el teléfono."
            )
            return

        if not cargo:
            messagebox.showwarning(
                "Validación",
                "Seleccioná un cargo."
            )
            return

        if not fecha:
            messagebox.showwarning(
                "Validación",
                "Ingresá la fecha de ingreso."
            )
            return


        # ----------------------------------------------------
        # Convertir DD/MM/YYYY -> YYYY-MM-DD
        # ----------------------------------------------------

        try:

            fecha_obj = datetime.strptime(
                fecha,
                "%d/%m/%Y"
            )

            fecha_mysql = fecha_obj.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Fecha incorrecta",
                "La fecha debe tener el formato:\n"
                "DD/MM/AAAA"
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


        try:

            # ------------------------------------------------
            # CREAR
            # ------------------------------------------------

            if self.empleado_seleccionado is None:

                respuesta = requests.post(
                    API_URL,
                    json=datos,
                    timeout=5
                )


                if respuesta.status_code == 201:

                    messagebox.showinfo(
                        "Éxito",
                        "Empleado agregado correctamente."
                    )

                    self.limpiar_formulario()
                    self.cargar_empleados()

                else:

                    self.mostrar_error_api(
                        respuesta
                    )


            # ------------------------------------------------
            # EDITAR
            # ------------------------------------------------

            else:

                id_empleado = (
                    self.empleado_seleccionado["id"]
                )

                respuesta = requests.put(
                    f"{API_URL}/{id_empleado}",
                    json=datos,
                    timeout=5
                )


                if respuesta.status_code == 200:

                    messagebox.showinfo(
                        "Éxito",
                        "Empleado actualizado correctamente."
                    )

                    self.limpiar_formulario()
                    self.cargar_empleados()

                else:

                    self.mostrar_error_api(
                        respuesta
                    )


        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )


    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar_empleado(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Eliminar",
                "Seleccioná un empleado."
            )

            return


        id_empleado = int(
            seleccion[0]
        )


        empleado = next(
            (
                e for e in self.empleados
                if e["id"] == id_empleado
            ),
            None
        )


        if not empleado:
            return


        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que querés eliminar a\n"
            f"{empleado.get('nombre', '')} "
            f"{empleado.get('apellido', '')}?"
        )


        if not confirmar:
            return


        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_empleado}",
                timeout=5
            )


            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Empleado eliminado correctamente."
                )

                self.limpiar_formulario()
                self.cargar_empleados()

            else:

                self.mostrar_error_api(
                    respuesta
                )


        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )


    # ========================================================
    # LIMPIAR FORMULARIO
    # ========================================================

    def limpiar_formulario(self):

        self.empleado_seleccionado = None

        self.nombre_var.set("")
        self.apellido_var.set("")
        self.dni_var.set("")
        self.telefono_var.set("")
        self.cargo_var.set("")
        self.fecha_var.set("")
        self.estado_var.set("Activo")

        self.titulo_formulario.config(
            text="Nuevo / Editar empleado"
        )

        for item in self.tabla.selection():
            self.tabla.selection_remove(item)


    # ========================================================
    # ERROR API
    # ========================================================

    def mostrar_error_api(self, respuesta):

        try:

            datos = respuesta.json()

            mensaje = datos.get(
                "error",
                "Ocurrió un error"
            )

            detalle = datos.get(
                "detalle",
                ""
            )

            if detalle:
                mensaje += f"\n\n{detalle}"

        except:

            mensaje = (
                f"Error HTTP {respuesta.status_code}"
            )


        messagebox.showerror(
            "Error",
            mensaje
        )


# ============================================================
# FUNCIÓN PARA USAR DESDE TU PROYECTO
# ============================================================

def crear_empleado(parent):

    frame = EmpleadosFrame(parent)

    return frame


# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Cuidar para Vivir - Registro de Empleados"
    )

    root.geometry(
        "1250x800"
    )

    root.minsize(
        1050,
        700
    )

    empleados = EmpleadosFrame(root)

    empleados.pack(
        fill="both",
        expand=True
    )

    root.mainloop()
