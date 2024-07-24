#!/usr/bin/env python


import argparse
import sys, os, time
from colorama import init, Fore
from dns.exception import DNSException
import dns.resolver
from contextlib import suppress
from threading import Thread
from pathlib import Path

def Colors():
    global red, yellow, green; red = Fore.RED; yellow = Fore.YELLOW; green = Fore.LIGHTGREEN_EX

def Banner():
    banner = f"""{Fore.RED}
   ____     __      __                _        _____         __       
  / __/_ __/ /  ___/ /__  __ _  ___ _(_)__    / __(_)__  ___/ /__ ____
 _\ \/ // / _ \/ _  / _ \/  ' \/ _ `/ / _ \  / _// / _ \/ _  / -_) __/
/___/\_,_/_.__/\_,_/\___/_/_/_/\_,_/_/_//_/ /_/ /_/_//_/\_,_/\__/_/                                                         
    """
    return banner

def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('subdominios', metavar='Lista de subdominios', help='', type=str)
    parser.add_argument('dominio', metavar='Dominio principal', help='', type=str)
    
    global args; args = parser.parse_args()
    
    if args.subdominios is None or args.dominio is None:
        time.sleep(1)
    
def Dividir_Archivivo(archivo):
    cont = 0
    list1 = list()
    list2 = list()
    with open(archivo, 'r') as file:
        for _ in file:
            cont += 1
        division = cont / 2
    cont = 0
    with open(archivo, 'r') as file:
        for word in file:
            cont += 1
            list1.append(word.rstrip())
            if int(division) == cont:
                break
    cont = 0
    with open(archivo, 'r') as file:
        for word in file:
            cont += 1
            if int(division) >= cont:
                pass
            else:
                list2.append(word.rstrip())
                
    return (list1, list2)

def Crear_Nuevos_Archivos(subdominios1, subdominios2):
    name1 = 'new1.txt'
    name2 = 'new2.txt'
    folder = 'subdominios'
    def crear_archivos():
        with open(f'{folder}\{name1}', 'w') as file:
            for word in subdominios1:
                file.write(f'{word}\n')
            file.close()
            
        with open(f'{folder}\{name2}', 'w') as file:
            for word in subdominios2:
                file.write(f'{word}\n')
            file.close()
    try:
        crear_archivos()
    
    except FileExistsError:
        crear_archivos()

    return (f'{folder}\{name1}', f'{folder}\{name2}')

def Borrar_Archivos_Temporales():
    os.remove('subdominios/new1.txt')
    os.remove('subdominios/new2.txt')
    

class Buscador(object):
    def __init__(self, dominio):
        self.dominio = dominio
        
        if 'http' in self.dominio:
            self.dominio = self.dominio.replace('http', '')
        
    def Buscar_Subdominios(self, subdominios):
        self.subdominios = subdominios
        self.encontrados = list()
        self.file = open('subdominios\Encontrados.txt', 'a')
        with open(self.subdominios, 'r') as subdominios:
            for subdominio in subdominios:
                subdominio = subdominio.rstrip()
                if subdominio == '':
                    pass
                try:
                    search = dns.resolver.resolve(f'{subdominio}.{self.dominio}', 'A')
                    self.encontrados.append(f'{subdominio}.{self.dominio}')
                    if search:
                        time.sleep(.005)
                        print(f'{green}[+] Subdominio encontrado: {subdominio}.{self.dominio}')
                except DNSException:
                    print(f'{red}[x] Subdominio no encontrado: {subdominio}.{self.dominio}')
        for subdominio in self.encontrados:
            self.file.write(subdominio + '\n')
        self.file.close()

if __name__ == '__main__':
    init()
    Colors()
    while True:
        try:
            fileObject = Path('subdominios/Encontrados.txt')
            if fileObject.is_file() is True:
                os.remove('subdominios/Encontrados.txt')
            setup()
            print(Banner())
            time.sleep(1)
            lista1, lista2 = Dividir_Archivivo(args.subdominios)
            file1, file2 = Crear_Nuevos_Archivos(lista1, lista2)
            buscador = Buscador(args.dominio)
            hilo1 = Thread(target=buscador.Buscar_Subdominios(file1))
            hilo1.start()
            time.sleep(0.5)
            hilo2 = Thread(target=buscador.Buscar_Subdominios(file2))
            hilo2.start()
            Borrar_Archivos_Temporales()
            break
    
        except KeyboardInterrupt:
            time.sleep(1)
            print(f'{red}[{yellow}i{red}] Cancelar busqueda de subdominios? [{yellow}yes{red}/{yellow}no{red}]', end=f' -> {yellow}')
            options = ['yes', 'no', 'YES', 'NO']
            option = str(input(''))
                
            while option not in options:
                print(f'{red}[{yellow}i{red}] Cancelar busqueda de subdominios? [{yellow}yes{red}/{yellow}no{red}]', end=f' -> {yellow}')
                option = str(input(''))
        
            if option == 'yes' or option == 'YES':
                time.sleep(1)
                print(Banner())
                print(f'{red}[x] Programa cancelado')
                sys.exit()
            
            elif option == 'no' or option == 'NO':
                with suppress(Exception):
                    continue
