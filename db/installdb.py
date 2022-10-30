import numpy as np 

from sodapy import Socrata
from connection import conn
import pandas as pd

db, cursor = conn()

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS [dbo].[data](
	[fecha_reporte_web] [varchar](50) NULL,
	[id_de_caso] [int] NOT NULL,
	[fecha_de_notificacion] [varchar](50) NULL,
	[divipola_departamento] [varchar](50) NULL,
	[departamento] [varchar](50) NULL,
	[divopola_municipio] [varchar](50) NULL,
	[municipio] [varchar](50) NULL,
	[edad] [int] NULL,
	[unidad_edad] [int] NULL,
	[sexo] [varchar](50) NULL,
	[tipo_contagio] [varchar](50) NULL,
	[ubicacion] [varchar](50) NULL,
	[estado] [varchar](50) NULL,
	[ISO_pais] [int] NULL,
	[pais] [varchar](50) NULL,
	[recuperado] [varchar](50) NULL,
	[fecha_inicio_sintomas] [varchar](50) NULL,
	[fecha_muerte] [varchar](50) NULL,
	[fecha_diagnostico] [varchar](50) NULL,
	[fecha_recuperacion] [varchar](50) NULL,
	[tipo_recuperacion] [varchar](50) NULL,
	[pertenencia_etnica] [int] NULL,
	[grupo_etnico] [varchar](50) NULL
) ON [PRIMARY]
"""
)

cursor.execute("SELECT COUNT (*) FROM dbo.data")
offset = cursor.fetchone()[0]
print("offset", offset)

client = Socrata("www.datos.gov.co", None)
data = client.get("gt2j-8ykr", limit=100000, offset=offset)
df = pd.DataFrame.from_records(data)

print("Number of rows = ", len(df))

cols = ["fecha_reporte_web", "id_de_caso", "fecha_de_notificaci_n", "departamento", "departamento_nom" "ciudad_municipio", "ciudad_municipio_nom","edad", "unidad_medida","sexo","fuente_tipo_contagio","ubicacion", "estado","pais_viajo_1_cod","pais_viajo_1_nom","recuperado","fecha_inicio_sintomas","fecha_muerte","fecha_diagnostico","fecha_recuperado","tipo_recuperacion","per_etn_","nom_grupo_"]

for col in cols:
    if col not in df:
        df[col] = None

df = df.astype(
    {
        "id_de_caso": int,
        "departamento": int,
        "ciudad_municipio": int, 
        "edad": int, 
        "unidad_medida": int, 
        "pais_viajo_1_cod": int, 
        "per_etn_": int
    }, 
    errors="ignore"
)

df.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
df = df.fillna(0)

insert = "INSERT INTO dbo.data (fecha_reporte_web, id_de_caso, fecha_de_notificacion, divipola_departamento, departamento, divopola_municipio, municipio, edad, unidad_edad, sexo, tipo_contagio, ubicacion, estado, ISO_pais, pais, recuperado, fecha_inicio_sintomas, fecha_muerte, fecha_diagnostico, fecha_recuperacion, tipo_recuperacion, pertenencia_etnica, grupo_etnico) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

for index, row in df.iterrows():
    val = (row.fecha_reporte_web,
            row.id_de_caso,
            row.fecha_de_notificaci_n,
            row.departamento,
            row.departamento_nom,
            row.ciudad_municipio,
            row.ciudad_municipio_nom,
            row.edad,
            row.unidad_medida,
            row.sexo,
            row.fuente_tipo_contagio,
            row.ubicacion,
            row.estado,
            row.pais_viajo_1_cod,
            row.pais_viajo_1_nom,
            row.recuperado,
            row.fecha_inicio_sintomas,
            row.fecha_muerte,
            row.fecha_diagnostico,
            row.fecha_recuperado,
            row.tipo_recuperacion,
            row.per_etn_,
            row.nom_grupo_
    )
    # print(len(val), val)
    # print(row)
    cursor.execute(insert, val)

db.commit()

# No he probado esta linea, puede que no funcione :p
cursor.close()
db.close()