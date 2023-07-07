import pyodbc


try:
    conn=pyodbc.connect('DRIVER={ODBC Driver 18 for SQL server};'+
                        'SERVER=181.48.67.101\interfaz;'+
                        'DATABASE=test;'+
                        'UID=sistemasdb;'+
                        'PWD=Grup0IVK2023*;'+
                        'ENCRYPT=No')
    cursor=conn.cursor()
    cursor.execute('select * from pruebaConsultas')
    resultado=cursor.fetchall()
    print(resultado)
except Exception:
    print("no")