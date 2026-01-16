# 📊 Sistema de Actualización de Datos CIS – GCBA

Este repositorio contiene un sistema que permite **actualizar y sincronizar datos del CIS – GCBA** de manera automática, tomando información desde **Google Sheets** y cargándola en la **base de datos Supabase**.

El objetivo principal es mantener la base siempre actualizada de forma **simple, segura y sin duplicar información**.

---

## 🚀 Cómo actualizar los datos

Cada vez que sea necesario actualizar la base, seguí estos pasos:

---

### 1️⃣ Abrir la terminal en la carpeta del proyecto

Podés hacerlo de cualquiera de estas formas:

- Click derecho sobre la carpeta del proyecto → **Open in Terminal**
- Abrir **PowerShell** o **Git Bash** y navegar hasta la carpeta del proyecto

---

### 2️⃣ Activar el entorno virtual

Ejecutá el siguiente comando:

powershell
.venv\Scripts\activate
Si el entorno se activó correctamente, vas a ver (.venv) al inicio de la línea de comandos.

3️⃣ Ejecutar la actualización
Corré el script principal:

powershell
Copy code
python main.py
El sistema comenzará a procesar los datos automáticamente y mostrará un resumen al finalizar.

🔍 ¿Qué hace el sistema?
El proceso realiza las siguientes acciones:

Lee los datos desde las hojas configuradas en Google Sheets.

Identifica la última fecha cargada en la base de datos.

Compara los datos nuevos con los ya existentes.

Carga solo los registros nuevos (actualización incremental).

Informa en pantalla cuántos registros fueron agregados.

Esto garantiza que la información no se duplique y que el historial se mantenga consistente.

🛠️ Solución de problemas
❌ Error de conexión
Verificá que tengas conexión a internet.

Revisá que el archivo .env exista y contenga las credenciales correctas.

❌ Error de librerías o módulos faltantes
Si aparece un error indicando que falta algún paquete, ejecutá:

powershell
Copy code
pip install -r requerimientos.txt
✅ Recomendaciones
Ejecutar siempre el script con el entorno virtual activado.

No modificar la estructura de los datos sin validarlo previamente.

Ante cambios importantes en las planillas, revisar el código antes de correr la actualización.

📌 Notas
Este sistema está pensado para ejecutarse de forma manual, pero puede adaptarse fácilmente para una ejecución automática programada.
