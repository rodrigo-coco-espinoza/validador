import os
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable
from reportlab.lib.units import inch
from datetime import datetime

def procesar_archivo(file_path):
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

def generar_informe_pdf(conteo_datos, fecha, output_filename="informe.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    elements.append(Paragraph("Informe de Conteo por ID Grupal", title_style))
    
    # Verificar archivos con ID grupales de menos de 11 contribuyentes
    archivos_problema = []
    for archivo, (conteo_por_id_grupal, _) in conteo_datos.items():
        if any(cantidad < 11 for cantidad in conteo_por_id_grupal.values()):
            archivos_problema.append(archivo)
    
    # Determinar mensaje condicional y color
    if archivos_problema:
        message_style = ParagraphStyle("MessageStyle", parent=normal_style, textColor=colors.red, fontName="Helvetica-Bold")
        mensaje = "Los archivos presentan grupos con menos de 11 contribuyentes."
        elements.append(Paragraph(mensaje, message_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Archivos con grupos de menos de 11 contribuyentes:", message_style))
        
        # Listar los archivos con problemas
        for archivo in archivos_problema:
            elements.append(Paragraph(f"- {archivo}", normal_style))
    else:
        message_style = ParagraphStyle("MessageStyle", parent=normal_style, textColor=colors.green, fontName="Helvetica-Bold")
        mensaje = "Los archivos no presentan grupos con menos de 11 contribuyentes."
        elements.append(Paragraph(mensaje, message_style))

    elements.append(Spacer(1, 12))
    
    for archivo, (conteo_por_id_grupal, total_filas) in conteo_datos.items():
        elements.append(Spacer(1, 12))  # Espacio adicional antes del siguiente archivo
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=10, spaceAfter=10))

        elements.append(Paragraph(f"Archivo procesado: {archivo}", heading_style))
        elements.append(Paragraph(f"Total de filas procesadas: {total_filas:,}", normal_style))
        
        elements.append(Spacer(1, 12))

        if conteo_por_id_grupal:
            data = [["ID Grupal", "Cantidad de Filas"]]
            ids_ordenados = sorted(conteo_por_id_grupal.items(), key=lambda x: x[1])

            for id_grupal, cantidad in ids_ordenados:
                data.append([id_grupal, f"{cantidad:,}"])

            table = Table(data, colWidths=[2 * inch, 2 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No se encontraron filas válidas en este archivo.\n", normal_style))

    try:
        doc.build(elements)
        print(f"Informe PDF generado con éxito: {output_filename}")
    except Exception as e:
        print(f"Error al generar el informe PDF: {e}")

def generar_informe():
    ruta_carpeta = os.getcwd()
    archivos_txt = [f for f in os.listdir(ruta_carpeta) if f.endswith('.txt')]

    if not archivos_txt:
        print("No se encontraron archivos .txt en la carpeta.")
        return

    conteo_datos = {}
    for archivo in archivos_txt:
        file_path = os.path.join(ruta_carpeta, archivo)
        conteo_por_id_grupal, total_filas = procesar_archivo(file_path)
        conteo_datos[archivo] = (conteo_por_id_grupal, total_filas)

    # Obtener la fecha actual en formato AAAAMMDD para el nombre del archivo PDF
    fecha = datetime.now().strftime("%Y%m%d")
    output_filename = f"Informe_Conversiones_{fecha}.pdf"
    generar_informe_pdf(conteo_datos, fecha, output_filename)

if __name__ == "__main__":
    generar_informe()
