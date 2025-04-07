from file_selector import FileSelector
import pandas as pd
from informe import Informe
from pprint import pprint
from tkinter import Tk, filedialog


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
            "validate_column_name": self.validate_column_name,
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

    # Funciones generales (archivo completo)
    def describir_archivo(self):
        self.informe.add_heading("Descripción del archivo")
        self.informe.add_sentence(f"Nombre del archivo: {self.file_path.split('/')[-1]}")
        self.informe.add_sentence(f"Fecha del informe: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.informe.add_sentence(f"Gabinete: {self.gabinete}")
        self.informe.add_sentence(f"Número de filas: {len(self.df)}")
        self.informe.add_sentence(f"Número de columnas: {len(self.df.columns)}")
        self.informe.add_sentence(f"Columnas:")
        self.informe.add_list(self.df.columns.tolist())

    def validate_filename(self, _, expected_filename):
        self.informe.add_heading("Validación de nombre de archivo")
        if self.filename == expected_filename:
            return self.informe.add_spaced_sentence(f"El nombre del archivo [{self.filename}] coincide con el nombre esperado [{expected_filename}].")
            
        
        return self.informe.add_spaced_sentence(f"El nombre del archivo [{self.filename}] no coincide con el nombre esperado [{expected_filename}].", red=True)
    
    def validate_sin_filas_repetidas(self, _, __):
        """
        Valida que no existan filas repetidas en el archivo.
        Returns:
            True si no existen filas repetidas. En caso contrario, devuelve una lista con los índices de las filas repetidas (partiendo de 0).
        """
        if self.df.duplicated().sum() == 0:
            return True
        
        return self.df[self.df.duplicated()].index.tolist()
    
    def validate_sin_filas_vacias(self, _, __):
        """
        Valida que no existan filas vacías en el archivo.
        Returns:
            True si no existen filas vacías. En caso contrario, devuelve una lista con los índices de las filas vacías (partiendo de 0).
        """
        empty_rows = self.df[self.df.isnull().all(axis=1)].index.tolist()
        if not empty_rows:
            return True
        
        return empty_rows
    
    # Funciones específicas (columna)
    def validate_column_name(self, _, expected_name):
        """
        Valida que el nombre esperado de la columna se encuentre en el archivo.
        Params:
            expected_name (str): Nombre esperado de la columna.
        Returns:
            bool: True si existe la columna con ese nombre, False en caso contrario.
        """
        if expected_name in self.df.columns:
            return True
        return False
    
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
        categorias = [self.df[column_name].dtype.type(cat) for cat in cat_string.split(",")]
        pertenece = self.df[column_name].isin(categorias)
        if pertenece.all():
            return True
        return self.df[column_name][~pertenece].tolist()
    
    def validate_fecha_desde(self, column_name, _):
        raise NotImplementedError
    
    def validate_fecha_hasta(self, column_name, _):
        raise NotImplementedError
    
    def validate_nulos_permitidos(self, column_name, _):
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
    validador = Validador(None, None, "RUTDEPRUEBAS.CSV")
    validador.run_validations()


    