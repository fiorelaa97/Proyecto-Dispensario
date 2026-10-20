import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# Ajustá estas rutas si en app.js montaste los routers con otros prefijos.
API_MOVIMIENTOS = "http://localhost:3000/api/movimientoinsumos"
API_INSUMOS = "http://localhost:3000/api/insumos"
API_EMPLEADOS = "http://localhost:3000/api/empleados"


def crear_movimientoinsumo(parent):
    COLOR_PRINCIPAL = "#006B6B"
    COLOR_SECUNDARIO = "#008C8C"
    COLOR_FONDO = "#F5FAFC"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_TEXTO = "#234052"
    COLOR_GRIS = "#6B7C85"
    COLOR_BORDE = "#D9E7EC"

    frame = tk.Frame(parent, bg=COLOR_FONDO)
    frame.pack(fill="both", expand=True)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Treeview", background=COLOR_BLANCO,
                    foreground=COLOR_TEXTO, rowheight=36,
                    fieldbackground=COLOR_BLANCO, borderwidth=0,
                    font=("Segoe UI", 9))
    style.configure("Treeview.Heading", background="#EAF5F8",
                    foreground=COLOR_TEXTO, font=("Segoe UI", 9, "bold"),
                    relief="flat")
    style.map("Treeview", background=[("selected", "#D8F0F0")],
              foreground=[("selected", COLOR_TEXTO)])
    style.configure("TCombobox", padding=6, font=("Segoe UI", 9))

    movimientos, insumos, empleados = [], [], []

    # Encabezado
    header = tk.Frame(frame, bg=COLOR_BLANCO, height=80)
    header.pack(fill="x")
    header.pack_propagate(False)
    titulo_frame = tk.Frame(header, bg=COLOR_BLANCO)
    titulo_frame.pack(side="left", padx=25, pady=12)
    tk.Label(titulo_frame, text="Movimientos de insumos",
             bg=COLOR_BLANCO, fg=COLOR_PRINCIPAL,
             font=("Segoe UI", 18, "bold")).pack(anchor="w")
    tk.Label(titulo_frame,
             text="Registrá y consultá las entradas y salidas de insumos.",
             bg=COLOR_BLANCO, fg=COLOR_GRIS,
             font=("Segoe UI", 9)).pack(anchor="w")

    # Controles
    controles = tk.Frame(frame, bg=COLOR_FONDO)
    controles.pack(fill="x", padx=22, pady=(15, 10))
    buscar_var = tk.StringVar()
    buscar_entry = tk.Entry(controles, textvariable=buscar_var,
                            bg=COLOR_BLANCO, fg=COLOR_TEXTO,
                            relief="solid", bd=1, font=("Segoe UI", 9))
    buscar_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
    buscar_entry.insert(0, "")
    filtro_var = tk.StringVar(value="Todos los tipos")
    filtro = ttk.Combobox(controles, textvariable=filtro_var,
                          values=["Todos los tipos", "Entrada", "Salida"],
                          state="readonly", width=18)
    filtro.pack(side="left", padx=(0, 10))
    boton_nuevo = tk.Button(controles, text="+ Nuevo movimiento",
                            bg=COLOR_PRINCIPAL, fg="white",
                            activebackground=COLOR_SECUNDARIO,
                            activeforeground="white", font=("Segoe UI", 9, "bold"),
                            bd=0, padx=16, pady=9, cursor="hand2")
    boton_nuevo.pack(side="right")

    # Tabla
    tabla_frame = tk.Frame(frame, bg=COLOR_BLANCO,
                           highlightbackground=COLOR_BORDE, highlightthickness=1)
    tabla_frame.pack(fill="both", expand=True, padx=22, pady=(0, 10))
    columnas = ("id", "fecha", "tipo", "insumo", "empleado", "cantidad", "motivo", "acciones")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                         selectmode="browse")
    encabezados = {
        "id": "ID", "fecha": "Fecha", "tipo": "Tipo",
        "insumo": "Insumo", "empleado": "Empleado",
        "cantidad": "Cantidad", "motivo": "Motivo", "acciones": "Acciones"
    }
    anchos = {"id": 45, "fecha": 100, "tipo": 80, "insumo": 150,
              "empleado": 165, "cantidad": 80, "motivo": 190, "acciones": 90}
    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, width=anchos[col],
                     anchor="center" if col in ("id", "fecha", "tipo", "cantidad", "acciones") else "w",
                     stretch=col in ("insumo", "empleado", "motivo"))
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    pie = tk.Frame(frame, bg=COLOR_FONDO)
    pie.pack(fill="x", padx=22, pady=(0, 14))
    info_registros = tk.Label(pie, text="Cargando movimientos...",
                              bg=COLOR_FONDO, fg=COLOR_GRIS,
                              font=("Segoe UI", 8))
    info_registros.pack(side="left")

    def pedir_lista(url, nombre):
        try:
            r = requests.get(url, timeout=6)
            r.raise_for_status()
            data = r.json()
            if not isinstance(data, list):
                raise ValueError("La API no devolvió una lista.")
            return data
        except (requests.RequestException, ValueError) as e:
            messagebox.showerror("Error de conexión",
                                 f"No se pudieron cargar {nombre}.\n\n{e}")
            return []

    def id_insumo_de(m):
        return m.get("id_insumo", m.get("insumo_id"))

    def id_empleado_de(m):
        return m.get("id_empleado", m.get("empleado_id"))

    def nombre_insumo(id_value):
        for i in insumos:
            if str(i.get("id_insumo")) == str(id_value):
                return i.get("nombre", f"ID {id_value}")
        return "Sin asignar" if id_value is None else f"ID {id_value}"

    def nombre_empleado(id_value):
        if id_value is None or str(id_value) == "":
            return "Sin asignar"
        for e in empleados:
            if str(e.get("id_empleado")) == str(id_value):
                return f"{e.get('nombre', '')} {e.get('apellido', '')}".strip() or f"ID {id_value}"
        return f"ID {id_value}"

    def mostrar_fecha(value):
        if not value:
            return ""
        value = str(value)
        # MySQL puede devolver YYYY-MM-DD o ISO con hora.
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
        except ValueError:
            return value[:10]

    def filtrados():
        texto = buscar_var.get().strip().lower()
        tipo_filtro = filtro_var.get().lower()
        salida = []
        for m in movimientos:
            tipo = str(m.get("tipo_movimiento", m.get("tipo", "")))
            campos = [
                str(m.get("id_movimiento", "")), tipo,
                nombre_insumo(id_insumo_de(m)), nombre_empleado(id_empleado_de(m)),
                str(m.get("motivo", "")), str(m.get("cantidad", "")),
                mostrar_fecha(m.get("fecha", m.get("fecha_movimiento", "")))
            ]
            if texto and not any(texto in c.lower() for c in campos):
                continue
            if tipo_filtro != "todos los tipos" and tipo.lower() != tipo_filtro:
                continue
            salida.append(m)
        return salida

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)
        lista = filtrados()
        for m in lista:
            fecha = m.get("fecha", m.get("fecha_movimiento", ""))
            tabla.insert("", "end", iid=str(m.get("id_movimiento")),
                         values=(
                             m.get("id_movimiento", ""),
                             mostrar_fecha(fecha),
                             m.get("tipo_movimiento", m.get("tipo", "")),
                             nombre_insumo(id_insumo_de(m)),
                             nombre_empleado(id_empleado_de(m)),
                             m.get("cantidad", 0),
                             m.get("motivo", ""),
                             "Editar / Eliminar"
                         ))
        info_registros.config(text=f"Mostrando {len(lista)} movimiento(s)")

    def cargar_movimientos(mostrar_error=True):
        nonlocal movimientos
        try:
            # El endpoint GET debe ser la raíz de API_MOVIMIENTOS.
            r = requests.get(API_MOVIMIENTOS, timeout=6)
            r.raise_for_status()
            datos = r.json()
            if not isinstance(datos, list):
                raise ValueError("La API no devolvió una lista de movimientos.")
            movimientos = datos
            actualizar_tabla()
        except (requests.RequestException, ValueError) as e:
            info_registros.config(text="No se pudieron cargar los movimientos")
            if mostrar_error:
                messagebox.showerror(
                    "Error al cargar movimientos",
                    f"Verificá que Express esté activo y que la ruta GET sea {API_MOVIMIENTOS}.\n\n{e}"
                )

    def cargar_catalogos():
        nonlocal insumos, empleados
        insumos = pedir_lista(API_INSUMOS, "insumos")
        empleados = pedir_lista(API_EMPLEADOS, "empleados")

    def abrir_formulario(movimiento=None):
        editando = movimiento is not None
        ventana = tk.Toplevel(frame)
        ventana.title("Editar movimiento" if editando else "Nuevo movimiento")
        ventana.geometry("520x680")
        ventana.minsize(500, 650)
        ventana.configure(bg=COLOR_BLANCO)
        ventana.transient(frame.winfo_toplevel())
        ventana.grab_set()

        tk.Label(ventana, text="Editar movimiento" if editando else "Nuevo movimiento",
                 bg=COLOR_BLANCO, fg=COLOR_PRINCIPAL,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=28, pady=(22, 4))
        tk.Label(ventana, text="Completá los datos del movimiento.",
                 bg=COLOR_BLANCO, fg=COLOR_GRIS,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=28, pady=(0, 16))

        form = tk.Frame(ventana, bg=COLOR_BLANCO)
        form.pack(fill="both", expand=True, padx=28)

        def etiqueta(texto):
            tk.Label(form, text=texto, bg=COLOR_BLANCO, fg=COLOR_TEXTO,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 3))

        # Combos con IDs guardados por separado: se muestran nombres, se envían IDs.
        insumos_map = {}
        for i in insumos:
            etiqueta_insumo = f"{i.get('nombre', 'Insumo')} (ID {i.get('id_insumo')})"
            insumos_map[etiqueta_insumo] = i.get("id_insumo")
        etiqueta("Insumo *")
        insumo_var = tk.StringVar()
        combo_insumo = ttk.Combobox(form, textvariable=insumo_var,
                                    values=list(insumos_map), state="readonly")
        combo_insumo.pack(fill="x", ipady=3, pady=(0, 7))

        empleados_map = {"Sin asignar": None}
        for e in empleados:
            nombre = f"{e.get('nombre', '')} {e.get('apellido', '')}".strip()
            empleados_map[f"{nombre or 'Empleado'} (ID {e.get('id_empleado')})"] = e.get("id_empleado")
        etiqueta("Empleado")
        empleado_var = tk.StringVar(value="Sin asignar")
        combo_empleado = ttk.Combobox(form, textvariable=empleado_var,
                                      values=list(empleados_map), state="readonly")
        combo_empleado.pack(fill="x", ipady=3, pady=(0, 7))

        etiqueta("Tipo de movimiento *")
        tipo_var = tk.StringVar()
        combo_tipo = ttk.Combobox(form, textvariable=tipo_var,
                                  values=["Entrada", "Salida"], state="readonly")
        combo_tipo.pack(fill="x", ipady=3, pady=(0, 7))

        etiqueta("Cantidad *")
        cantidad_var = tk.StringVar()
        entrada_cantidad = tk.Entry(form, textvariable=cantidad_var, font=("Segoe UI", 10),
                                    relief="solid", bd=1)
        entrada_cantidad.pack(fill="x", ipady=5, pady=(0, 7))

        etiqueta("Fecha * (AAAA-MM-DD)")
        fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        entrada_fecha = tk.Entry(form, textvariable=fecha_var, font=("Segoe UI", 10),
                                 relief="solid", bd=1)
        entrada_fecha.pack(fill="x", ipady=5, pady=(0, 7))

        etiqueta("Motivo")
        motivo_var = tk.StringVar()
        entrada_motivo = tk.Entry(form, textvariable=motivo_var, font=("Segoe UI", 10),
                                  relief="solid", bd=1)
        entrada_motivo.pack(fill="x", ipady=5, pady=(0, 8))

        if editando:
            target_insumo = id_insumo_de(movimiento)
            for label, ident in insumos_map.items():
                if str(ident) == str(target_insumo):
                    insumo_var.set(label)
                    break
            target_empleado = id_empleado_de(movimiento)
            for label, ident in empleados_map.items():
                if ident is not None and str(ident) == str(target_empleado):
                    empleado_var.set(label)
                    break
            if target_empleado is None:
                empleado_var.set("Sin asignar")
            tipo_var.set(str(movimiento.get("tipo_movimiento", movimiento.get("tipo", ""))).capitalize())
            cantidad_var.set(str(movimiento.get("cantidad", "")))
            fecha_var.set(str(movimiento.get("fecha", movimiento.get("fecha_movimiento", "")))[:10])
            motivo_var.set(str(movimiento.get("motivo", "")))

        def guardar():
            if insumo_var.get() not in insumos_map:
                messagebox.showwarning("Dato obligatorio", "Seleccioná un insumo.", parent=ventana)
                return
            if tipo_var.get() not in ("Entrada", "Salida"):
                messagebox.showwarning("Dato obligatorio", "Seleccioná Entrada o Salida.", parent=ventana)
                return
            try:
                cantidad = int(cantidad_var.get().strip())
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Cantidad incorrecta", "La cantidad debe ser un entero mayor que cero.", parent=ventana)
                return
            try:
                fecha = datetime.strptime(fecha_var.get().strip(), "%Y-%m-%d").date().isoformat()
            except ValueError:
                messagebox.showwarning("Fecha incorrecta", "Ingresá la fecha como AAAA-MM-DD, por ejemplo 2026-10-21.", parent=ventana)
                return
            empleado_label = empleado_var.get()
            if empleado_label not in empleados_map:
                messagebox.showwarning("Empleado incorrecto", "Seleccioná un empleado de la lista.", parent=ventana)
                return

            datos = {
                "id_insumo": insumos_map[insumo_var.get()],
                "id_empleado": empleados_map[empleado_label],
                "tipo_movimiento": tipo_var.get(),
                "cantidad": cantidad,
                "fecha": fecha,
                "motivo": motivo_var.get().strip()
            }
            try:
                if editando:
                    ident = movimiento.get("id_movimiento")
                    respuesta = requests.put(f"{API_MOVIMIENTOS}/{ident}", json=datos, timeout=8)
                else:
                    respuesta = requests.post(API_MOVIMIENTOS, json=datos, timeout=8)
                if respuesta.status_code in (200, 201, 204):
                    messagebox.showinfo("Correcto",
                                        "Movimiento actualizado." if editando else "Movimiento creado.",
                                        parent=ventana)
                    ventana.destroy()
                    cargar_movimientos()
                else:
                    try:
                        cuerpo = respuesta.json()
                        detalle = cuerpo.get("detalle") or cuerpo.get("error") or cuerpo.get("mensaje") or respuesta.text
                    except ValueError:
                        detalle = respuesta.text
                    messagebox.showerror("Error", f"No se pudo guardar el movimiento.\n{detalle}", parent=ventana)
            except requests.RequestException as e:
                messagebox.showerror("Error de conexión", str(e), parent=ventana)

        botones = tk.Frame(ventana, bg=COLOR_BLANCO)
        botones.pack(fill="x", padx=28, pady=(10, 22))
        tk.Button(botones, text="Cancelar", command=ventana.destroy,
                  bg="#EDF3F5", fg=COLOR_TEXTO, bd=0, padx=18, pady=9,
                  font=("Segoe UI", 9), cursor="hand2").pack(side="right", padx=(8, 0))
        tk.Button(botones, text="Guardar cambios" if editando else "Guardar movimiento",
                  command=guardar, bg=COLOR_PRINCIPAL, fg="white",
                  activebackground=COLOR_SECUNDARIO, activeforeground="white",
                  bd=0, padx=18, pady=9, font=("Segoe UI", 9, "bold"),
                  cursor="hand2").pack(side="right")

    def obtener_seleccionado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccioná un movimiento",
                                   "Primero seleccioná un movimiento en la tabla.")
            return None
        ident = seleccion[0]
        for m in movimientos:
            if str(m.get("id_movimiento")) == str(ident):
                return m
        return None

    def editar_seleccionado():
        m = obtener_seleccionado()
        if m:
            abrir_formulario(m)

    def eliminar_seleccionado():
        m = obtener_seleccionado()
        if not m:
            return
        ident = m.get("id_movimiento")
        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Querés eliminar el movimiento #{ident}?"):
            return
        try:
            r = requests.delete(f"{API_MOVIMIENTOS}/{ident}", timeout=8)
            if r.status_code in (200, 204):
                messagebox.showinfo("Correcto", "Movimiento eliminado correctamente.")
                cargar_movimientos()
            else:
                try:
                    cuerpo = r.json()
                    detalle = cuerpo.get("detalle") or cuerpo.get("error") or r.text
                except ValueError:
                    detalle = r.text
                messagebox.showerror("Error", f"No se pudo eliminar el movimiento.\n{detalle}")
        except requests.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))

    # Barra de acciones separada para que editar/eliminar sean visibles y fiables.
    acciones = tk.Frame(frame, bg=COLOR_FONDO)
    acciones.pack(fill="x", padx=22, pady=(0, 8))
    tk.Label(acciones, text="Seleccioná una fila para editar o eliminar.",
             bg=COLOR_FONDO, fg=COLOR_GRIS, font=("Segoe UI", 8)).pack(side="left")
    tk.Button(acciones, text="Editar seleccionado", command=editar_seleccionado,
              bg="#EAF5F8", fg=COLOR_PRINCIPAL, bd=0, padx=13, pady=7,
              font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="right", padx=(8, 0))
    tk.Button(acciones, text="Eliminar seleccionado", command=eliminar_seleccionado,
              bg="#FCE8E6", fg="#B42318", bd=0, padx=13, pady=7,
              font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="right")

    boton_nuevo.config(command=lambda: abrir_formulario())
    buscar_var.trace_add("write", lambda *_: actualizar_tabla())
    filtro.bind("<<ComboboxSelected>>", lambda _e: actualizar_tabla())
    tabla.bind("<Double-1>", lambda _e: editar_seleccionado())

    # Carga inicial: catálogos primero para que la tabla pueda mostrar nombres.
    cargar_catalogos()
    cargar_movimientos()

    return frame
