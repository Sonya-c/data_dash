
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

    cursor.execute("SELECT edad, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY edad " + 
                "ORDER BY edad ") 
    results = cursor.fetchall()
    edad_casos = pd.DataFrame.from_records(results, columns=["edad", "numero_casos"])

    cursor.execute("SELECT sexo, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY sexo " + 
                "ORDER BY sexo ") 
    results = cursor.fetchall()
    sexo_casos = pd.DataFrame.from_records(results, columns=["sexo", "numero_casos"])

    cursor.execute("SELECT estado, count(*) " + 
                "FROM dbo.data " +
                "GROUP BY estado " + 
                "ORDER BY estado ") 
    results = cursor.fetchall()
    estado_casos = pd.DataFrame.from_records(results, columns=["estado", "numero_casos"])

    cursor.close()
    db.close()

    return fecha_casos, edad_casos, sexo_casos, estado_casos