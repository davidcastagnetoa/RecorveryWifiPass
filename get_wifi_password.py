import subprocess
import inquirer
import sys
import os


def validate_network_name(answers, current):
    if current.lower() == 'cancel':
        sys.exit("Operación cancelada por el usuario.")
    return True


questions = [
    inquirer.Text('network_profile',
                  message="Enter the profile name of the Wi-Fi network, (write 'cancel' to exit)",
                  validate=validate_network_name),
]

answers = inquirer.prompt(questions)

# El nombre del perfil de red está en answers['network_profile']
network_profile = answers['network_profile']

# Continúa con el procesamiento si se proporciona un nombre de perfil
print(f"Network chosen: {network_profile}")

# Preguntar al usuario por el sistema operativo
questions = [
    inquirer.List('OS',
                  message="What is your OS?",
                  choices=['Linux', 'Windows', "Cancel"],
                  ),
]

answers = inquirer.prompt(questions)


def obtener_contraseña_wifi(network_profile, OS):
    if OS == 'Windows':
        # Windows System
        try:
            results = subprocess.check_output([
                'netsh',
                'wlan',
                'show',
                'profiles',
                network_profile,
                'key=clear'
            ], shell=True).decode('utf-8', errors='backslashreplace')

            print(results)

            if 'Key Content' in results or 'Contenido de la Clave' in results:
                for line in results.split('\n'):
                    if 'Key Content' in line:
                        password = line.split(':')[1].strip()
                        print(
                            f"The {network_profile} network's password is: {password} ")
                        break
            else:
                print(f"Password for {network_profile} not found!")
        except subprocess.CalledProcessError:
            print(f"Could not obtain {network_profile} profile information")

    elif OS == 'Linux':
        # Linux System
        # Verificar si el usuario es root
        if os.geteuid() != 0:
            print("This operation is only allowed for root users.")
            exit(-1)

        try:
            # Ubicación de los archivos de configuración de las redes Wi-Fi
            file_path = f"/etc/NetworkManager/system-connections/{network_profile}"

            password_found = False

            # Leer el archivo de configuración de la red específica
            with open(file_path, 'r') as file:
                for linea in file:
                    if "psk=" in linea:
                        # Devolver la contraseña (línea que contiene "psk=")
                        result = linea.strip().split('=')[1]
                        print(f"Your wifi password is : {result}")
                        password_found = True
                        break

            if not password_found:
                print("Password not found!.")
        except FileNotFoundError:
            print("Network configuration file not found or Network Wifi Incorrect")
        except Exception as e:
            print(f"Error: {e}")

    elif OS == 'Cancel':
        print("Operation canceled by user.")
        sys.exit()  # Salir del programa
    else:
        print("Operating system not supported.")


obtener_contraseña_wifi(network_profile, answers['OS'])
