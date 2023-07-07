# Aplicación de Eventos

Esta es una aplicación de agenda de eventos que permite a los usuarios registrar, editar y eliminar eventos. Los eventos pueden ser presenciales o virtuales y se ordenan en función de su fecha, mostrando los eventos más recientes en la parte superior.

## Características

- Registro de usuarios: Los usuarios pueden crear una cuenta proporcionando su nombre, correo electrónico y contraseña.
- Inicio de sesión: Los usuarios pueden iniciar sesión en la aplicación utilizando sus credenciales.
- Creación de eventos: Los usuarios autenticados pueden crear eventos ingresando el nombre del evento, la fecha, el lugar y la modalidad (presencial o virtual).
- Edición y eliminación de eventos: Los usuarios pueden editar y eliminar los eventos que han creado.
- Listado de eventos: Se muestra una lista de eventos ordenados por fecha, con los eventos más recientes en la parte superior.

## Tecnologías utilizadas

- Flask: Framework web utilizado para el desarrollo de la aplicación.
- SQLAlchemy: Biblioteca ORM utilizada para interactuar con la base de datos relacional.
- MySQL: Sistema de gestión de bases de datos relacional utilizado para almacenar los datos de la aplicación.
- JWT: Biblioteca utilizada para la autenticación de usuarios.
- Bootstrap: Framework CSS utilizado para el diseño de la aplicación.
- bcrypt: Biblioteca utilizada para el cifrado de contraseñas.

# Para desarrolladores

## Instalación
1. Cree el ambiente virtual
```bash
python3 -m venv .venv
```

2. Iniciar ambiente virtual


* En windows
```bash 
.venv\Scripts\Activate.ps1
```
* En linux
```bash 
source .env/bin/activate
```

3. Intalar dependencias
```bash 
pip  install -r requirements.txt
```
4. Crear archivo `.env` de variable de ambiente en la raiz del proyecto y agregar el siguiente contenido
```MD 
HOST=<your db host>
PORT=<your db port>
USER=<your db user>
PASSWORD=<yor db password>
DB=<your database name>
```

### URL
```
    http://127.0.0.1:5000