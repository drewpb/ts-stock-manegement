# Stock Management Desktop app

![imagen](https://github.com/user-attachments/assets/ca78b32c-9cb8-42be-a77f-add683ad539d)

## Desktop app with database project

In this project I have created a desktop application with connection to a database. This application will aim to be a stock manager, that is, a software that will allow the user the following basic actions:
    - Create products
    - Edit a product
    - Delete products
In addition to other improvements proposed by the teacher to change and improve the graphical interface:
    - Add a Category field for the product
    - Add a Stock field for the product
    - Implementing SQLAlchemy on SQLite to be able to change database without touching the code
    - Adding a Menu as a new graphical widget provided by Tkinter
      
The technology stack to be used in this project is the following:
    - Python 3. As base programming language.
    - Jetbrains Pycharm Community. IDE chosen for the development of the project.
    - Tkinter. Module integrated in Python that provides graphical interfaces.
    - SQLite. Fast and powerful SQL database for moderate size installations.
    - SQLAlchemy. It is a Python module, which acts as an ORM (Object-Relational Mapping) application that will allow working with the database (SQLite in this case) in a simpler way, working with programming objects and not with the tables, syntax and particularities of the chosen database. In short, it is an application that will facilitate the management and communication with the database from Python.

Preparing the environment
    - Have PyCharm or similar installed
    - Clone the repository
    - Open PyCharm
    - Open the project 
    - Open the PyCharm terminal
    - Install the dependencies:
        ◦ `pip install -r requirements.txt`
    - Run the program:
        ◦ `python app.py`


Funcionamiento

    • Al momento de ejecutar el programa, se abrirá la app con el siguiente contenido:
	
    • En este punto podemos observar tres partes principales:
        ◦ El menú, de cara a un mayor desarrollo, pero con ciertas funcionalidades:




	Por un lado, ‘Archivos’, donde con un mayor desarrollo se le incluiría opciones para crear uno nuevo, abrir uno ya existente, etc. Además de la posibilidad de salir.

	Por otro lado, ‘Ayuda’ donde está al alcance este mismo PDF a modo de “Manual de Usuario” y un clásico “Acerca de…” con información de las librerías usadas, información del sistemas y más.
	

        ◦ La cabecera, donde podemos crear un nuevo producto:

	Al crear un producto debemos rellenar todos los campos obligatoriamente. En caso contrario saldrá un mensaje en rojo a modo de aviso. Los nombres de Categoría por lo general es conveniente que se ajuste a una sola palabra y como máximo dos.
    • ‘Nombre’ y ‘Categoría’ son cadenas de texto.
    • ‘Precio’ es un número en decimal. Para añadir decimales basta con separar la parte entera de la decimal con un punto ‘.’
    • ‘Stock’ es un número entero.
	Cuando estén todos los campos con la información que queremos, solo queda darle al botón de ‘Guardar Producto’. Esto se conectará con la base de datos y la actualizará con la nueva tarea:

        ◦ El cuerpo, donde visualizamos los productos que ya tenemos creadas y que podemos seleccionar uno a uno si queremos editar o eliminar algún producto:
          

	Las acciones permitidas son:
    • Borrar producto de la base de datos →  Al pulsar el botón, se conectará con la base de datos para eliminar el registro del producto. Y no volverá a visualizarse.
      
    • Editar tarea → Al pulsar en el botón, se abrirá una nueva ventana:
 		
	En esta ventana, modificaremos los campos que queramos. Teniendo que cuenta y respetando el tipo de dato explicado anteriormente en cada parámetro del producto. En caso de no escribir nada, se quedará como estaba y solo se modificará aquel campo donde se haya escrito algo. Una vez terminado, hacer click  en “Actualizar Producto”. Automáticamente se cerrará esa ventana y volverá a la principal con los productos actualizados.
