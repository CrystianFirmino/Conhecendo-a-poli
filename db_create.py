import sqlite3

conection = sqlite3.connect('db1.db')

cursor = conection.cursor()

cursor.execute (

"""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        usuario TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
        )
"""
)

cursor.execute (

    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        nome TEXT NOT NULL, 
        descricao TEXT NOT NULL,
        local TEXT,
        horario 

    )

)

cursor.execute (

    CREATE TABLE IF NOT EXISTS local (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        nome TEXT NOT NULL, 
        bloco TEXT NOT NULL,
        sala TEXT,
        descricao TEXT NOT NULL

    )

)