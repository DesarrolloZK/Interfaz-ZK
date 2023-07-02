# DOCUMENTACION

## Descripcion

Este programa se encarga de realizar de forma automatica la elaboracion de la interfaz de los distintos restaurantes de la empresa que se sube a sap para que los administradores tengan un control sobre su inventario.

## Archivos importantes

Para este programa se estructuraron algunos archivos para que su funcionamiento sea correcto, dentro de dichos archivos se definen caracteristicas necesarias para que el programa tenga la capacidad de realizar su tarea y son los siguientes:

## configuracion.json:

### Indispensables-> (Si falta algun dato de estos el programa no funcionara).

- consulta: Contiene el QUERY necesario para extraer la informacion escencial de las caps de cada punto.
- impoConsumo: Contiene el valor del impuesto al consumo para que el codigo lo tome como un valor constante y realice los calculos      pertinentes.
- DriverDB: Contiene la informacion del driver que se encarga de la comunicacion con la base de datos, en caso de actualizar o cambiar este driver, buscar documentacion sobre pyodbc que es la libreria de python que utiliza este driver para que el codigo interactue con la DB.
- ServerDB: Contiene el nombre del servidor necesa
    rio para su conexion.
- DATABASE: Contiene el nombre de la base de datos que se consultara.
- UID: Nombre de usuario para autenticarse en la base de datos.
- PWD: Contraseña para autenticarse en la base de datos.
- ENCRYPT: Indica si la conexion es encriptada.

### Opcionales-> (Aqui estara la conexion al FTP para enviar los archivos, si esta informacion falta igualmente se guardaran los archivos en la carpeta raiz del programa dentro de la carpeta "Reportes")

- ipFtp: Direccion ip del ftp donde se enviaran los archivos.
- userFtp: Usuario de autenticacion en el servidor que publica el FTP.
- passwordFtp: Contraseña de autenticacion en el servidor que publica el FTP.
