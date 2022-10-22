import pandas as pd
from sqlalchemy import false

def cargar_datos(sheet_name):
    df= pd.read_excel("./data/Matriz_de_adyacencia_data_team.xlsx", sheet_name=sheet_name, index_col=False)


def insert_personas():
    insert = f"INSERT INTO persona (idPersona, nombrePersona) VALUES "
    insertQuery = ""
    dataFrame = cargar_datos('Lista de actores')
    for row in dataFrame.iterrows():
        insertQuery +=(insert + f"{row.idPersona},'{row.nombrePersona}'); ")
    return insertQuery


def insert_relations():
    insert = f"INSERT INTO relaciones (idPersona, nombrePersona) VALUES "
    insertQuery = ""
    dataFrame = cargar_datos('Lista de actores')
    for row in dataFrame.iterrows():
        insertQuery +=(insert + f"{row.idPersona},'{row.nombrePersona}'); ")
    return insertQuery