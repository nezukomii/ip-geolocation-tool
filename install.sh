#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' 

echo -e "${CYAN}"
echo "██╗██████╗     ██╗      ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗ "
echo "██║██╔══██╗    ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗"
echo "██║██████╔╝    ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝"
echo "██║██╔═══╝     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗"
echo "██║██║         ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║"
echo "╚═╝╚═╝         ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${GREEN}                    📍 IP Geolocation Tool v1.0 📍${NC}"
echo -e "${YELLOW}                        Installer Script${NC}"
echo

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python3 encontrado: $python_version"
        return 0
    elif command -v python &> /dev/null; then
        python_version=$(python --version 2>&1 | cut -d' ' -f2)
        print_success "Python encontrado: $python_version"
        return 0
    else
        print_error "Python no está instalado"
        return 1
    fi
}

check_pip() {
    if command -v pip3 &> /dev/null; then
        print_success "pip3 encontrado"
        return 0
    elif command -v pip &> /dev/null; then
        print_success "pip encontrado"
        return 0
    else
        print_error "pip no está instalado"
        return 1
    fi
}

install_dependencies() {
    print_status "Instalando dependencias..."
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        print_error "No se pudo instalar las dependencias"
        return 1
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas correctamente"
        return 0
    else
        print_error "Error al instalar dependencias"
        return 1
    fi
}

make_executable() {
    print_status "Haciendo ejecutable el script principal..."
    chmod +x main.py
    if [ $? -eq 0 ]; then
        print_success "Script principal ahora es ejecutable"
        return 0
    else
        print_error "Error al hacer ejecutable el script"
        return 1
    fi
}

create_alias() {
    echo
    read -p "¿Deseas crear un alias 'iplocator' para ejecutar la herramienta? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        current_dir=$(pwd)
        
        alias_line="alias iplocator='python3 $current_dir/main.py'"
        
        echo "$alias_line" >> ~/.bashrc
        
        if [ -f ~/.bash_profile ]; then
            echo "$alias_line" >> ~/.bash_profile
        fi
        
        if [ -f ~/.zshrc ]; then
            echo "$alias_line" >> ~/.zshrc
        fi
        
        print_success "Alias 'iplocator' creado exitosamente"
        print_warning "Ejecuta 'source ~/.bashrc' o abre una nueva terminal para usar el alias"
    fi
}

show_usage() {
    echo
    echo -e "${MAGENTA}===============================================${NC}"
    echo -e "${MAGENTA}            INSTALACIÓN COMPLETADA            ${NC}"
    echo -e "${MAGENTA}===============================================${NC}"
    echo
    echo -e "${WHITE}Formas de usar la herramienta:${NC}"
    echo
    echo -e "${GREEN}