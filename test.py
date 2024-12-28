import os
import shutil
import time
import threading
import subprocess

def install_dependencies():
    """Instala las dependencias necesarias para ejecutar Minecraft con Forge."""
    print("Instalando Forge y configurando el servidor de Minecraft...")
    os.system("sudo apt-get update && sudo apt-get install -y openjdk-17-jre wget unzip")

    # Descargar Forge
    forge_installer_url = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.1.0/forge-1.20.1-47.1.0-installer.jar"
    forge_installer_path = "forge-installer.jar"
    if not os.path.exists(forge_installer_path):
        os.system(f"wget {forge_installer_url} -O {forge_installer_path}")

    # Instalar Forge
    os.system(f"java -jar {forge_installer_path} --installServer")

    # Descargar Minecraft server
    server_url = "https://launcher.mojang.com/v1/objects/6f762bfca1ba1e2fd46462de2dc2b313fe570b5d/server.jar"
    server_jar_path = "server.jar"
    if not os.path.exists(server_jar_path):
        os.system(f"wget {server_url} -O {server_jar_path}")

    print("Instalación completada.\n")

def create_world():
    """Crea un nuevo mundo de Minecraft."""
    eula_path = "eula.txt"
    with open(eula_path, "w") as eula_file:
        eula_file.write("eula=true\n")

    print("Creando el mundo por primera vez...")
    subprocess.run(["java", "-Xmx2G", "-Xms1G", "-jar", "forge-1.20.1-47.1.0.jar", "--nogui"])
    print("Mundo creado exitosamente.\n")

def start_world():
    """Inicia el servidor de Minecraft."""
    print("Iniciando el servidor de Minecraft...")
    backup_thread = threading.Thread(target=auto_save)
    backup_thread.daemon = True
    backup_thread.start()

    server_process = subprocess.Popen(["java", "-Xmx2G", "-Xms1G", "-jar", "forge-1.20.1-47.1.0.jar", "--nogui"])

    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("Deteniendo el servidor de Minecraft...")
        server_process.terminate()


def auto_save():
    """Realiza copias de seguridad automáticas del mundo."""
    world_path = "world"
    backup_path = "backups"

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    while True:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"world_backup_{timestamp}"
        backup_folder = os.path.join(backup_path, backup_name)

        print(f"Realizando copia de seguridad en: {backup_folder}")
        try:
            shutil.copytree(world_path, backup_folder)
            print("Copia de seguridad completada.")
        except Exception as e:
            print(f"Error al realizar la copia de seguridad: {e}")

        time.sleep(300)  # Guardado cada 5 minutos

if __name__ == "__main__":
    while True:
        print("\nOpciones:")
        print("1. Instalar dependencias y crear mundo")
        print("2. Iniciar servidor")
        print("3. Salir")

        option = input("Selecciona una opción: ")

        if option == "1":
            install_dependencies()
            create_world()
        elif option == "2":
            start_world()
        elif option == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")
