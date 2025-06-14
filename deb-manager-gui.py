import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import sys
import os

def install_package(pkg_name, progress_var, status_label):
    try:
        status_label.config(text=f"Instalando '{pkg_name}'...")
        # Simula progresso enquanto instala
        process = subprocess.Popen(
            ['sudo', 'apt', 'install', '-y', pkg_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in process.stdout:
            print(line.strip())
            if "Lendo listas de pacotes" in line or "Preparando" in line:
                progress_var.set(20)
            elif "Instalando" in line:
                progress_var.set(60)
            elif "Configurando" in line:
                progress_var.set(90)
        
        process.wait()
        progress_var.set(100)

        if process.returncode == 0:
            messagebox.showinfo("Sucesso", f"O pacote '{pkg_name}' foi instalado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao instalar o pacote '{pkg_name}'.")
    except Exception as e:
        messagebox.showerror("Erro inesperado", str(e))


def run_gui(pkg_name):
    root = tk.Tk()
    root.title("Instalador APT")

    tk.Label(root, text=f"Instalando o pacote: {pkg_name}", font=("Arial", 14)).pack(pady=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress_bar.pack(pady=10)

    status_label = tk.Label(root, text="Iniciando...", font=("Arial", 10))
    status_label.pack(pady=5)

    def start_install():
        threading.Thread(target=install_package, args=(pkg_name, progress_var, status_label), daemon=True).start()

    install_button = ttk.Button(root, text="Instalar", command=start_install)
    install_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: deb-install-gui <nome-do-pacote>")
        sys.exit(1)

    package = sys.argv[1]
    run_gui(package)
