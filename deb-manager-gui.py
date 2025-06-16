import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class AptInstaller(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, package_name):
        super().__init__()
        self.package_name = package_name

    def run(self):
        try:
            cmd = ['sudo', 'apt', 'install', '-y', self.package_name]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in process.stdout:
                print(line.strip())
                if "Lendo listas" in line:
                    self.progress.emit(10)
                elif "Construindo árvore" in line:
                    self.progress.emit(20)
                elif "Lendo informação" in line:
                    self.progress.emit(30)
                elif "Os NOVOS pacotes" in line or "Instalando" in line:
                    self.progress.emit(60)
                elif "Configurando" in line:
                    self.progress.emit(90)

            process.wait()
            self.progress.emit(100)

            success = process.returncode == 0
            self.finished.emit(success, self.package_name)

        except Exception as e:
            self.finished.emit(False, str(e))


class InstallerWindow(QWidget):
    def __init__(self, package_name):
        super().__init__()
        self.setWindowTitle("Instalador de Pacotes APT")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()

        self.label = QLabel(f"Instalando o pacote: {package_name}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.installer = AptInstaller(package_name)
        self.installer.progress.connect(self.progress_bar.setValue)
        self.installer.finished.connect(self.on_finished)
        self.installer.start()

    def on_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Sucesso", f"O pacote '{message}' foi instalado com sucesso!")
        else:
            QMessageBox.critical(self, "Erro", f"Falha ao instalar: {message}")
        self.close()


def main():
    if len(sys.argv) != 2:
        print("Uso: deb-install-gui-qt6.py <nome-do-pacote>")
        sys.exit(1)

    package = sys.argv[1]
    app = QApplication(sys.argv)
    window = InstallerWindow(package)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
