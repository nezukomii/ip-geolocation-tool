#!/usr/bin/env python3
"""
IP Geolocation Tool
Una herramienta para localizar direcciones IP usando múltiples fuentes públicas
"""
# Developed By Nezukomi >w<

import requests
import json
import sys
import re
import time
import random
from typing import Dict, Optional, List
from urllib.parse import urlencode
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class Colors:
    """Colores para la terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class IPLocator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.sources = [
            self._get_ipinfo_data,
            self._get_ipstack_data,
            self._get_ipgeolocation_data,
            self._get_freegeoip_data,
            self._get_ipwhois_data
        ]
    
    def _validate_ip(self, ip: str) -> bool:
        """Valida si la IP es válida"""
        pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip))
    
    def _get_ipinfo_data(self, ip: str) -> Optional[Dict]:
        """Obtiene datos de ipinfo.io"""
        try:
            response = self.session.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'loc' in data:
                    lat, lon = data['loc'].split(',')
                    return {
                        'ip': ip,
                        'country': data.get('country', 'N/A'),
                        'region': data.get('region', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'latitude': lat,
                        'longitude': lon,
                        'org': data.get('org', 'N/A'),
                        'postal': data.get('postal', 'N/A'),
                        'timezone': data.get('timezone', 'N/A'),
                        'source': 'ipinfo.io'
                    }
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error con ipinfo.io: {e}{Colors.END}")
        return None
    
    def _get_ipstack_data(self, ip: str) -> Optional[Dict]:
        """Obtiene datos usando scraping de ipstack público"""
        try:
            response = self.session.get(f'http://ip-api.com/json/{ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'ip': ip,
                        'country': data.get('country', 'N/A'),
                        'region': data.get('regionName', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'latitude': str(data.get('lat', 'N/A')),
                        'longitude': str(data.get('lon', 'N/A')),
                        'org': data.get('isp', 'N/A'),
                        'postal': data.get('zip', 'N/A'),
                        'timezone': data.get('timezone', 'N/A'),
                        'source': 'ip-api.com'
                    }
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error con ip-api.com: {e}{Colors.END}")
        return None
    
    def _get_ipgeolocation_data(self, ip: str) -> Optional[Dict]:
        """Obtiene datos de freegeoip"""
        try:
            response = self.session.get(f'https://freegeoip.app/json/{ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'ip': ip,
                    'country': data.get('country_name', 'N/A'),
                    'region': data.get('region_name', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'latitude': str(data.get('latitude', 'N/A')),
                    'longitude': str(data.get('longitude', 'N/A')),
                    'org': 'N/A',
                    'postal': data.get('zip_code', 'N/A'),
                    'timezone': data.get('time_zone', 'N/A'),
                    'source': 'freegeoip.app'
                }
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error con freegeoip.app: {e}{Colors.END}")
        return None
    
    def _get_freegeoip_data(self, ip: str) -> Optional[Dict]:
        """Obtiene datos de ipapi.co"""
        try:
            response = self.session.get(f'https://ipapi.co/{ip}/json/', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    return {
                        'ip': ip,
                        'country': data.get('country_name', 'N/A'),
                        'region': data.get('region', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'latitude': str(data.get('latitude', 'N/A')),
                        'longitude': str(data.get('longitude', 'N/A')),
                        'org': data.get('org', 'N/A'),
                        'postal': data.get('postal', 'N/A'),
                        'timezone': data.get('timezone', 'N/A'),
                        'source': 'ipapi.co'
                    }
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error con ipapi.co: {e}{Colors.END}")
        return None
    
    def _get_ipwhois_data(self, ip: str) -> Optional[Dict]:
        """Obtiene datos adicionales"""
        try:
            response = self.session.get(f'http://ipwhois.app/json/{ip}', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return {
                        'ip': ip,
                        'country': data.get('country', 'N/A'),
                        'region': data.get('region', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'latitude': str(data.get('latitude', 'N/A')),
                        'longitude': str(data.get('longitude', 'N/A')),
                        'org': data.get('isp', 'N/A'),
                        'postal': 'N/A',
                        'timezone': data.get('timezone', 'N/A'),
                        'source': 'ipwhois.app'
                    }
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error con ipwhois.app: {e}{Colors.END}")
        return None
    
    def get_location(self, ip: str) -> Optional[Dict]:
        """Obtiene la ubicación de una IP usando múltiples fuentes"""
        if not self._validate_ip(ip):
            print(f"{Colors.RED}[!] Dirección IP inválida: {ip}{Colors.END}")
            return None
        
        print(f"{Colors.BLUE}[*] Buscando información para IP: {ip}{Colors.END}")
        print(f"{Colors.CYAN}[*] Consultando múltiples fuentes...{Colors.END}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(source, ip): source for source in self.sources}
            
            for future in as_completed(futures, timeout=30):
                try:
                    result = future.result()
                    if result:
                        print(f"{Colors.GREEN}[+] Datos obtenidos de: {result['source']}{Colors.END}")
                        return result
                except Exception as e:
                    print(f"{Colors.YELLOW}[!] Error en una fuente: {e}{Colors.END}")
        
        print(f"{Colors.RED}[!] No se pudo obtener información de la IP{Colors.END}")
        return None
    
    def display_info(self, data: Dict):
        """Muestra la información de forma decorativa"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}               INFORMACIÓN DE GEOLOCALIZACIÓN{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🌐 IP Address:{Colors.END} {Colors.WHITE}{data['ip']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🏳️  País:{Colors.END} {Colors.WHITE}{data['country']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🏛️  Región:{Colors.END} {Colors.WHITE}{data['region']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🏙️  Ciudad:{Colors.END} {Colors.WHITE}{data['city']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}📍 Latitud:{Colors.END} {Colors.WHITE}{data['latitude']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}📍 Longitud:{Colors.END} {Colors.WHITE}{data['longitude']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🏢 Organización:{Colors.END} {Colors.WHITE}{data['org']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}📮 Código Postal:{Colors.END} {Colors.WHITE}{data['postal']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🕐 Zona Horaria:{Colors.END} {Colors.WHITE}{data['timezone']}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}📡 Fuente:{Colors.END} {Colors.WHITE}{data['source']}{Colors.END}")
        
        # Mostrar enlace a Google Maps
        if data['latitude'] != 'N/A' and data['longitude'] != 'N/A':
            maps_url = f"https://maps.google.com/maps?q={data['latitude']},{data['longitude']}"
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}🗺️  Google Maps:{Colors.END} {Colors.BLUE}{maps_url}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")

def print_banner():
    """Imprime el banner de la herramienta"""
    banner = f"""
{Colors.BOLD}{Colors.CYAN}
██╗██████╗     ██╗      ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
██║██╔══██╗    ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║██████╔╝    ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
██║██╔═══╝     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
██║██║         ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝╚═╝         ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Colors.END}
{Colors.BOLD}{Colors.GREEN}                    📍 IP Geolocation Tool v1.0 📍{Colors.END}
{Colors.BOLD}{Colors.YELLOW}                   Desarrollado por: Nezukomi{Colors.END}
{Colors.BOLD}{Colors.MAGENTA}                  GitHub: github.com/nezukomii{Colors.END}

{Colors.BOLD}{Colors.WHITE}Una herramienta avanzada localizar direcciones IP usando múltiples fuentes{Colors.END}
"""
    print(banner)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Herramienta de geolocalización por IP')
    parser.add_argument('-i', '--ip', help='Dirección IP a localizar')
    parser.add_argument('-f', '--file', help='Archivo con lista de IPs')
    parser.add_argument('-o', '--output', help='Archivo de salida JSON')
    
    args = parser.parse_args()
    
    print_banner()
    
    locator = IPLocator()
    results = []
    
    if args.ip:
        data = locator.get_location(args.ip)
        if data:
            locator.display_info(data)
            results.append(data)
    
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            
            for ip in ips:
                data = locator.get_location(ip)
                if data:
                    locator.display_info(data)
                    results.append(data)
                time.sleep(1)  
        except FileNotFoundError:
            print(f"{Colors.RED}[!] Archivo no encontrado: {args.file}{Colors.END}")
            return
    
    else:
        while True:
            try:
                ip = input(f"\n{Colors.BOLD}{Colors.CYAN}[?] Ingresa una dirección IP (o 'quit' para salir): {Colors.END}")
                if ip.lower() in ['quit', 'exit', 'q']:
                    print(f"{Colors.GREEN}[+] ¡Hasta luego!{Colors.END}")
                    break
                
                data = locator.get_location(ip)
                if data:
                    locator.display_info(data)
                    results.append(data)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Interrumpido por el usuario{Colors.END}")
                break
    
    if args.output and results:
        try:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n{Colors.GREEN}[+] Resultados guardados en: {args.output}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error al guardar archivo: {e}{Colors.END}")

if __name__ == "__main__":
    main()