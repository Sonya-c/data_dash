
from db.connection import conn
import pandas as pd 

def queries():

    db, cursor = conn()

    cursor.execute("SELECT fecha_reporte_web, sexo, estado, municipio, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY fecha_reporte_web, sexo, estado, municipio " + 
                "ORDER BY fecha_reporte_web ") 
    results = cursor.fetchall()
    fecha_casos = pd.DataFrame.from_records(results, columns=["fecha", "sexo", "estado", "municipio", "numero_casos"])

    cursor.execute("SELECT edad, municipio, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY edad, municipio " + 
                "ORDER BY edad ") 
    results = cursor.fetchall()
    edad_casos = pd.DataFrame.from_records(results, columns=["edad", "municipio", "numero_casos"])

    cursor.execute("SELECT sexo, municipio, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY sexo, municipio " + 
                "ORDER BY sexo ") 
    results = cursor.fetchall()
    sexo_casos = pd.DataFrame.from_records(results, columns=["sexo", "municipio", "numero_casos"])

    cursor.execute("SELECT estado, municipio, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY estado, municipio " + 
                "ORDER BY estado ") 
    results = cursor.fetchall()
    estado_casos = pd.DataFrame.from_records(results, columns=["estado", "municipio", "numero_casos"])

    cursor.close()
    db.close()

    return fecha_casos, edad_casos, sexo_casos, estado_casos