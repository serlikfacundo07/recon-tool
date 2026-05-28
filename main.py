import subprocess

def ejecutar_comando(comando):
    print(f"\n[*] Ejecutando: {comando}\n")
    try:
        subprocess.run(comando, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error al ejecutar el comando: {e}")
    input("\nPresiona Enter para continuar...")

while True:
    print("\n" + "="*30)
    print("--- MENÚ PRINCIPAL DE RECONOCIMIENTO ---")
    print("="*30)
    print("1. Reconocimiento de Puertos y Tecnologías (Nmap)")
    print("2. Fuzzing de Archivos y Directorios (Gobuster, FFuf, Dirb)")
    print("3. Descubrimiento y Fuzzing de Subdominios (Subfinder, Assetfinder, FFuf, Sublist3r, Amass)")
    print("4. Fuzzing de Parámetros (Curl + FFuf)")
    print("5. Escaneo de Vulnerabilidades Web (WordPress / WPScan)")
    print("x. Salir")
    print("-"*30)
    
    opcion_principal = input("Seleccionar una opción: ").strip().lower()

    if opcion_principal == "x":
        print("Saliendo del programa...")
        break

    elif opcion_principal == "1":
        ip = input("Introduce la IP u objetivo: ").strip()
        if ip:
            comando = f"nmap -A -F -T1 {ip} -v"
            ejecutar_comando(comando)

    elif opcion_principal == "2":
        while True:
            print("\n--- Opciones de Fuzzing de Archivos/Directorios ---")
            print("1. Gobuster (Archivos php, html, txt)")
            print("2. FFuf (Fuzzing con descarte de códigos 403, 301)")
            print("3. Dirb (Escaneo estándar)")
            print("v. Volver al menú principal")
            
            opcion = input("Seleccionar una opción: ").strip().lower()
            if opcion == "v":
                break
            elif opcion == "1":
                target = input("Introduce la URL objetivo (ej. http://172.17.0.2/): ").strip()
                comando = f"gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt -t 100"
                ejecutar_comando(comando)
            elif opcion == "2":
                dominio = input("Introduce el dominio objetivo (ej. dominio.com): ").strip()
                comando = f"ffuf -w /usr/share/wordlists/dirb/common.txt -u {dominio}/FUZZ -fc 403,301 -p 1"
                ejecutar_comando(comando)
            elif opcion == "3":
                dominio = input("Introduce el dominio objetivo (ej. dominio.com): ").strip()
                comando = f"dirb {dominio}"
                ejecutar_comando(comando)

    elif opcion_principal == "3":
        while True:
            print("\n--- Descubrimiento de Subdominios ---")
            print("1. Gobuster Vhost")
            print("2. Subfinder")
            print("3. Assetfinder")
            print("4. FFuf para Subdominios")
            print("5. Sublist3r")
            print("6. Amass (Pasivo)")
            print("v. Volver al menú principal")
            
            opcion = input("Seleccionar una opción: ").strip().lower()
            if opcion == "v":
                break
            elif opcion == "1":
                target = input("Introduce la URL u objetivo: ").strip()
                comando = f"gobuster vhost -u {target} -w /usr/share/wordlists/dirb/common.txt --append-domain -t 2"
                ejecutar_comando(comando)
            elif opcion == "2":
                dominio = input("Introduce el dominio: ").strip()
                comando = f"subfinder -d {dominio} -o archivo_subfinder.txt"
                ejecutar_comando(comando)
            elif opcion == "3":
                dominio = input("Introduce el dominio: ").strip()
                comando = f"assetfinder {dominio} --subs-only > archivos_assetfinder.txt"
                ejecutar_comando(comando)
            elif opcion == "4":
                dominio = input("Introduce el dominio base (ej. dominio.com): ").strip()
                comando = f"ffuf -w /usr/share/wordlists/dirb/common.txt -u FUZZ.{dominio} -fc 403,301 -p 1 > subdominios_ffuf.txt"
                ejecutar_comando(comando)
            elif opcion == "5":
                dominio = input("Introduce el dominio: ").strip()
                comando = f"sublist3r -d {dominio} -v -t 2 -o subdominios_sublist3r.txt"
                ejecutar_comando(comando)
            elif opcion == "6":
                dominio = input("Introduce el dominio: ").strip()
                comando = f"amass enum -passive -d {dominio} > archivo_amass.txt"
                ejecutar_comando(comando)

    elif opcion_principal == "4":
        target = input("Introduce la URL de la ruta objetivo (ej. http://172.17.0.2/ruta): ").strip()
        if target:
            print("[*] Midiendo el tamaño de la respuesta base...")
            resultado = subprocess.run(f"curl -s {target} | wc -c", shell=True, capture_output=True, text=True)
            tamano_pagina = resultado.stdout.strip()
            print(f"[*] Tamaño de página detectado: {tamano_pagina} bytes")
            
            comando = f"ffuf -u '{target}?FUZZ=valorparametro' -w /usr/share/wordlists/dirb/common.txt -fs {tamano_pagina}"
            ejecutar_comando(comando)

    elif opcion_principal == "5":
        url = input("Introduce la URL del sitio WordPress: ").strip()
        if url:
            comando = f"wpscan -url {url} -e ap,at,tt,cb,dbe --plugins-detection aggressive"
            ejecutar_comando(comando)

    else:
        print("[!] Opción no válida. Por favor, selecciona una opción del menú.")