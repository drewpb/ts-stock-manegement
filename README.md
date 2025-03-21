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
    -`pip install -r requirements.txt`
- Run the program:
    -`python app.py`


## How the application works

Main window:
![imagen](https://github.com/user-attachments/assets/b04b1560-6477-4344-bcd9-b39aed4ee086)

Create a new product:
![imagen](https://github.com/user-attachments/assets/714655f6-f527-4538-b472-768074875a5f)

Edit already created product:
![imagen](https://github.com/user-attachments/assets/6a8e3180-fa11-4913-bb49-f0bf7773f0a2)

And delete an existing product by clicking on 'Eliminar' product selected
