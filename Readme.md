# TaskManager

Aplicación de consola para organizar tareas. Permite crear tareas manualmente, dividir una tarea compleja en subtareas con ayuda de OpenAI, consultar la lista, marcar tareas como completadas y eliminarlas. Las tareas se guardan localmente en un archivo JSON.

## Requisitos

- Python 3.10 o posterior.
- Una clave de API de OpenAI para iniciar la aplicación, incluida la opción de tareas sin IA. El cliente de OpenAI se crea al cargar el programa.

## Instalación

Clona el repositorio y entra en su directorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd TaskManager
```

Crea y activa un entorno virtual.

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración de OpenAI

Crea un archivo `.env` en la carpeta del proyecto y añade tu clave:

```dotenv
OPENAI_API_KEY=tu_clave_de_api
```

El archivo `.env` está excluido de Git. No publiques ni compartas tu clave de API. La opción de subtareas utiliza el modelo `gpt-5` y requiere conexión a internet y una clave válida.

## Uso

Desde la carpeta del proyecto, ejecuta:

```bash
python main.py
```

El menú ofrece estas opciones:

1. Añadir una tarea manualmente.
2. Desglosar una tarea compleja en subtareas con IA. Las subtareas generadas se añaden individualmente.
3. Listar las tareas y su estado.
4. Marcar una tarea como completada mediante su ID.
5. Eliminar una tarea mediante su ID.
6. Salir.

Los IDs se asignan automáticamente. Al reiniciar la aplicación, se cargan las tareas guardadas y el siguiente ID continúa después del último ID almacenado.

## Persistencia

La aplicación lee y escribe `tasks.json` en la carpeta desde la que se ejecuta. Cada elemento contiene los campos `id`, `description` y `completed`. El archivo de datos está excluido de Git, por lo que las tareas locales no se suben al repositorio.

## Pruebas

Las pruebas usan `unittest` y archivos temporales; no modifican el `tasks.json` del proyecto. Desde la raíz del proyecto, ejecuta:

```bash
python -m unittest discover -s . -p '*test.py'
```

El mismo patrón está configurado en `.vscode/settings.json` para que VS Code descubra las pruebas.

## Estructura del proyecto

```text
TaskManager/
├── ai_service.py          # Integración con OpenAI para generar subtareas
├── main.py                # Menú y ciclo principal de la aplicación
├── task_manager.py        # Modelo Task y operaciones de gestión y persistencia
├── task_manager_test.py   # Pruebas automatizadas con unittest
├── requirements.txt       # Dependencias de Python
├── tasks.json             # Datos locales generados durante el uso
└── .env                   # Clave de API local (no se versiona)
```
