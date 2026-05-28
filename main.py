import subprocess

def ejecutar_comando(comando):
    print(f"\n[*] Ejecutando: {comando}\n")
    try:
        subprocess.run(comando, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error al ejecutar el comando: {e}")
    input("\nPresiona Enter para continuar...")

def seleccionar_modo():
    while True:
        print("\n" + "=" * 40)
        print("    ¿QUÉ TIPO DE RECONOCIMIENTO DESEAS REALIZAR?")
        print("=" * 40)
        print("")
        print("  [1]  AGRESIVO")
        print("      → Máxima velocidad, muchos hilos")
        print("      → Sin delays entre requests")
        print("      → Ideal para entornos controlados / CTF")
        print("")
        print("  [2]  SILENCIOSO")
        print("      → Pocos hilos, escaneo lento")
        print("      → Delays entre requests para evadir detección")
        print("      → Ideal para entornos reales / pentesting")
        print("")
        print("-" * 40)

        modo = input("Selecciona el modo (1/2): ").strip()

        if modo == "1":
            print("\n[✔] Modo AGRESIVO seleccionado.\n")
            return "agresivo"
        elif modo == "2":
            print("\n[✔] Modo SILENCIOSO seleccionado.\n")
            return "silencioso"
        else:
            print("[!] Opción no válida. Elige 1 o 2.")

def obtener_perfil(modo):
    if modo == "agresivo":
        return {
            "nmap_timing": "-T4",
            "nmap_flags": "-A -p- --open",
            "gobuster_threads": 100,
            "gobuster_delay": "",
            "ffuf_threads": 50,
            "ffuf_delay": "",
            "gobuster_vhost_threads": 50,
            "sublist3r_threads": 10,
            "ffuf_rate": "",
            "wpscan_throttle": "",
            "dirb_delay": "",
        }
    else:
        return {
            "nmap_timing": "-T1",
            "nmap_flags": "-sS -sV -F --open",
            "gobuster_threads": 5,
            "gobuster_delay": "--delay 500ms",
            "ffuf_threads": 2,
            "ffuf_delay": "-p 2",
            "gobuster_vhost_threads": 2,
            "sublist3r_threads": 2,
            "ffuf_rate": "-rate 10",
            "wpscan_throttle": "--throttle 2000",
            "dirb_delay": "-z 1000",
        }

def mostrar_modo_actual(modo):
    icono = "🔥 AGRESIVO" if modo == "agresivo" else "🤫 SILENCIOSO"
    return f"[Modo: {icono}]"

modo = seleccionar_modo()
perfil = obtener_perfil(modo)

while True:
    etiqueta = mostrar_modo_actual(modo)

    print("\n" + "=" * 50)
    print(f"--- MENÚ PRINCIPAL DE RECONOCIMIENTO {etiqueta} ---")
    print("=" * 50)
    print("1. Reconocimiento de Puertos y Tecnologías (Nmap)")
    print("2. Fuzzing de Archivos y Directorios (Gobuster, FFuf, Dirb)")
    print("3. Descubrimiento y Fuzzing de Subdominios (Subfinder, Assetfinder, FFuf, Sublist3r, Amass)")
    print("4. Fuzzing de Parámetros (Curl + FFuf)")
    print("5. Escaneo de Vulnerabilidades Web (WordPress / WPScan)")
    print("m. Cambiar modo de reconocimiento")
    print("x. Salir")
    print("-" * 50)

    opcion_principal = input("Seleccionar una opción: ").strip().lower()

    if opcion_principal == "x":
        print("Saliendo del programa...")
        break

    elif opcion_principal == "m":
        modo = seleccionar_modo()
        perfil = obtener_perfil(modo)

    elif opcion_principal == "1":
        ip = input("Introduce la IP u objetivo: ").strip()
        if ip:
            comando = f"nmap {perfil['nmap_flags']} {perfil['nmap_timing']} {ip} -v"
            ejecutar_comando(comando)

    elif opcion_principal == "2":
        while True:
            print(f"\n--- Opciones de Fuzzing de Archivos/Directorios {etiqueta} ---")
            print("1. Gobuster (Archivos php, html, txt)")
            print("2. FFuf (Fuzzing con descarte de códigos 403, 301)")
            print("3. Dirb (Escaneo estándar)")
            print("v. Volver al menú principal")

            opcion = input("Seleccionar una opción: ").strip().lower()
            if opcion == "v":
                break
            elif opcion == "1":
                target = input("Introduce la URL objetivo (ej. http://172.17.0.2/): ").strip()
                delay_flag = f" {perfil['gobuster_delay']}" if perfil['gobuster_delay'] else ""
                comando = f"gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt -t {perfil['gobuster_threads']}{delay_flag}"
                ejecutar_comando(comando)
            elif opcion == "2":
                dominio = input("Introduce el dominio objetivo (ej. dominio.com): ").strip()
                delay_flag = f" {perfil['ffuf_delay']}" if perfil['ffuf_delay'] else ""
                rate_flag = f" {perfil['ffuf_rate']}" if perfil['ffuf_rate'] else ""
                comando = f"ffuf -w /usr/share/wordlists/dirb/common.txt -u {dominio}/FUZZ -fc 403,301 -t {perfil['ffuf_threads']}{delay_flag}{rate_flag}"
                ejecutar_comando(comando)
            elif opcion == "3":
                dominio = input("Introduce el dominio objetivo (ej. dominio.com): ").strip()
                delay_flag = f" {perfil['dirb_delay']}" if perfil['dirb_delay'] else ""
                comando = f"dirb {dominio}{delay_flag}"
                ejecutar_comando(comando)

    elif opcion_principal == "3":
        while True:
            print(f"\n--- Descubrimiento de Subdominios {etiqueta} ---")
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
                delay_flag = f" {perfil['gobuster_delay']}" if perfil['gobuster_delay'] else ""
                comando = f"gobuster vhost -u {target} -w /usr/share/wordlists/dirb/common.txt --append-domain -t {perfil['gobuster_vhost_threads']}{delay_flag}"
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
                delay_flag = f" {perfil['ffuf_delay']}" if perfil['ffuf_delay'] else ""
                rate_flag = f" {perfil['ffuf_rate']}" if perfil['ffuf_rate'] else ""
                comando = f"ffuf -w /usr/share/wordlists/dirb/common.txt -u FUZZ.{dominio} -fc 403,301 -t {perfil['ffuf_threads']}{delay_flag}{rate_flag} > subdominios_ffuf.txt"
                ejecutar_comando(comando)
            elif opcion == "5":
                dominio = input("Introduce el dominio: ").strip()
                comando = f"sublist3r -d {dominio} -v -t {perfil['sublist3r_threads']} -o subdominios_sublist3r.txt"
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

            delay_flag = f" {perfil['ffuf_delay']}" if perfil['ffuf_delay'] else ""
            rate_flag = f" {perfil['ffuf_rate']}" if perfil['ffuf_rate'] else ""
            comando = f"ffuf -u '{target}?FUZZ=valorparametro' -w /usr/share/wordlists/dirb/common.txt -fs {tamano_pagina} -t {perfil['ffuf_threads']}{delay_flag}{rate_flag}"
            ejecutar_comando(comando)

    elif opcion_principal == "5":
        url = input("Introduce la URL del sitio WordPress: ").strip()
        if url:
            throttle_flag = f" {perfil['wpscan_throttle']}" if perfil['wpscan_throttle'] else ""
            comando = f"wpscan -url {url} -e ap,at,tt,cb,dbe --plugins-detection aggressive{throttle_flag}"
            ejecutar_comando(comando)

    else:
        print("[!] Opción no válida. Por favor, selecciona una opción del menú.")