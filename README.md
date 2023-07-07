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