import os
import pyodbc 
from pandas import DataFrame
from dagster import job, op, get_dagster_logger, TripDataFrame, Out, read_csv, script_relative_path, datetime


def crear_tablas():
    return """
    CREATE TABLE IF NOT EXISTS `persona` (
  `idPersona` int NOT NULL,
  `nombrePersona` varchar(45) NOT NULL,
  PRIMARY KEY (`idPersona`),
  UNIQUE KEY `nombrePersona_UNIQUE` (`nombrePersona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `relaciones` (
  `persona1` int NOT NULL,
  `persona2` int NOT NULL,
  PRIMARY KEY (`persona1`,`persona2`),
  KEY `persona2_idx` (`persona2`),
  CONSTRAINT `persona1` FOREIGN KEY (`persona1`) REFERENCES `persona` (`idPersona`),
  CONSTRAINT `persona2` FOREIGN KEY (`persona2`) REFERENCES `persona` (`idPersona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

def get_sql_conn():
    
    cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for MySQL};User ID=root;Password=123456;Server=127.0.0.1;Database=Pipeline server;Port=3306;String Types=Unicode')
    try:
        return cnxn
    except:
        print("Error loading the config file.")

@op(out=Out(TripDataFrame))
def load_trip_dataframe() -> DataFrame:
    return read_csv(
        script_relative_path("./Matriz_de_adyacencia_data_team.xlsx"),
        parse_dates=["start_time", "end_time"],
        date_parser=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"),
        dtype={"color": "category"},
    )

@op
def create_table(context) -> None:
    with get_sql_conn() as conn:
        src_cursor = conn.cursor()
        src_cursor.execute( crear_tablas())
    