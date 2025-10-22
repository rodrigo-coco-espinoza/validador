from file_selector import FileSelector
import pandas as pd
from informe import Informe
from pprint import pprint
from tkinter import Tk, filedialog
import re
import sys


class Validador:
    def __init__(self, file_path=None, validations=None, rut_prueba=None):

        file_selector = FileSelector()

        # Solicitar archivos y número de gabinete
        self.file_path = file_path if file_path else file_selector.select_file(title="Seleccione archivo a validar")
        self.ruts_prueba_path = rut_prueba if rut_prueba else file_selector.select_file("Seleccione archivo de ruts de prueba")
        self.validation_path = validations if validations else file_selector.select_file("Seleccione archivo de validaciones")
        self.gabinete = input("Ingrese el número de gabinete: ")

        # Cargar archivos y obtener datos
        self.filename = self.file_path.split("/")[-1].rsplit(".", 1)[0]
        self.folder_path = "/".join(self.file_path.split("/")[:-1])
        self.df = file_selector.load_file(self.file_path)     
        self.ruts_prueba = file_selector.load_file(self.ruts_prueba_path)
        self.validations = file_selector.load_validations(self.validation_path)
        

        # Diccionario con validaciones disponibles
        self.validations_availables = {
            "describir_archivo": self.describir_archivo,
            "validate_filename": self.validate_filename,
            "validate_sin_filas_repetidas": self.validate_sin_filas_repetidas,
            "validate_sin_filas_vacias": self.validate_sin_filas_vacias,
            "validate_column_names": self.validate_column_names,
            "validate_column_type": self.validate_column_type,
            "validate_sin_ruts_falsos": self.validate_sin_ruts_falsos,
            "validate_sin_valores_nulos": self.validate_sin_valores_nulos,
            "validate_mayor_igual_a": self.validate_mayor_igual_a,
            "validate_menor_igual_a": self.validate_menor_igual_a,
            "validate_sin_valores_repetidos": self.validate_sin_valores_repetidos,
            "validate_pertenece_a_categorias": self.validate_pertenece_a_categorias,
        }
        

        # Inicializar informe y describir archivo 
        self.informe = Informe(f"validaciones_{self.filename}", self.folder_path)
        self.informe.add_title("Informe de validaciones")
        self.describir_archivo()

    def get_function_param(self, validation_raw):
        validation_split = validation_raw.split("(")
        function = validation_split[0]
        param = validation_split[1].replace(")", "")
        
        return function, param

    # Funciones describe (archivo completo)
    def describir_archivo(self):
        """
        Describe el archivo cargado, incluyendo nombre, fecha, gabinete y número de filas y columnas.
        """

        self.informe.add_heading("Descripción del archivo")
        self.informe.add_sentence(f"Nombre del archivo: {self.file_path.split('/')[-1]}")
        self.informe.add_sentence(f"Fecha del informe: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.informe.add_sentence(f"Gabinete: {self.gabinete}")
        self.informe.add_sentence(f"Número de filas: {len(self.df):,}".replace(",", "."))
        self.informe.add_sentence(f"Número de columnas: {len(self.df.columns)}")
        self.informe.add_sentence(f"Columnas:")
        self.informe.add_list(self.df.columns.tolist())


        # Rut máximo
    
        # Rut minimo
        a = 1

        # Rut entre 30 y 40 millones




    def validate_filename(self, _, expected_pattern):
        """
        Valida que el nombre del archivo tenga el formato esperado.
        Params:
            expected_pattern (str): Patrón esperado del nombre del archivo. 
                                  Use AAAA para año (4 dígitos), MM para mes (2 dígitos), 
                                  DD para día (2 dígitos).
                                  Ejemplos:
                                  - ANEXO_6_A_BTE_AAAAMM
                                  - ANEXO_1_C_ACTECO
                                  - IPS_entrega_actecos_MM_AAAA
        Returns:
            Agrega un mensaje al informe indicando si el nombre del archivo coincide con el patrón esperado.
        """

        self.informe.add_heading("Validación de nombre de archivo")

        # Convertir el patrón a expresión regular
        regex_pattern = expected_pattern
        # Reemplazar los patrones de fecha
        regex_pattern = regex_pattern.replace("AAAA", r"\d{4}")  # Año: 4 dígitos
        regex_pattern = regex_pattern.replace("MM", r"\d{2}")    # Mes: 2 dígitos  
        regex_pattern = regex_pattern.replace("DD", r"\d{2}")    # Día: 2 dígitos
        regex_pattern = regex_pattern.replace("mm", r"\d{2}")    # Mes alternativo: 2 dígitos
        regex_pattern = regex_pattern.replace("aaaa", r"\d{4}")  # Año alternativo: 4 dígitos
        regex_pattern = regex_pattern.replace("dd", r"\d{2}")    # Día alternativo: 2 dígitos
        
        # Agregar anclas para coincidencia exacta
        regex_pattern = f"^{regex_pattern}$"
        
        # Validar el nombre del archivo
        if re.match(regex_pattern, self.filename):
            return self.informe.add_spaced_sentence(f"El nombre del archivo [{self.filename}] coincide con el patrón esperado [{expected_pattern}].")
        else:
            return self.informe.add_spaced_sentence(f"El nombre del archivo [{self.filename}] no coincide con el patrón esperado [{expected_pattern}].", red=True)
    
    def validate_sin_filas_repetidas(self, _, __):
        """
        Valida que no existan filas repetidas en el archivo.
        Returns:
            Agrega un mensaje al informe indicando si existen filas repetidas.
        """

        self.informe.add_heading("Validación de filas repetidas en el archivo")
        if self.df.duplicated().sum() == 0:
            return self.informe.add_spaced_sentence("No existen filas repetidas en el archivo.")
        
        return self.informe.add_spaced_sentence(f"Las siguientes filas se encuentran repetidas: {[index + 1 for index in self.df[self.df.duplicated()].index.tolist()]}", red=True)
    
    def validate_sin_filas_vacias(self, _, __):
        """
        Valida que no existan filas vacías en el archivo.
        Returns:
            Agrega un mensaje al informe indicando si existen filas vacías.
        """
        
        self.informe.add_heading("Validación de filas vacías en el archivo")
        if self.df.empty:
            return self.informe.add_spaced_sentence("El archivo está vacío.", red=True)
        
        empty_rows = self.df[self.df.isnull().all(axis=1)].index.tolist()
        if not empty_rows:
            return self.informe.add_spaced_sentence("No existen filas vacías en el archivo.")
        
        return self.informe.add_spaced_sentence(f"Las siguientes filas están vacías: {[index + 1 for index in empty_rows]}", red=True)
    
    # Funciones específicas (columna)
    def validate_column_names(self, _, expected_names):
        """
        Valida que el nombre esperado de la columna se encuentre en el archivo.
        Params:
            expected_names (str): Nombre esperado de la columna, puede ser una lista separada por comas.
        Returns:
            Agrega un mensaje al informe indicando si el nombre de la columna coincide con el esperado.

        """
        expected_names_list = [name.strip() for name in expected_names.split(",")]
        columns_found = [col for col in expected_names_list if col in self.df.columns]
        columns_not_found = [col for col in expected_names_list if col not in self.df.columns]
        columns_not_expected = [col for col in self.df.columns if col not in expected_names_list]

        self.informe.add_heading("Validación de nombres de columnas")
        if columns_found:
            self.informe.add_sentence(f"Las siguientes columnas pertenecen al archivo: {', '.join(columns_found)}.")
        if columns_not_found:
            self.informe.add_sentence(f"Las siguientes columnas no pertenecen al archivo: {', '.join(columns_not_found)}.", red=True)
        if columns_not_expected:
            self.informe.add_sentence(f"Las siguientes columnas no son esperadas: {', '.join(columns_not_expected)}.", red=True)

        self.informe.add_spacer()



    def validate_column_type(self, column_name, expected_type):
        """
        Valida que el tipo de dato de la columna sea el esperado.
        Params:
            column_name (str): Nombre de la columna a validar.
            expected_type (str): Tipo de dato esperado de la columna, valores posibles: texto, entero, decimal, fecha.
        Returns:  
            bool: True si el tipo de dato de la columna es el esperado, False en caso contrario.
        """

        if expected_type not in ["texto", "entero", "decimal", "fecha"]:
            raise ValueError("Tipo de dato no válido.")

        if expected_type == "texto":
            if pd.api.types.is_string_dtype(self.df[column_name]):
                return True
        elif expected_type == "entero":
            if pd.api.types.is_integer_dtype(self.df[column_name]):
                return True
            else:
                return self.df[~pd.api.types.is_integer_dtype(self.df[column_name])].index.tolist()

        elif expected_type == "decimal":
            if pd.api.types.is_float_dtype(self.df[column_name]):
                return True
            else:
                return self.df[column_name][pd.api.types.is_float_dtype(self.df[column_name])].tolist()
        elif expected_type == "fecha":
            if pd.api.types.is_datetime64_any_dtype(self.df[column_name]):
                return True
            else:
                return self.df[column_name][not pd.api.types.is_datetime64_any_dtype(self.df[column_name])].tolist()

        
        # try:
        #     self.df[column_name] = self.df[column_name].astype(expected_type)
        #     return True
        # except ValueError:
        #     return False

    def validate_sin_ruts_falsos(self, column_name, _):
        """
        Valida que los RUTs de la columna no estén en el archivo de RUTs de prueba.
        Params:
            column_name (str): Nombre de la columna a validar, debe contener RUTs.
        Returns:
            list: Lista de RUTs que están en el archivo de RUTs de prueba.
        """
        if not pd.api.types.is_integer_dtype(self.df[column_name]):
            raise TypeError("La columna no es numérica.")

        ruts_prueba = self.ruts_prueba.iloc[:, 0].tolist()
        ruts_df = self.df[column_name].tolist()
        ruts_falsos = [rut for rut in ruts_df if rut in ruts_prueba]
        
        if ruts_falsos:
            return ruts_falsos
        return True
    
    def validate_sin_valores_nulos(self, column_name, _):
        return self.df[column_name].isnull().sum() == 0
    
    def validate_mayor_igual_a(self, column_name, value):
        menores = self.df[column_name][self.df[column_name] < float(value)].tolist()
        if menores:
            return menores
        return True
    
    def validate_menor_igual_a(self, column_name, value):
        mayores = self.df[column_name][self.df[column_name] > float(value)].tolist()
        if mayores:
            return mayores
        return True

    def validate_sin_valores_repetidos(self, column_name, _):
        repetidos = self.df[column_name][self.df[column_name].duplicated()].tolist()
        if repetidos:
            return list(set(repetidos))
        return True

    def validate_pertenece_a_categorias(self, column_name, cat_string):
        """
        Valida que los valores de la columna pertenezcan a las categorías especificadas.
        Params:
            column_name (str): Nombre de la columna a validar.
            cat_string (str): Categorías válidas separadas por comas.
        Returns:
            Agrega un mensaje al informe indicando si todos los valores pertenecen a las categorías esperadas.
        """
        self.informe.add_heading(f"Validación de categorías en columna '{column_name}'")
        
        # Separar y limpiar las categorías
        categorias_str = [cat.strip() for cat in cat_string.split(",")]
        
        # Convertir las categorías al tipo de dato de la columna
        try:
            if pd.api.types.is_numeric_dtype(self.df[column_name]):
                categorias = [float(cat) if '.' in cat else int(cat) for cat in categorias_str]
            else:
                categorias = categorias_str
        except ValueError:
            return self.informe.add_spaced_sentence(f"Error: No se pudieron convertir las categorías [{cat_string}] al tipo de dato de la columna.", red=True)
        
        # Verificar qué valores pertenecen a las categorías
        pertenece = self.df[column_name].isin(categorias)
        valores_invalidos = self.df[column_name][~pertenece].unique().tolist()
        valores_encontrados = self.df[column_name].unique().tolist()
        
        # Mostrar información básica
        self.informe.add_sentence(f"Categorías esperadas: {', '.join(categorias_str)}.")
        self.informe.add_sentence(f"Valores encontrados en la columna: {valores_encontrados[:15]}{'...' if len(valores_encontrados) > 15 else ''}.")
        
        if pertenece.all():
            return self.informe.add_spaced_sentence(f"✓ Todos los valores de la columna '{column_name}' pertenecen a las categorías esperadas.")
        else:
            count_invalidos = (~pertenece).sum()
            self.informe.add_sentence(f"✗ Se encontraron {count_invalidos:,} valores que no pertenecen a las categorías esperadas.".replace(",", "."), red=True)
            self.informe.add_sentence(f"Valores inválidos: {valores_invalidos[:10]}{'...' if len(valores_invalidos) > 10 else ''}.", red=True)
            self.informe.add_spacer()
    
    def validate_fecha_desde(self, column_name, _):
        raise NotImplementedError
    
    def validate_fecha_hasta(self, column_name, _):
        raise NotImplementedError
    
    def validate_nulos_permitidos(self, column_name, _):
        raise NotImplementedError
    
    def validate_sin_caracteres_especiales(self, column_name, _):
        raise NotImplementedError
    
    def validate_comuna(self, column_name, _):
        raise NotImplementedError

    def run_validations(self):

        for campo, validation in self.validations:
            function, param = self.get_function_param(validation)
            if function in self.validations_availables:

                self.validations_availables[function](campo, param)

            else:
                self.informe.add_heading(f"Validación {function}")
                self.informe.add_spaced_sentence("No se encontró la función de validación.")

        self.informe.create_informe()
        print("Informe generado con éxito.")

if __name__ == "__main__":
    # Verificar si se pasaron argumentos desde la línea de comandos
    if len(sys.argv) == 4:
        # Usar argumentos de línea de comandos: archivo_datos, validaciones, ruts_prueba
        archivo_datos = sys.argv[1]
        archivo_validaciones = sys.argv[2]
        archivo_ruts_prueba = sys.argv[3]
        
        print(f"Ejecutando validaciones con:")
        print(f"- Archivo de datos: {archivo_datos}")
        print(f"- Archivo de validaciones: {archivo_validaciones}")
        print(f"- Archivo de RUTs de prueba: {archivo_ruts_prueba}")
        
        validador = Validador(archivo_datos, archivo_validaciones, archivo_ruts_prueba)
        validador.run_validations()
    elif len(sys.argv) == 1:
        # Modo interactivo (sin argumentos) - usar selección de archivos
        print("Modo interactivo: seleccione los archivos manualmente")
        validador = Validador(None, None, "RUTDEPRUEBAS.CSV")
        validador.run_validations()
    else:
        # Mostrar ayuda si el número de argumentos es incorrecto
        print("Uso del programa:")
        print("  Modo CLI: python validaciones.py <archivo_datos> <archivo_validaciones> <archivo_ruts_prueba>")
        print("  Ejemplo:  python validaciones.py catastro_ciren.csv validaciones_ciren.csv RUTDEPRUEBA.csv")
        print("  Modo interactivo: python validaciones.py (sin argumentos)")
        sys.exit(1)


    