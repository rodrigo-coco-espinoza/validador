"""
Versión mejorada de procesar_txt.py usando la clase Informe modernizada
"""

import os
from collections import defaultdict
from datetime import datetime
from reportlab.lib.units import inch
from informe import Informe

def procesar_archivo(file_path):
    """Procesar archivo y contar ocurrencias por ID grupal"""
    conteo_por_id_grupal = defaultdict(int)
    total_filas = 0

    try:
        with open(file_path, 'r') as f:
            for linea in f:
                if len(linea) >= 24:
                    id_grupal = linea[:13]
                    conteo_por_id_grupal[id_grupal] += 1
                    total_filas += 1
                else:
                    print(f"Línea ignorada por tener menos de 24 caracteres: {linea.strip()}")
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")

    return conteo_por_id_grupal, total_filas

def generar_informe_moderno(conteo_datos, fecha, output_filename="informe_moderno.pdf"):
    """
    Generar informe PDF con diseño moderno usando la clase Informe mejorada
    """
    try:
        # Crear instancia del informe
        informe = Informe(output_filename.replace('.pdf', ''), os.getcwd())
        
        # Título principal
        informe.add_title("Informe de Conteo por ID Grupal")
        
        # Verificar archivos con ID grupales de menos de 11 contribuyentes
        archivos_problema = []
        for archivo, (conteo_por_id_grupal, _) in conteo_datos.items():
            if any(cantidad < 11 for cantidad in conteo_por_id_grupal.values()):
                archivos_problema.append(archivo)
        
        # Mensaje condicional con estilos modernos
        if archivos_problema:
            informe.add_spaced_sentence(
                "⚠ Los archivos presentan grupos con menos de 11 contribuyentes.",
                style_type="highlight"
            )
            
            informe.add_sentence(
                "Archivos con grupos de menos de 11 contribuyentes:",
                style_type="highlight"
            )
            informe.add_spacer(8)
            
            # Listar archivos con problemas
            informe.add_list([f"📄 {archivo}" for archivo in archivos_problema])
        else:
            informe.add_spaced_sentence(
                "✓ Los archivos no presentan grupos con menos de 11 contribuyentes.",
                style_type="success"
            )

        informe.add_separator("modern")
        
        # Procesar cada archivo
        for i, (archivo, (conteo_por_id_grupal, total_filas)) in enumerate(conteo_datos.items()):
            if i > 0:  # Separador entre archivos (excepto el primero)
                informe.add_separator("simple")
            
            # Información del archivo
            informe.add_heading(f"📊 Archivo: {archivo}")
            informe.add_sentence(f"Total de filas procesadas: {total_filas:,}")
            informe.add_spacer(12)

            if conteo_por_id_grupal:
                # Preparar datos para la tabla
                headers = ["ID Grupal", "Cantidad de Filas", "Estado"]
                data = []
                
                # Ordenar por cantidad (menor a mayor para identificar problemas)
                ids_ordenados = sorted(conteo_por_id_grupal.items(), key=lambda x: x[1])

                for id_grupal, cantidad in ids_ordenados:
                    # Determinar estado basado en la cantidad
                    if cantidad < 11:
                        estado = "⚠ Revisar"
                    elif cantidad < 50:
                        estado = "⚡ Bajo"
                    else:
                        estado = "✓ Normal"
                    
                    data.append([id_grupal, f"{cantidad:,}", estado])

                # Agregar tabla con diseño moderno
                col_widths = [2*inch, 1.5*inch, 1.5*inch]
                informe.add_table(data, headers=headers, col_widths=col_widths)
                
                # Estadísticas adicionales
                total_grupos = len(conteo_por_id_grupal)
                grupos_problematicos = sum(1 for cantidad in conteo_por_id_grupal.values() if cantidad < 11)
                
                informe.add_spacer(10)
                informe.add_sentence(f"📈 Total de grupos únicos: {total_grupos}")
                
                if grupos_problematicos > 0:
                    informe.add_sentence(
                        f"⚠ Grupos con menos de 11 contribuyentes: {grupos_problematicos}",
                        style_type="highlight"
                    )
                else:
                    informe.add_sentence(
                        "✓ Todos los grupos tienen 11 o más contribuyentes",
                        style_type="success"
                    )
            else:
                informe.add_sentence(
                    "❌ No se encontraron filas válidas en este archivo",
                    style_type="highlight"
                )

        # Información final
        informe.add_separator("thick")
        informe.add_sentence(
            f"Informe generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}",
            style_type="normal"
        )
        
        # Crear el informe
        success = informe.create_informe(
            title=f"Informe de Conteo - {fecha}",
            author="Sistema Validador"
        )
        
        if success:
            print(f"✓ Informe PDF moderno generado con éxito: {output_filename}")
        else:
            print(f"❌ Error al generar el informe PDF moderno")
            
    except Exception as e:
        print(f"❌ Error al generar el informe moderno: {e}")

def generar_informe():
    """Función principal para generar el informe"""
    ruta_carpeta = os.getcwd()
    archivos_txt = [f for f in os.listdir(ruta_carpeta) if f.endswith('.txt')]

    if not archivos_txt:
        print("❌ No se encontraron archivos .txt en la carpeta.")
        return

    print(f"📂 Procesando {len(archivos_txt)} archivo(s) .txt encontrado(s)...")
    
    conteo_datos = {}
    for archivo in archivos_txt:
        file_path = os.path.join(ruta_carpeta, archivo)
        print(f"   📄 Procesando: {archivo}")
        conteo_por_id_grupal, total_filas = procesar_archivo(file_path)
        conteo_datos[archivo] = (conteo_por_id_grupal, total_filas)

    # Obtener la fecha actual para el nombre del archivo
    fecha = datetime.now().strftime("%Y%m%d")
    output_filename = f"Informe_Conversiones_Moderno_{fecha}.pdf"
    
    # Generar el informe moderno
    generar_informe_moderno(conteo_datos, fecha, output_filename)

if __name__ == "__main__":
    print("🚀 Iniciando generación de informe moderno...")
    generar_informe()
    print("✅ Proceso completado.")
