
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime, date, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm


# ==========================================================
# CONFIGURACIÓN DE LA API
# ==========================================================

API_URL = "http://localhost:3000/api/reportes"


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def crear_reportes(parent):

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
    COLOR_CELESTE = "#EAF6F7"
    COLOR_ROJO = "#B94242"
    COLOR_AMARILLO = "#FFF0C2"

    # ------------------------------------------------------
    # LIMPIAR CONTENEDOR
    # ------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=COLOR_FONDO)

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    reporte_actual = tk.StringVar(value="movimientos")
    datos_actuales = []

    columnas_actuales = []

    fecha_hoy = date.today()
    fecha_inicio = fecha_hoy.replace(day=1)

    desde_var = tk.StringVar(
        value=fecha_inicio.strftime("%Y-%m-%d")
    )

    hasta_var = tk.StringVar(
        value=fecha_hoy.strftime("%Y-%m-%d")
    )

    # ======================================================
    # FUNCIONES AUXILIARES
    # ======================================================

    def consultar_api(ruta, parametros=None):

        respuesta = requests.get(
            f"{API_URL}/{ruta}",
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()

        return respuesta.json()

    def formatear_fecha(valor):

        if not valor:
            return "-"

        texto = str(valor)

        try:
            fecha = datetime.fromisoformat(
                texto.replace("Z", "+00:00")
            )

            return fecha.strftime("%d/%m/%Y")

        except (ValueError, TypeError):
            return texto[:10]

    def convertir_fecha(valor):

        if not valor:
            return None

        try:
            return date.fromisoformat(str(valor)[:10])
        except (ValueError, TypeError):
            return None

    def validar_fechas():

        try:
            desde = date.fromisoformat(desde_var.get())
            hasta = date.fromisoformat(hasta_var.get())

            if desde > hasta:
                messagebox.showwarning(
                    "Fechas incorrectas",
                    "La fecha desde no puede ser "
                    "posterior a la fecha hasta."
                )
                return None

            return {
                "desde": desde.isoformat(),
                "hasta": hasta.isoformat()
            }

        except ValueError:

            messagebox.showwarning(
                "Formato incorrecto",
                "Ingresá las fechas con el formato "
                "AAAA-MM-DD."
            )

            return None

    def obtener_alertas(insumos):

        alertas = []

        hoy = date.today()
        limite = hoy + timedelta(days=30)

        for insumo in insumos:

            nombre = insumo.get("nombre", "")
            cantidad = insumo.get("cantidad", 0)
            stock_minimo = insumo.get("stock_minimo", 0)

            try:
                cantidad = float(cantidad or 0)
                stock_minimo = float(stock_minimo or 0)
            except (ValueError, TypeError):
                continue

            fecha = convertir_fecha(
                insumo.get("fecha_vencimiento")
            )

            motivos = []

            if cantidad <= stock_minimo:
                motivos.append("Stock bajo")

            if fecha:
                if fecha < hoy:
                    motivos.append("Vencido")
                elif fecha <= limite:
                    motivos.append("Próximo a vencer")

            if motivos:

                alertas.append({
                    "id_insumo": insumo.get("id_insumo"),
                    "nombre": nombre,
                    "categoria": insumo.get("categoria", ""),
                    "cantidad": cantidad,
                    "stock_minimo": stock_minimo,
                    "fecha_vencimiento": formatear_fecha(
                        insumo.get("fecha_vencimiento")
                    ),
                    "alerta": " / ".join(motivos)
                })

        return alertas

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
        pady=(20, 15)
    )

    tk.Label(
        encabezado,
        text="▥",
        font=("Segoe UI", 27, "bold"),
        fg=COLOR_PRINCIPAL,
        bg=COLOR_FONDO
    ).pack(
        side="left",
        padx=(0, 12)
    )

    titulo_frame = tk.Frame(
        encabezado,
        bg=COLOR_FONDO
    )

    titulo_frame.pack(side="left")

    tk.Label(
        titulo_frame,
        text="Reportes",
        font=("Segoe UI", 19, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    tk.Label(
        titulo_frame,
        text="Generá y consultá los reportes del sistema.",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    ).pack(anchor="w")

    # ======================================================
    # FILTROS DE FECHA
    # ======================================================

    filtros = tk.Frame(
        encabezado,
        bg=COLOR_FONDO
    )

    filtros.pack(side="right")

    tk.Label(
        filtros,
        text="Desde",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    ).grid(row=0, column=0, padx=5, sticky="w")

    tk.Label(
        filtros,
        text="Hasta",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_FONDO
    ).grid(row=0, column=1, padx=5, sticky="w")

    entrada_desde = ttk.Entry(
        filtros,
        textvariable=desde_var,
        width=13
    )

    entrada_desde.grid(
        row=1,
        column=0,
        padx=5,
        ipady=5
    )

    entrada_hasta = ttk.Entry(
        filtros,
        textvariable=hasta_var,
        width=13
    )

    entrada_hasta.grid(
        row=1,
        column=1,
        padx=5,
        ipady=5
    )

    btn_generar = tk.Button(
        filtros,
        text="▣  Generar reporte",
        font=("Segoe UI", 9, "bold"),
        fg=COLOR_BLANCO,
        bg=COLOR_PRINCIPAL,
        activebackground=COLOR_PRINCIPAL_OSCURO,
        activeforeground=COLOR_BLANCO,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=13,
        pady=8
    )

    btn_generar.grid(
        row=1,
        column=2,
        padx=(10, 0)
    )

    # ======================================================
    # TARJETAS DE REPORTES
    # ======================================================

    contenedor_tarjetas = tk.Frame(
        parent,
        bg=COLOR_FONDO
    )

    contenedor_tarjetas.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    for columna in range(4):
        contenedor_tarjetas.grid_columnconfigure(
            columna,
            weight=1,
            uniform="tarjetas"
        )

    def crear_tarjeta(columna, icono, titulo, descripcion, tipo):

        tarjeta = tk.Frame(
            contenedor_tarjetas,
            bg=COLOR_BLANCO,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        interior = tk.Frame(
            tarjeta,
            bg=COLOR_BLANCO
        )

        interior.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=14
        )

        tk.Label(
            interior,
            text=icono,
            font=("Segoe UI", 23, "bold"),
            fg=COLOR_PRINCIPAL,
            bg=COLOR_BLANCO
        ).pack(anchor="w")

        tk.Label(
            interior,
            text=titulo,
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        tk.Label(
            interior,
            text=descripcion,
            font=("Segoe UI", 9),
            fg=COLOR_GRIS,
            bg=COLOR_BLANCO,
            justify="left",
            wraplength=170
        ).pack(
            anchor="w",
            fill="x"
        )

        tk.Button(
            interior,
            text="Ver reporte  →",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_BLANCO,
            bg=COLOR_PRINCIPAL,
            activebackground=COLOR_PRINCIPAL_OSCURO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: cargar_reporte(tipo)
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

    crear_tarjeta(
        0,
        "♟",
        "Empleados",
        "Listado de empleados, altas, bajas y estado actual.",
        "empleados"
    )

    crear_tarjeta(
        1,
        "⬡",
        "Insumos",
        "Stock actual, movimientos y vencimientos.",
        "insumos"
    )

    crear_tarjeta(
        2,
        "⇄",
        "Movimientos de insumos",
        "Entradas y salidas en el período seleccionado.",
        "movimientos"
    )

    crear_tarjeta(
        3,
        "⚠",
        "Alertas",
        "Insumos con stock bajo o próximos a vencer.",
        "alertas"
    )

    # ======================================================
    # CONTENEDOR DE VISTA PREVIA
    # ======================================================

    vista_frame = tk.Frame(
        parent,
        bg=COLOR_BLANCO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )

    vista_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    encabezado_tabla = tk.Frame(
        vista_frame,
        bg=COLOR_BLANCO
    )

    encabezado_tabla.pack(
        fill="x",
        padx=15,
        pady=(12, 8)
    )

    lbl_titulo_tabla = tk.Label(
        encabezado_tabla,
        text="▣  Vista previa del reporte",
        font=("Segoe UI", 11, "bold"),
        fg=COLOR_PRINCIPAL,
        bg=COLOR_BLANCO
    )

    lbl_titulo_tabla.pack(side="left")

    lbl_total = tk.Label(
        encabezado_tabla,
        text="0 registros",
        font=("Segoe UI", 9),
        fg=COLOR_GRIS,
        bg=COLOR_BLANCO
    )

    lbl_total.pack(side="right")

    # ======================================================
    # ESTILOS DE LA TABLA
    # ======================================================

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Reportes.Treeview",
        background=COLOR_BLANCO,
        fieldbackground=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=35,
        font=("Segoe UI", 9),
        borderwidth=0
    )

    estilo.configure(
        "Reportes.Treeview.Heading",
        background=COLOR_CELESTE,
        foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        padding=8
    )

    estilo.map(
        "Reportes.Treeview",
        background=[("selected", COLOR_PRINCIPAL)],
        foreground=[("selected", COLOR_BLANCO)]
    )

    # ======================================================
    # TABLA DE DATOS
    # ======================================================

    tabla_frame = tk.Frame(
        vista_frame,
        bg=COLOR_BLANCO
    )

    tabla_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 12)
    )

    scroll_y = ttk.Scrollbar(
        tabla_frame,
        orient="vertical"
    )

    scroll_x = ttk.Scrollbar(
        tabla_frame,
        orient="horizontal"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        show="headings",
        style="Reportes.Treeview",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    tabla.tag_configure(
        "par",
        background="#F1F8F9"
    )

    tabla.tag_configure(
        "impar",
        background=COLOR_BLANCO
    )

    tabla.tag_configure(
        "alerta",
        background="#FFF0E8",
        foreground=COLOR_ROJO
    )

    # ======================================================
    # CONFIGURACIÓN DE COLUMNAS
    # ======================================================

    def configurar_tabla(tipo):

        configuraciones = {

            "empleados": [
                ("id_empleado", "ID", 60),
                ("nombre", "Nombre", 130),
                ("apellido", "Apellido", 130),
                ("dni", "DNI", 100),
                ("email", "Correo electrónico", 200),
                ("estado", "Estado", 100)
            ],

            "insumos": [
                ("id_insumo", "ID", 60),
                ("nombre", "Insumo", 160),
                ("categoria", "Categoría", 130),
                ("cantidad", "Stock", 80),
                ("stock_minimo", "Stock mínimo", 100),
                ("fecha_vencimiento", "Vencimiento", 120),
                ("estado", "Estado", 110)
            ],

            "movimientos": [
                ("fecha", "Fecha", 100),
                ("tipo_movimiento", "Tipo", 90),
                ("insumo", "Descripción", 170),
                ("categoria", "Categoría", 120),
                ("cantidad", "Cantidad", 90),
                ("empleado", "Empleado", 170),
                ("motivo", "Motivo", 200)
            ],

            "alertas": [
                ("nombre", "Insumo", 160),
                ("categoria", "Categoría", 130),
                ("cantidad", "Stock", 80),
                ("stock_minimo", "Stock mínimo", 100),
                ("fecha_vencimiento", "Vencimiento", 120),
                ("alerta", "Alerta", 180)
            ]
        }

        columnas = configuraciones[tipo]

        tabla["columns"] = [
            columna[0] for columna in columnas
        ]

        for clave, titulo, ancho in columnas:

            tabla.heading(
                clave,
                text=titulo
            )

            tabla.column(
                clave,
                width=ancho,
                minwidth=60,
                anchor="center" if clave in (
                    "id_empleado",
                    "id_insumo",
                    "cantidad",
                    "stock_minimo"
                ) else "w"
            )

        return columnas

    # ======================================================
    # MOSTRAR DATOS EN LA TABLA
    # ======================================================

    def actualizar_tabla(datos, tipo):

        nonlocal datos_actuales, columnas_actuales

        datos_actuales = datos

        for item in tabla.get_children():
            tabla.delete(item)

        columnas_actuales = configurar_tabla(tipo)

        # Mostrar un máximo de 100 registros en pantalla.
        # El PDF incluye todos los datos consultados.

        for indice, registro in enumerate(datos[:100]):

            valores = []

            for clave, titulo, ancho in columnas_actuales:

                valor = registro.get(clave, "")

                if clave in ("fecha", "fecha_vencimiento"):
                    valor = formatear_fecha(valor)

                if valor is None:
                    valor = "-"

                valores.append(valor)

            etiqueta = "par" if indice % 2 == 0 else "impar"

            if tipo == "alertas":
                etiqueta = "alerta"

            tabla.insert(
                "",
                "end",
                values=valores,
                tags=(etiqueta,)
            )

        lbl_total.config(
            text=f"{len(datos)} registros"
        )

    # ======================================================
    # CARGAR REPORTE DESDE LA API
    # ======================================================

    def cargar_reporte(tipo):

        reporte_actual.set(tipo)

        nombres = {
            "empleados": "Reporte de empleados",
            "insumos": "Reporte de insumos",
            "movimientos": "Reporte de movimientos",
            "alertas": "Reporte de alertas"
        }

        lbl_titulo_tabla.config(
            text="▣  " + nombres[tipo]
        )

        try:

            # ----------------------------------------------
            # EMPLEADOS
            # ----------------------------------------------

            if tipo == "empleados":

                respuesta = consultar_api("empleados")

                datos = respuesta.get("empleados", [])

            # ----------------------------------------------
            # INSUMOS
            # ----------------------------------------------

            elif tipo == "insumos":

                respuesta = consultar_api("insumos")

                datos = respuesta.get("insumos", [])

            # ----------------------------------------------
            # MOVIMIENTOS
            # ----------------------------------------------

            elif tipo == "movimientos":

                parametros = validar_fechas()

                if parametros is None:
                    return

                respuesta = consultar_api(
                    "movimientos",
                    parametros
                )

                datos = respuesta.get("movimientos", [])

                # Unificar nombre y apellido del empleado

                for movimiento in datos:

                    nombre = movimiento.get(
                        "nombre_empleado"
                    ) or ""

                    apellido = movimiento.get(
                        "apellido_empleado"
                    ) or ""

                    movimiento["empleado"] = (
                        f"{nombre} {apellido}".strip()
                        or "Sin empleado"
                    )

            # ----------------------------------------------
            # ALERTAS
            # ----------------------------------------------

            elif tipo == "alertas":

                respuesta = consultar_api("insumos")

                insumos = respuesta.get("insumos", [])

                datos = obtener_alertas(insumos)

            else:
                return

            actualizar_tabla(datos, tipo)

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                "Verificá que Node.js esté ejecutándose."
            )

        except requests.exceptions.Timeout:

            messagebox.showerror(
                "Tiempo de espera agotado",
                "El servidor tardó demasiado en responder."
            )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de servidor",
                f"No se pudo consultar el reporte.\n\n{error}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo cargar el reporte.\n\n{error}"
            )

    # ======================================================
    # VISTA PREVIA INICIAL
    # ======================================================

    def cargar_vista_previa():

        try:

            datos = consultar_api("vista-previa")

            movimientos = []

            for registro in datos:

                movimientos.append({
                    "fecha": registro.get("fecha"),
                    "tipo_movimiento": registro.get(
                        "tipo_movimiento", ""
                    ),
                    "insumo": registro.get(
                        "descripcion", ""
                    ),
                    "categoria": "",
                    "cantidad": registro.get("cantidad", 0),
                    "empleado": registro.get(
                        "usuario", "Sin empleado"
                    ),
                    "motivo": ""
                })

            actualizar_tabla(
                movimientos,
                "movimientos"
            )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo cargar la vista previa.\n\n{error}"
            )

    # ======================================================
    # GENERAR REPORTE EN PDF
    # ======================================================

    def generar_pdf():

        tipo = reporte_actual.get()

        # Recargar para exportar los datos actualizados
        cargar_reporte(tipo)

        # Validar que se pudo obtener información
        if not datos_actuales:

            messagebox.showinfo(
                "Sin datos",
                "No hay datos para generar el reporte."
            )
            return

        nombres = {
            "empleados": "Empleados",
            "insumos": "Insumos",
            "movimientos": "Movimientos",
            "alertas": "Alertas"
        }

        nombre_reporte = nombres[tipo]

        nombre_archivo = (
            f"Reporte_{nombre_reporte}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile=nombre_archivo,
            title="Guardar reporte"
        )

        if not ruta:
            return

        try:

            documento = SimpleDocTemplate(
                ruta,
                pagesize=landscape(A4),
                rightMargin=1.3 * cm,
                leftMargin=1.3 * cm,
                topMargin=1.5 * cm,
                bottomMargin=1.5 * cm
            )

            elementos = []

            estilos = getSampleStyleSheet()

            estilo_titulo = estilos["Title"]
            estilo_titulo.textColor = colors.HexColor(
                COLOR_PRINCIPAL
            )

            estilo_titulo.alignment = TA_CENTER

            elementos.append(
                Paragraph(
                    "Cuidar para Vivir - Centro de Salud",
                    estilo_titulo
                )
            )

            elementos.append(Spacer(1, 0.4 * cm))

            elementos.append(
                Paragraph(
                    f"Reporte de {nombre_reporte}",
                    estilos["Heading2"]
                )
            )

            elementos.append(Spacer(1, 0.2 * cm))

            elementos.append(
                Paragraph(
                    "Fecha de generación: "
                    + datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    estilos["Normal"]
                )
            )

            if tipo == "movimientos":

                elementos.append(
                    Paragraph(
                        f"Período: {desde_var.get()} "
                        f"al {hasta_var.get()}",
                        estilos["Normal"]
                    )
                )

            elementos.append(
                Paragraph(
                    f"Total de registros: {len(datos_actuales)}",
                    estilos["Normal"]
                )
            )

            elementos.append(Spacer(1, 0.5 * cm))

            # Columnas
            encabezados = [
                titulo
                for clave, titulo, ancho in columnas_actuales
            ]

            datos_tabla = [encabezados]

            for registro in datos_actuales:

                fila = []

                for clave, titulo, ancho in columnas_actuales:

                    valor = registro.get(clave, "")

                    if clave in ("fecha", "fecha_vencimiento"):
                        valor = formatear_fecha(valor)

                    if valor is None:
                        valor = "-"

                    fila.append(str(valor))

                datos_tabla.append(fila)

            # Estilo para texto dentro de las celdas
            estilo_celda = estilos["BodyText"].clone(
                "CeldaReporte"
            )

            estilo_celda.fontSize = 7
            estilo_celda.leading = 9

            datos_formateados = []

            for fila in datos_tabla:

                datos_formateados.append([
                    Paragraph(
                        str(valor)
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"),
                        estilo_celda
                    )
                    for valor in fila
                ])

            ancho_disponible = landscape(A4)[0] - 2.6 * cm

            suma_anchos = sum(
                ancho for _, _, ancho in columnas_actuales
            )

            anchos_pdf = [
                ancho_disponible * ancho / suma_anchos
                for _, _, ancho in columnas_actuales
            ]

            tabla_pdf = Table(
                datos_formateados,
                colWidths=anchos_pdf,
                repeatRows=1,
                hAlign="LEFT"
            )

            tabla_pdf.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(COLOR_PRINCIPAL)
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#F1F8F9")
                        ]
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.3,
                        colors.HexColor(COLOR_BORDE)
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ])
            )

            elementos.append(tabla_pdf)

            documento.build(elementos)

            messagebox.showinfo(
                "Reporte generado",
                "El reporte PDF se generó correctamente.\n\n"
                f"Ubicación:\n{ruta}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error al generar PDF",
                f"No se pudo generar el archivo.\n\n{error}"
            )

    # ======================================================
    # ASIGNAR EVENTOS
    # ======================================================

    btn_generar.config(
        command=generar_pdf
    )

    entrada_desde.bind(
        "<Return>",
        lambda event: cargar_reporte("movimientos")
    )

    entrada_hasta.bind(
        "<Return>",
        lambda event: cargar_reporte("movimientos")
    )

    # ======================================================
    # CARGA INICIAL
    # ======================================================

    cargar_vista_previa()
