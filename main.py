import subprocess


def ejecutar_como_root(comando):
    try:
        # Asegúrate de que cada parte del comando sea un elemento separado de la lista
        comando_lista = comando.split()
        subprocess.run(['sudo'] + comando_lista, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except KeyboardInterrupt:
        print("Operation interrupted")


# Ejemplo de uso
comando = 'python get_wifi_password.py'  # Ahora es una cadena simple
ejecutar_como_root(comando)
