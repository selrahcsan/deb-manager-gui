#!/usr/bin/env python3

import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class AptWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, packages, mode):
        super().__init__()
        self.packages = packages
        self.mode = mode

    def run(self):
        try:
            total_packages = len(self.packages)
            progress_block = 100 // total_packages
            overall_progress = 0

            for i, package_name in enumerate(self.packages):
                if self.mode == "install":
                    cmd = ['sudo', 'apt', 'install', '-y', package_name]
                    action_word = "Instalando"
                else:
                    cmd = ['sudo', 'apt', 'remove', '-y', package_name]
                    action_word = "Removendo"

                self.progress.emit(overall_progress)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

                for line in process.stdout:
                    print(line.strip())
                    current_progress = overall_progress
                    step_progress = 0
                    if "Lendo listas" in line:
                        step_progress = 10
                    elif "Construindo árvore" in line:
                        step_progress = 20
                    elif "Lendo informação" in line:
                        step_progress = 30
                    elif action_word in line:
                        step_progress = 60
                    elif "Configurando" in line or "Removido" in line:
                        step_progress = 90

                    current_progress = overall_progress + int(step_progress * progress_block / 100)
                    self.progress.emit(min(current_progress, 100))

                process.wait()
                if process.returncode != 0:
                    self.finished.emit(False, f"Erro ao processar o pacote: {package_name}")
                    return

                overall_progress += progress_block

            self.progress.emit(100)
            self.finished.emit(True, ", ".join(self.packages))

        except Exception as e:
            self.finished.emit(False, str(e))


class ManagerWindow(QWidget):
    def __init__(self, packages, mode, custom_text=None):
        super().__init__()
        self.mode = mode
        action = "Instalando" if mode == "install" else "Removendo"
        self.setWindowTitle(f"{action} Pacotes APT")
        self.setFixedSize(450, 180)

        layout = QVBoxLayout()

        if custom_text:
            label_text = custom_text
        else:
            pkg_text = ", ".join(packages)
            label_text = f"{action} os pacotes: {pkg_text}"

        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.worker = AptWorker(packages, mode)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, message):
        if success:
            action = "instalados" if self.mode == "install" else "removidos"
            QMessageBox.information(self, "Sucesso", f"Os pacotes '{message}' foram {action} com sucesso!")
        else:
            QMessageBox.critical(self, "Erro", f"Falha ao processar os pacotes: {message}")
        self.close()


def main():
    if len(sys.argv) < 3:
        print("Uso: deb-manager-gui.py --in|--rm <pacote1> [pacote2 ...] [--tx mensagem personalizada]")
        sys.exit(1)

    # Detectar --tx e mensagem personalizada
    if '--tx' in sys.argv:
        tx_index = sys.argv.index('--tx')
        custom_text = " ".join(sys.argv[tx_index + 1:])
        args = sys.argv[1:tx_index]  # argumentos antes do --tx
    else:
        custom_text = None
        args = sys.argv[1:]

    if len(args) < 2:
        print("Uso: deb-manager-gui.py --in|--rm <pacote1> [pacote2 ...] [--tx mensagem personalizada]")
        sys.exit(1)

    option = args[0]
    packages = args[1:]

    if option == "--in":
        mode = "install"
    elif option == "--rm":
        mode = "remove"
    else:
        print("Opção inválida! Use --in para instalar ou --rm para remover.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = ManagerWindow(packages, mode, custom_text)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

