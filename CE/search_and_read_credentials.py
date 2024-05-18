"""Librerias."""
import os


class ReadPathCredentials:
    """Funcion para encontrar archivos dentro del path."""
    def search_files_path(self, path_credential, file_extension):
        """Funcion para encontrar archivos dentro del path."""
        path_files = os.listdir(path_credential)
        for name_file in path_files:
            if name_file.endswith(file_extension):
                path_file_found = name_file
                return path_credential+'\\'+path_file_found
        return print("No se encontro el archivo:", file_extension)
            
    def read_password(self, path_credential):
        """Funcion para leer archivo .txt"""
        path_files = os.listdir(path_credential)
        for name_file in path_files:
            if name_file.endswith('.txt'):
                file_found = name_file
        if '.txt' in file_found:
            with open(path_credential+'\\'+file_found, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                return contenido
        else:
            print("No se encontro el archivo .txt")
            return None