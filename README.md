📊 Sistema de Actualización de Datos CIS – GCBA

Este proyecto permite sincronizar automáticamente los datos desde Google Sheets hacia la base de datos Supabase del CIS – GCBA, realizando una carga incremental (solo se suben los registros nuevos).

El sistema está pensado para ejecutarse de forma simple, segura y repetible.

🚀 Guía rápida para actualizar los datos

Cada vez que necesites actualizar la base de datos, seguí estos 3 pasos simples:

1️⃣ Abrir la terminal en el proyecto

Ubicate en la carpeta del proyecto y abrí una terminal:

Click derecho sobre la carpeta → Open in Terminal

O abrí PowerShell / Git Bash y navegá hasta la carpeta del proyecto

2️⃣ Activar el entorno virtual

Ejecutá el siguiente comando:

.venv\Scripts\activate


✔️ Si todo salió bien, vas a ver (.venv) al inicio de la línea de comandos.
Eso indica que el entorno está activo y listo para usar.

3️⃣ Ejecutar la actualización de datos

Corré el script principal con:

python main.py


⏳ El proceso se ejecuta automáticamente y al finalizar mostrará un resumen en pantalla.

🔍 ¿Qué hace el programa?

El script realiza los siguientes pasos de forma automática:

📥 Lee los datos desde las hojas de Google Sheets configuradas.

🕒 Identifica la última fecha cargada en la base de datos.

🔄 Compara los datos nuevos contra los existentes.

⬆️ Carga únicamente los registros nuevos (actualización incremental).

📊 Informa en pantalla cuántos registros fueron agregados.

Esto evita duplicados y asegura que la base siempre esté actualizada.

🛠️ Solución de problemas comunes
❌ Error de conexión

Verificá que tengas conexión a internet.

Revisá que el archivo .env exista y tenga las credenciales correctas.

❌ Error de librerías o módulos faltantes

Si aparece un error indicando que falta algún paquete, ejecutá:

pip install -r requerimientos.txt

✅ Recomendaciones

Ejecutar siempre el script con el entorno virtual activado.

No modificar el orden ni los nombres de las hojas sin validar previamente.

Ante cualquier cambio estructural en los datos, revisar el código antes de correr la actualización.
