import os, sys
from subprocess import call
# # # # # #
import tkinter as tk
from tkinter import ttk
from tkinter import *
# # # # # #
import db
from models import Producto


""" Para recursos:
Para imagenes e iconos:
> https://freepik.com

Para iconos en extension .ico y mas:
> https://icon-icons.com

Para sacar la combinación de colores del GUI:
> https://www.flaticon.com/blog/es/paletas-color-interfaces/
    Donde me quedé con: 
    > https://dribbble.com/shots/18575810-Eco-Recycling-App

Guia bastante completa de los widgets Tkinter, de ahí he sacado la gran mayoría de código
> https://tkdocs.com/shipman/tkinter.pdf
"""

# noinspection PyTypeChecker
class VentanaPrincipal():
    def __init__(self, root):  # Pasamos al constructor la instancia de la ventana principal
        self.v_principal = root
        self.v_principal.title("App Gestor de Productos")
        self.v_principal.resizable(0, 0)  # Desactiva la redimensión de la venta; (1,1) activa ambos ejes

        # Defino los colores en un diccionario
        menu_colors = {"background": "#FEF9E0", "activebackground": "#d9c36b"}
        # '**menu_colors': pasará cada clave-valor del diccionario como si fueran argumentos separados.
        menubar = Menu(self.v_principal, **menu_colors)
        # Menu de Archivos y submenus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nuevo", command=self.desarrolloMenu, **menu_colors)
        filemenu.add_command(label="Abrir", command=self.desarrolloMenu, **menu_colors)
        filemenu.add_separator(background="#FEF9E0")
        filemenu.add_command(label="Salir", command=root.quit, **menu_colors)
        menubar.add_cascade(label="Archivo", menu=filemenu)
        # Menu de Ayuda y submenus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual de Uso", command=self.ayudaMenu, **menu_colors)
        helpmenu.add_command(label="Acerca de...", command=self.infoMenu, **menu_colors) #  Por hacer...
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        # Activo el menu..
        self.v_principal.configure(bg="#586232", menu=menubar)
        # Usar un archivo .png o .xbm como icono para Linux
        self.v_principal.iconphoto(False,
                        PhotoImage(file='recursos/icon.xbm'))  # False para configurar solo el icono principal

        # Creación del contendedor principal (frame)
        frame = LabelFrame(self.v_principal, text=" Registrar Nuevo Producto",
                           font=('Calibri', 12, 'bold'), bg="#FEF9E0", fg="#3b4126", labelanchor=N)
        # Lo ubicamos. 'columnspan' y 'rowspan' es para decir cuanto ocupará.
        frame.grid(row=0, column=0, pady=20, padx=100, columnspan=3, sticky=W+E)

        # Label de Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", bg="#FEF9E0", fg="#3b4126")
        self.etiqueta_nombre.grid(row=1, column=0, pady=3, padx=2)
        # Entry de Nombre
        self.nombre = Entry(frame, justify=CENTER)
        self.nombre.grid(row=1, column=1, pady=3, padx=2, columnspan=4, sticky=W+E)
        self.nombre.focus()  # Como en html, para empezar a escribir directamente

        # Label de Categoria
        self.etiqueta_categoria = Label(frame, text="Categoría: ", bg="#FEF9E0", fg="#3b4126")
        self.etiqueta_categoria.grid(row=2, column=0, pady=3, padx=2)
        # Entry de Categoria
        self.categoria = Entry(frame, justify=CENTER)
        self.categoria.grid(row=2, column=1, pady=3, padx=2, columnspan=4, sticky=W + E)

        # Label de Precio
        self.etiqueta_precio = Label(frame, text="Precio(€/u): ", bg="#FEF9E0", fg='#3b4126')
        self.etiqueta_precio.grid(row=3, column=0, pady=3, padx=2)
        # Entry de Precio
        self.precio = Entry(frame, justify=CENTER, width=12)
        self.precio.grid(row=3, column=1, pady=3, padx=2, columnspan=2)

        # Label de Stock
        self.etiqueta_stock = Label(frame, text="  Stock: ", bg="#FEF9E0", fg='#3b4126')
        self.etiqueta_stock.grid(row=3, column=3, pady=3)
        # Entry de Stock
        self.stock = Entry(frame, justify=CENTER, width=6)
        self.stock.grid(row=3, column=4, pady=3, columnspan=1)

        style_2 = ttk.Style()
        style_2.configure("Custom_2.TButton",
                        font=("Arial", 11),  # Tamaño de la fuente y familia
                        padding=3,  # Tamaño del botón (relleno interno)
                        relief="raised",  # Tipo de borde ('flat', 'raised', 'sunken', 'solid', etc.)
                        borderwidth=1,
                        background='#d9c36b')

        # Boton añadir nuevo producto, el parametro 'command' nos permite escribir la función a ejecutar sin paréntesis
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style="Custom_2.TButton")
        # La ocupación con sticky es obligatorio, con 'columnspan'; opcional
        # Sticky usa de referencia las coordenadas: n, s, e, o, no, ne, so....
        self.boton_aniadir.grid(row=4, column=1, columnspan=3, sticky=W + E, pady=9)  # Sticky de izquierda a derecha

        # Espacio para el mensaje informativo al usuario
        self.mensaje = Label(text='', fg='red', bg="#FEF9E0")
        self.mensaje.grid(row=3, column=0, columnspan=3, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()

        # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11), background='#FEF9E0')
        # Se modifica la fuente de las cabeceras
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'),
                        padding=4,
                        background="#586232",
                        foreground="#FEF9E0",
                        activebackground="#374F1S")
        # Eliminamos los bordes
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        style.configure("Custom.TButton",
                        font=("Arial", 12),  # Tamaño de la fuente y familia
                        padding=4,  # Tamaño del botón (relleno interno)
                        relief="raised",  # Tipo de borde ('flat', 'raised', 'sunken', 'solid', etc.)
                        borderwidth=2,
                        background='#d9c36b')  # Grosor del borde

        # Personalizar el color de fondo y el color de texto de la fila seleccionada
        style.map("mystyle.Treeview",
                  background=[('selected', '#374F1D')],  # Color de fondo cuando está seleccionada
                  foreground=[('selected', '#FEF9E0')])  # Color del texto cuando está seleccionada

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=15, columns=("#1", "#2", "#3"), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=3)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Categoria', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='Precio(€/u)', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('#3', text='Stock', anchor=CENTER)  # Encabezado 3

        # Configuración de columnas
        self.tabla.column('#0', anchor=CENTER)  # Centra los datos en la columna '#0'
        self.tabla.column('#1', anchor=CENTER, width=140)  # Centra los datos en la columna '#1'
        self.tabla.column('#2', anchor=CENTER, width=120)  # Centra los datos en la columna '#2'
        self.tabla.column('#3', anchor=CENTER, width=70)  # Centra los datos en la columna '#3'

        # Botones de Eliminar y Editar
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style="Custom.TButton", width=20)
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E, padx=30, pady=3)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style="Custom.TButton", width=20)
        self.boton_editar.grid(row=5, column=2, sticky=W + E, padx=30, pady=3)

        self.get_productos()

        assert isinstance(root, object)  # Verifica si root es un objeto, en caso contrario lanza un AssertionError

    ################################################
    ### FUNCIONES DEL MENÚ
    def desarrolloMenu(self):
        try:
            VentanaEnDesarrollo(self, self.mensaje)
        except:
            pass

    def ayudaMenu(self):
        try:
            VentanaUso(self, self.mensaje)
        except:
            pass

    def infoMenu(self):
        try:
            VentanaInfo(self, self.mensaje)
        except:
            pass
    ###------------------------------------------###

    def get_productos(self):
        #  Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        productos_db = db.session.query(Producto).all()
        for p in productos_db:
            print(p)
            self.tabla.insert("", 0, text=p.nombre, values=[p.categoria, p.precio, p.stock])

    #################################################################################
    ###   FUNCIONES DE VALIDACIÓN: COMPRUEBA QUE HAYA CONTENIDO EN LOS ENTRY'S
    def validacion_nombre(self):
        # Compruebo que el 'cajón' de texto no esté vacío..
        # Accediendo a su contenido por el método get() que tienen todos los 'entry'
        return self.nombre.get().strip() != ""  # Devuelve True o False

    def validacion_categoria(self):
        # Compruebo que el 'cajón' de texto no esté vacío..
        # Accediendo a su contenido por el método get() que tienen todos los 'entry'
        return self.categoria.get().strip() != ""  # Devuelve True o False

    def validacion_precio(self):
        # Compruebo que el 'cajón' de texto no esté vacío..
        # Pero al ser un numero, primero le hago casting a float
        # Se pone en try..except por si algún error
        try:
            precio = float(self.precio.get())  # Conseguimos el texto y transformamos
            return precio > 0  # Retornamos el valor siempre que sea mayor a cero
        except ValueError:
            return False

    def validacion_stock(self):
        # Compruebo que el 'cajón' de texto no esté vacío..
        # Pero al ser un numero, primero le hago casting a int
        # Se pone en try..except por si algún error
        try:
            stock = int(self.stock.get())  # Conseguimos el texto y transformamos
            return stock >= 0  # Retornamos el valor siempre que sea mayor a cero
        except ValueError:
            return False
    ###---------------------------------------------------------------------------###

    ###############################################################################################
    ###   FUNCIONES ASOCIADAS A BOTONES DE LA VENTANA PRINCIPAL:
    def add_producto(self):
        # Evalúo que haya algo en el nombre
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            # Se podría usar self.mensaje.configure(), pero mas intuitivo usar lo siguiente
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacío'
            return
        # Evalúo que haya algo en el nombre
        if not self.validacion_categoria():
            print("La categria es obligatoria")
            # Se podría usar self.mensaje.configure(), pero mas intuitivo usar lo siguiente
            self.mensaje['text'] = 'La categoría es obligatoria y no puede estar vacío'
            return
        # Evalúo que haya algo en el precio
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número mayor que 0'
            return
            # Evalúo que haya algo en el precio
        if not self.validacion_stock():
            print("El stock es obligatorio")
            self.mensaje['text'] = 'El stock es obligatorio y debe ser un número mayor o igual que 0'
            return
        print(f"Creando producto.. {self.nombre.get()} ; {self.precio.get()} ; {self.categoria.get()}")
        producto = Producto(nombre=self.nombre.get(), categoria=self.categoria.get(),
                      precio=self.precio.get(),
                      stock=self.stock.get())  # Al crear una tarea, por defect no están hecha
        print(producto)
        db.session.add(producto)
        db.session.commit()

        print("Datos guardados")

        # Mostramos mensaje en la App, en el Label ubicado entre el boton y la tabla
        self.mensaje.config(text='Producto {} añadido con éxito'.format(self.nombre.get()), fg='green')

        self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
        self.categoria.delete(0, END)  # Borrar el campo precio del formulario
        self.precio.delete(0, END)  # Borrar el campo precio del formulario
        self.stock.delete(0, END)  # Borrar el campo precio del formulario

        # Debug
        # print(self.nombre.get())
        # print(self.precio.get())

        # Cuando se finalice la inserción de datos volvemos a invocar a este método para actualizar el contenido
        self.get_productos()

    def del_producto(self):
        # Debug
        # print(self.tabla.item(self.tabla.selection()))
        print(self.tabla.item(self.tabla.selection())['text'])
        print(self.tabla.item(self.tabla.selection())['values'])
        # print(self.tabla.item(self.tabla.selection())['values'][0])

        self.mensaje['text'] = ''  # Me aseguro que el Label del mensaje está inicialmente vacío
        # Comprobación de que se seleccione un producto para poder eliminarlo
        try:
            # Asegurar que hay un elemento seleccionado
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''  # Vacio el label de mensaje
        nombre = self.tabla.item(self.tabla.selection())['text']  # Extraigo el nombre
        db.session.query(Producto).filter(Producto.nombre == nombre).delete()
        db.session.commit()

        self.mensaje.config(text='Producto {} eliminado con éxito'.format(nombre), fg='green')
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            categoria = self.tabla.item(self.tabla.selection())['values'][0]
            precio = self.tabla.item(self.tabla.selection())['values'][1]
            stock = self.tabla.item(self.tabla.selection())['values'][2]
            # Creo un objeto de otra clase ventana, le paso mensaje para que se actualice también en la ventana
            VentanaEditarProducto(self, nombre, categoria, precio, stock, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
    ###-----------------------------------------------------------------------------------------###

    def info(self):
        try:
            VentanaInfo(self, self.mensaje)
        except:
            pass

class VentanaEditarProducto():  # Necesita la referencia de la ventana principal 'v_principal'
    def __init__(self, v_principal, nombre, categoria, precio, stock, mensaje):
        self.v_principal = v_principal
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.mensaje = mensaje

        # Instruccion que crea una ventana hija por encima de la principal
        self.v_editar = Toplevel()
        self.v_editar.title("Editar Producto")
        self.v_editar.configure(bg="#FEF9E0")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.v_editar, text="Editar el siguiente Producto",
                              font=('Calibri', 16, 'bold'), bg="#FEF9E0", fg="#3b4126", labelanchor=N)
        frame_ep.grid(row=0, column=0, columnspan=2, pady=30, padx=30)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=1, column=0, pady=3)
        # Con textvariable y haciendo un casting, insertamos la info que queremos
        # Con 'readonly' no se puede modificar
        Entry(frame_ep, textvariable=StringVar(self.v_editar, value=nombre),
              state='readonly', font=('Calibri', 13), justify=CENTER).grid(row=1, column=1, pady=3)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=2, column=0, pady=3)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13), justify=CENTER)
        self.input_nombre_nuevo.grid(row=2, column=1, pady=3)
        self.input_nombre_nuevo.focus()

        # Label y Entry para el Categoria antigua (solo lectura)
        Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=3, column=0, pady=3)
        # Con textvariable y haciendo un casting, insertamos la info que queremos
        # Con 'readonly' no se puede modificar
        Entry(frame_ep, textvariable=StringVar(self.v_editar, value=categoria),
              state='readonly', font=('Calibri', 13), justify=CENTER).grid(row=3, column=1, pady=3)

        # Label y Entry para el Categoria nueva
        Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=4, column=0, pady=3)
        self.input_categ_nuevo = Entry(frame_ep, font=('Calibri', 13), justify=CENTER)
        self.input_categ_nuevo.grid(row=4, column=1, pady=3)

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=5, column=0, pady=3)
        Entry(frame_ep, textvariable=StringVar(self.v_editar, value=precio),
              state='readonly', font=('Calibri', 13), justify=CENTER).grid(row=5, column=1, pady=3)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=6, column=0, pady=3)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13), justify=CENTER)
        self.input_precio_nuevo.grid(row=6, column=1, pady=3)

        # Stock antiguo (solo lectura)
        Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=7, column=0, pady=3)
        Entry(frame_ep, textvariable=StringVar(self.v_editar, value=stock), background="#FEF9E0",
              state='readonly', font=('Calibri', 13), justify=CENTER).grid(row=7, column=1, pady=3)

        # Stock nuevo
        Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13), bg="#FEF9E0").grid(row=8, column=0, pady=3)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13), justify=CENTER)
        self.input_stock_nuevo.grid(row=8, column=1, pady=3)

        style_2 = ttk.Style()
        style_2.configure("Custom_3.TButton",
                          font=("Arial", 12),  # Tamaño de la fuente y familia
                          padding=3,  # Tamaño del botón (relleno interno)
                          relief="raised",  # Tipo de borde ('flat', 'raised', 'sunken', 'solid', etc.)
                          borderwidth=1,
                          background='#d9c36b')

        # Botón Actualizar Producto
        ttk.Button(frame_ep, text="Actualizar Producto",
                   command=self.actualizar, style="Custom_3.TButton").grid(row=9, columnspan=2, sticky=W + E, pady=3)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_categ = self.input_categ_nuevo.get() or self.categoria
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nuevo_stock = self.input_stock_nuevo.get() or self.stock

        if nuevo_nombre and nuevo_precio and nuevo_stock and nuevo_categ:  # Si tienen algo
            print(f"Editando producto.. {nuevo_nombre} ; {nuevo_precio} ; {nuevo_categ}")
            producto = db.session.query(Producto).filter(Producto.nombre == self.nombre).first()
            producto.nombre = nuevo_nombre
            producto.categoria = nuevo_categ
            producto.precio = nuevo_precio
            producto.stock = nuevo_stock

            db.session.commit()
            self.mensaje.config(text=f'El producto {self.nombre} ha sido actualizado con éxito', fg='green')
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

        # Destruimos la ventana editar
        self.v_editar.destroy()
        # Actualizamos ventana principal
        self.v_principal.get_productos()

class VentanaEnDesarrollo():  # Necesita la referencia de la ventana principal 'v_principal'
    def __init__(self, v_principal, mensaje):
        self.v_principal = v_principal
        self.mensaje = mensaje

        # Instruccion que crea una ventana hija por encima de la principal
        self.v_desarrollo = Toplevel()
        self.v_desarrollo.title("..En Desarrollo..")
        self.v_desarrollo.configure(bg="#FEF9E0")

        text = tk.Text(self.v_desarrollo, wrap='word', height=15)
        texto = """
        Actualmente esta opción se encuentra en desarrollo.
           Por favor, disculpe las molestias.
           
        Atentamente, 
         - Alumno de Tokio School -
           """
        text.insert(tk.END, texto)
        text.config(state=tk.DISABLED)  # Deshabilitar la edición del texto
        # Empaqueto el widget Text
        text.pack(padx=6, pady=6, fill=NONE)

        # (Opcional) Añadir un botón para cerrar la ventana
        close_button = tk.Button(self.v_desarrollo, text="Cerrar", command=self.v_desarrollo.destroy, bg="#d9c36b")
        close_button.pack(pady=(0, 10))

class VentanaUso():  # Necesita la referencia de la ventana principal 'v_principal'
    def __init__(self, v_principal, mensaje):
        self.v_principal = v_principal
        self.mensaje = mensaje

        # Localizo el pdf a abrir
        archivo_pdf = "recursos/Funcionamiento GestorProductos de AndresRPB.pdf"
        # name y startfile de la libreria 'os'
        if os.name == 'nt':  # Para Windows
            os.startfile(archivo_pdf)
        elif os.name == 'posix':  # Para Linux/Mac
            # call de la libreria subprocess
            call(['xdg-open', archivo_pdf])

class VentanaInfo():  # Necesita la referencia de la ventana principal 'v_principal'
    def __init__(self, v_principal, mensaje):
        self.v_principal = v_principal
        self.mensaje = mensaje

        # Instruccion que crea una ventana hija por encima de la principal
        self.v_info = Toplevel()
        self.v_info.title("Acerca de ...")
        self.v_info.configure(bg="#FEF9E0")

        text = tk.Text(self.v_info, wrap='word', width=150, height=15)
        texto = f"""
    Acerca de las librerias usadas:
        - SQLAlchemy --> {db.__version__}
        - Tkinter --> {tk.TkVersion}
        
    Acerca del sistema:
        - Plataforma: {sys.platform.upper()}
        - Python Version: {sys.version.rsplit()[0]}
        - Codificación al sistema de archivos: {sys.getfilesystemencoding().upper()}
        - Version info: {sys.version_info}
        - Ruta de la App: {sys.path[0]}
        - Ruta al interprete de Python: {sys.executable}
                   """
        text.insert(tk.END, texto)
        text.config(state=tk.DISABLED)  # Deshabilitar la edición del texto
        # Empaqueto el widget Text
        text.pack(padx=6, pady=6, fill=NONE)

        # (Opcional) Añadir un botón para cerrar la ventana
        close_button = tk.Button(self.v_info, text="Cerrar", command=self.v_info.destroy, bg="#d9c36b")
        close_button.pack(pady=(0, 10))



if __name__ == "__main__":
    # Esto va a ir al fichero db.py, poner en marcha todo lo que tenemos ahi, llegar al
    # fichero models, poner en marcha todo y mapear las clases.
    db.Base.metadata.create_all(db.engine)

    root = Tk()  # Instancia de la ventana principal
    app = VentanaPrincipal(root)  # Enviamos y cedemos el control a la clase
    root.mainloop()  # Mantiene la ventana abierta
