# pipeline.py

import os
import subprocess

# Función para ejecutar comandos en la terminal
def run_command(command):
    print(f"Ejecutando comando: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error al ejecutar el comando: {command}")
        print(result.stderr)
    else:
        print(result.stdout)

# Ejecutar pruebas unitarias utilizando unittest
def run_unit_tests():
    try:
        print("Ejecutando tests unitarios...")
        run_command("cd Chess1.0.1/Chess && python -m unittest discover -s tests -p 'utest_*.py'")
        print("Tests unitarios completados.")
    except Exception as e:
        print(f"Error al ejecutar tests unitarios: {e}")

# Tareas del pipeline
def main():
    try:
        # Ejecutar pruebas unitarias antes de cualquier cosa
        run_unit_tests()
        
        # Verificar el estilo de código con flake8
        run_command("cd Chess1.0.1/Chess && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics")
        run_command("cd Chess1.0.1/Chess && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics")

        # Ejecutar el juego de ajedrez
        run_command("cd Chess1.0.1/Chess && python main.py")

    except Exception as e:
        print(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    main()
