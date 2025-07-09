"""
Ejemplo de uso de la clase Informe mejorada con estilos modernos
"""

import os
from reportlab.lib.units import inch
from informe import Informe

def crear_informe_ejemplo():
    """Crear un informe de ejemplo mostrando todas las características"""
    
    # Crear instancia del informe
    informe = Informe("informe_ejemplo_moderno", os.getcwd())
    
    # Agregar título principal
    informe.add_title("Informe de Análisis de Datos Modernizado")
    
    # Agregar separador moderno
    informe.add_separator("modern")
    
    # Agregar encabezado de sección
    informe.add_heading("Resumen Ejecutivo")
    
    # Agregar texto normal
    informe.add_sentence(
        "Este es un ejemplo de informe con diseño moderno y atractivo. "
        "El nuevo sistema de estilos utiliza una paleta de colores profesional "
        "y tipografía mejorada para una mejor presentación."
    )
    
    informe.add_spacer(15)
    
    # Agregar texto de éxito
    informe.add_spaced_sentence(
        "✓ Procesamiento completado exitosamente", 
        style_type="success"
    )
    
    # Agregar texto de alerta
    informe.add_spaced_sentence(
        "⚠ Puntos que requieren atención", 
        style_type="highlight"
    )
    
    # Agregar separador
    informe.add_separator("simple")
    
    # Agregar nueva sección
    informe.add_heading("Datos Procesados")
    
    # Crear datos de ejemplo para la tabla
    headers = ["ID Grupal", "Cantidad", "Estado", "Porcentaje"]
    data = [
        ["GRP001", "1,245", "✓ Válido", "85.2%"],
        ["GRP002", "987", "✓ Válido", "78.9%"],
        ["GRP003", "756", "⚠ Revisar", "45.3%"],
        ["GRP004", "1,123", "✓ Válido", "92.1%"],
        ["GRP005", "634", "❌ Error", "23.7%"]
    ]
    
    # Agregar tabla con diseño moderno
    col_widths = [1.5*inch, 1.2*inch, 1.3*inch, 1.2*inch]
    informe.add_table(data, headers=headers, col_widths=col_widths)
    
    # Agregar lista con elementos
    informe.add_heading("Observaciones")
    items = [
        "Los grupos GRP001 y GRP004 muestran excelente performance",
        "El grupo GRP003 requiere revisión manual",
        "El grupo GRP005 presenta errores críticos que deben resolverse",
        "Se recomienda realizar validación adicional en grupos con menos del 50%"
    ]
    informe.add_list(items)
    
    # Agregar separador final
    informe.add_separator("thick")
    
    # Agregar información final
    informe.add_sentence(
        "Informe generado automáticamente por el Sistema Validador v2.0",
        style_type="normal"
    )
    
    # Crear el archivo PDF
    success = informe.create_informe(
        title="Informe Modernizado de Análisis", 
        author="Sistema Validador"
    )
    
    if success:
        print("✓ Informe ejemplo creado exitosamente: informe_ejemplo_moderno.pdf")
    else:
        print("❌ Error al crear el informe ejemplo")

if __name__ == "__main__":
    crear_informe_ejemplo()
