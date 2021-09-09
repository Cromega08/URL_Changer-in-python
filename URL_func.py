import pyshorteners as pyshort
import pyperclip as clip
import pyqrcode as pyqr
import png
from pathlib import Path as p
import shutil as sh
import os
import sys

class file():

    def __init__(self):

        self.current = p.cwd()
        self.downloads = self.check()

    def check(self):
        
        dir_down = self.current.joinpath("URL_Download")

        if dir_down.exists():

            return str(dir_down)      

        dir_down.mkdir(777, exist_ok=True)

    def move(self, file_out):

        if type(file_out) == type("a"):

            source = p(self.current).joinpath(file_out)
            sh.move(source, self.downloads)
        
        else:

            for paths in file_out:

                source = p(self.current).joinpath(paths)
                sh.move(source, self.downloads)

    def clipboard(self, string):

        copy = input("Desea copiarlo al portapapeles? [y/n]: ")
        
        if copy == "y":

            clip.copy(string)
            print("Copiado al portapapeles")

class functions():

    def __init__(self, link):
        
        self.link = link

    def shortener(self):

        short = pyshort.Shortener()
        shorted = short.tinyurl.short(self.link)
        print(shorted)
        return shorted

    def qr_input(self):

        name = input("Ingrese el nombre del archivo: ")

        scale_u = input("Si desea modificar la escala, ingrese el valor\n"\
                    "~ 1(s) = 1.3(cm) or 0.51(in)\n"\
                    "~ No ingrese nada mas que valores numericos\n"\
                    "~ Si desea usar la escala predeterminada(8), presione 'Enter'\n\n"\
                    "Escala (max. 8): ")

        scale = int(scale_u) if scale_u != "" else 8

        save  = input("Desea guardarlo como:\n"\
                    "1. 'png'\n"\
                    "2. 'svg'\n"\
                    "3. Ambas\n\n"\
                    "Opcion: ")

        validate = [name != "", scale in list(range(0, 9)), int(save) in list(range(0, 4))]

        if all(validate):

            return name, scale, save
        
        else:

            print("Parametros incorrectos, ingreselos de nuevo")
            self.qr_input()

    def qr_creator(self, name, scale, save):

        qr = pyqr.create(self.link)
        suffix = ".png" if save == "1" else ".svg" if save == "2" else "(.png)/(.svg)"
        qr.show(wait = 5, scale = scale)
        action = input(f"Nombre: {name}{suffix}\n"+\
                        f"Tamaño:{qr.get_png_size(scale=scale)}kb\n\n"+\
                        "Esta de acuerdo? [y/n]: ")
        
        if action == "y":

            if save == "1" or save == "3":
            
                qr.png(f"{name}.png", scale=scale)
            
            if save == "2" or save == "3":
                
                qr.svg(f"{name}.svg", scale=scale)

            if save != "3":

                return f"{name}{suffix}"
            
            else:

                return [f"{name}.png", f"{name}.svg"]

class app():

    def __init__(self):

        self.file = file()
        self.exec()
    
    def exec(self):

        choice = input("Que desea hacer?\n"\
                    "1. Acortar un URL\n"\
                    "2. Generar un codigo QR\n"\
                    "3. Salir\n\n"\
                    "Opcion: ")

        link = input("Ingrese el URL: ")

        func = functions(link)
        self.clear_screen()

        if choice == "1":

            shorted = func.shortener()
            self.file.clipboard(shorted)
            self.clear_screen(True)
            self.exec()

        elif choice == "2":

            name, scale, save = func.qr_input()
            path = func.qr_creator(name, scale, save)
            self.file.move(path)
            print("Codigo QR creado con exito")
            self.clear_screen(True)
            self.exec()

        elif choice == "3":
            
            self.clear_screen()
            sys.exit()
    
    def clear_screen(self, wait = False):

        if wait == True:

            os.system("Pause")

        if os.name == "nt":

            os.system("cls")
        
        else:

            os.system("clear")