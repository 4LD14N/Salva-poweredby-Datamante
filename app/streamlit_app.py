import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="Salva", page_icon=":money_with_wings:")
app_name = "💸Salva"

def run_script(script_path):
    """
    Ejecuta un script Python y muestra su salida en tiempo real en Streamlit.
    """
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=False,  # Importante para manejar bytes
    )

    output_area = st.empty()  # Espacio vacío para actualizar la salida
    output_buffer = b""  # Almacenará la salida completa en bytes

    # Lee la salida en tiempo real
    for line in iter(process.stdout.readline, b''):
        output_buffer += line
        try:
            decoded_line = output_buffer.decode('utf-8')
        except UnicodeDecodeError:
            decoded_line = output_buffer.decode('latin-1', errors='replace')  # Forzar otra decodificación
        output_area.text(decoded_line)

    process.stdout.close()
    process.wait()
    return process.returncode

def main():
    """
    Función principal de la aplicación Streamlit.
    """
    st.sidebar.title(app_name)
    menu_options = ["Bienvenido", "Script", "Chat bot AI", "Indicadores y Gráficos"]

    select_option = st.sidebar.selectbox("Seleccione una opción:", menu_options, label_visibility="collapsed")

    if select_option == menu_options[0]:
        st.write("¡Bienvenido a Salva!")
        st.write("Esta aplicación te ayudará a gestionar tus finanzas personales.")

    elif select_option == menu_options[1]:
        st.header("Ejecutar Scripts")
        st.write("Esta sección ejecuta los scripts principales que extraen, normalizan y categorizan tus datos financieros.")

        start_button = st.button("Ejecutar Scripts")

        if start_button:
            st.info("Ejecutando los scripts, por favor espera...")

            # Ruta de los scripts (asegúrate de que las rutas sean correctas dentro del contenedor Docker o tu entorno)
            scripts = [
                "./app/main_script.py",
                "./app/normalized.py",
                "./app/categorizer.py"
            ]

            for script in scripts:
                if os.path.exists(script):
                    st.write(f"Ejecutando {script}...")
                    exit_code = run_script(script)

                    if exit_code == 0:
                        st.success(f"¡{os.path.basename(script)} ejecutado exitosamente!")
                    else:
                        st.error(f"Error al ejecutar {os.path.basename(script)}. Deteniendo la ejecución.")
                        break  # Detiene la ejecución si falla un script
                else:
                    st.error(f"No se encontró el script en la ruta: {script}")
                    break

if __name__ == "__main__":
    main()
