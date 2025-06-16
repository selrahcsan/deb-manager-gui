# Instalador APT com Interface Gráfica

Este é um instalador gráfico simples feito em Python usando ~~**Tkinter**~~ PyQT, que permite instalar pacotes `.deb` ou pacotes APT diretamente via nome, com barra de progresso e status.

![screenshot](imgs/02.png) <!-- você pode colocar um link para um print da interface aqui -->

## 🛠️ Funcionalidades

- Interface gráfica amigável usando ~~tkinter~~ `QT5`
- Instala pacotes do repositório APT via nome (`apt install`)
- Exibe progresso simulado e status textual durante a instalação
- Usa ~~sudo~~`pkexec`, portanto, exige privilégios de administrador;
- Mostra mensagens de sucesso ou erro após a instalação

## 📦 Requisitos

- Python 3.x
- Sistema baseado em Debian/Ubuntu
- Dependências Python (geralmente já incluídas):
  - `PyQT` -> `sudo apt install python3-pyqt5`

## ⚙️ Recursos incluídos:

- Instalação automática ao iniciar
- Interface Qt (PyQt5)
- Barra de progresso
- Notificação ao final

🚧 Recurso em processso de implementação:

- Detectar o modo (instalar ou remover), com argumentos --in (instalar) --rm (remover)
- Mostrar uma janela com barra de progresso e status
- Personalizar a mensagem de instação com argumento --tx
- Instalação de 2 pacotes ou mais pacotes

## 🚀 Como usar

### 🔗 Clone o repositório

```bash
git clone https://github.com/selrahcsan/deb-manager-gui.git
cd deb-manager-gui
```

### 🏃‍➡️ Execute o script via terminal, passando o nome do pacote a ser instalado:

Exemplo:
```bash
pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY python3 $PWD/deb-manager-gui.py htop
```
