# Salva: Gestión de Datos Basada en Correos Electrónicos

## Descripción

**Salva** es una solución innovadora y automatizada, impulsada por inteligencia artificial (Llama3.2) y técnicas de minería de datos, que transforma la gestión de las finanzas personales. Desarrollada en Python, extrae y procesa información financiera proveniente de notificaciones por correo electrónico del Banco de Crédito del Perú (BCP) y de transacciones bancarias, categorizando automáticamente los gastos con una precisión aproximada del 70%. Esta herramienta permite analizar en detalle los patrones de consumo, ayudando a los usuarios a comprender mejor sus hábitos financieros y a tomar decisiones informadas para optimizar sus recursos económicos. Es ideal para quienes buscan claridad y precisión en el seguimiento de sus movimientos bancarios.

## Características

- **Extracción Automática:** Recupera datos financieros de notificaciones bancarias enviadas por correo electrónico del BCP.
- **Gestión de Fechas:** Almacena y recupera la fecha de la última ejecución para evitar procesar correos repetidos.
- **Limpieza y Preprocesamiento:** Elimina datos duplicados y organiza la información de forma eficiente.
- **Normalización de Datos:** Procesa y consolida los datos en archivos Excel.
- **Categorías Automatizadas:** Utiliza inteligencia artificial (Llama3.2) para categorizar transacciones mediante reglas predefinidas y análisis contextual.
- **Visualización:** Ofrece una vista del proceso a través de una interfaz en Streamlit (en construcción).
- **Dashboard en Excel:** Se ha desarrollado un dashboard interactivo en Excel con indicadores y gráficos. (Solicítalo para obtener acceso).

## Estructura del Proyecto

### Scripts Principales

1. **main_script.py:**
- Autentica la cuenta de Gmail.
- Recupera correos electrónicos.
- Extrae datos financieros y almacena la fecha de la última ejecución.
- Guarda los datos procesados en archivos Excel.

2. **gmail_auth.py:**
- Gestiona la autenticación con la API de Gmail.

3. **get_mail.py:**
- Obtiene y procesa el contenido de los correos electrónicos.

4. **patterns_bcp.py, patterns_yape.py, patterns_yape_1.py:**
- Contienen patrones específicos para extraer datos de notificaciones del BCP y de transacciones realizadas mediante Yape.

5. **normalized.py:**
- Normaliza los datos extraídos, consolidándolos en un formato adecuado para su análisis.

6. **categorizer.py:**
- Categoriza los datos normalizados utilizando reglas predefinidas y, en casos específicos, invoca el modelo Llama3.2 para identificar el servicio o producto asociado a cada transacción.

### Interfaz de Usuario

- **streamlit_app.py (Streamlit):**
   Permite ejecutar los scripts directamente desde una interfaz web. Actualmente, se encuentra en desarrollo y optimización.

- **Dashboard en Excel:**
   Además de los archivos generados, se ha creado un dashboard interactivo en Excel para visualizar indicadores y gráficos. (Solicítalo para obtener acceso).

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/4LD14N/Salva.v1.git
   cd salva.v1
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Coloca tu archivo de credenciales en app/credentials.json. Puedes seguir la documentación oficial de Google API para obtenerlas.

## Importante

La sesión se maneja mediante un archivo pickle (app/token.pickle). Cuando la sesión expire, elimina dicho archivo y vuelve a ejecutar la solución para renovar la autenticación.

### **Modo de Uso**

1. **Ejecuta el script principal:**
   ```bash
   python .\app\main_script.py
   ```
- Concede los permisos necesarios para la lectura de correos en Gmail.

2. **Normaliza los datos extraídos:**
   ```bash
   python ./app/normalized.py
   ```

3. **Verifica que la aplicación Ollama esté activa:**
Asegúrate de que la aplicación Ollama, con el modelo Llama3.2, se encuentre en ejecución.

4. **Categoriza los datos normalizados:**
   ```bash
   python ./app/categorizer.py
   ```

5. **Revisa los archivos generados:**
Los resultados se guardan en la ruta ./app/data.

## Limitaciones Actuales

- Actualmente, el sistema extrae información únicamente de notificaciones de dos remitentes del BCP.
- La visualización de los datos extraídos, normalizados y categorizados se realiza únicamente en Excel.
- Es posible que algunas transacciones no se extraigan correctamente o generen errores, ya que solo se han mapeado transacciones generales. Si requieres mapear una transacción específica, contáctame para ofrecerte un servicio personalizado.
- Si deseas acceder a gráficos interactivos, comunícate conmigo para compartir el dashboard desarrollado en formato XLSX.
- La integración con otros bancos (como Interbank, BBVA, entre otros) se considerará si el proyecto tiene buena acogida.

## Requisitos

- Python 3.12 o superior
- Aplicación Ollama con el modelo Llama3.2
- Google API configurada para la autenticación de Gmail

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contribuciones

Se aceptan contribuciones para mejorar el proyecto. Por favor, envía un pull request con tus propuestas.

## Contacto

Para consultas, problemas o colaboración, contáctame a través de: datamante.company.pe@gmail.com

---

**Nota:** 
Asegúrate de que las rutas de los scripts estén correctamente configuradas en tu entorno de desarrollo. Si necesitas ayuda, asesoría o un desarrollo personalizado, no dudes en contactarme.

---
