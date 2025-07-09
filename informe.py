from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable, ListFlowable, ListItem
from reportlab.lib.units import inch

# Crear estilos modernos y atractivos
styles = getSampleStyleSheet()

# Estilo para título principal - moderno y elegante
title_style = ParagraphStyle(
    'ModernTitle',
    parent=styles['Title'],
    fontSize=24,
    spaceAfter=20,
    textColor=colors.HexColor('#2C3E50'),  # Azul oscuro elegante
    alignment=1,  # Centrado
    fontName='Helvetica-Bold',
    borderWidth=2,
    borderColor=colors.HexColor('#3498DB'),  # Azul moderno
    borderPadding=10
)

# Estilo para encabezados - con color y espaciado mejorado
heading_style = ParagraphStyle(
    'ModernHeading',
    parent=styles['Heading2'],
    fontSize=16,
    spaceAfter=12,
    spaceBefore=18,
    textColor=colors.HexColor('#34495E'),  # Gris azulado
    fontName='Helvetica-Bold',
    leftIndent=0,
    borderWidth=0,
    borderColor=colors.HexColor('#E74C3C'),  # Rojo elegante
    borderPadding=8
)

# Estilo para texto normal - mejorado
normal_style = ParagraphStyle(
    'ModernBody',
    parent=styles['BodyText'],
    fontSize=11,
    spaceAfter=6,
    textColor=colors.HexColor('#2C3E50'),
    fontName='Helvetica',
    alignment=4,  # Justificado
    lineHeight=1.4
)

# Estilo para texto destacado
highlight_style = ParagraphStyle(
    'Highlight',
    parent=normal_style,
    fontSize=12,
    textColor=colors.HexColor('#E74C3C'),  # Rojo elegante
    fontName='Helvetica-Bold',
    spaceAfter=8,
    spaceBefore=8
)

# Estilo para texto de éxito
success_style = ParagraphStyle(
    'Success',
    parent=normal_style,
    fontSize=12,
    textColor=colors.HexColor('#27AE60'),  # Verde elegante
    fontName='Helvetica-Bold',
    spaceAfter=8,
    spaceBefore=8
)

class Informe():
    def __init__(self, filename, folder_path, pagesize=A4):
        self.filename = filename
        self.folder_path = folder_path
        self.doc = SimpleDocTemplate(f"{folder_path}/{filename}.pdf", pagesize=pagesize)
        self.content = []

        

    def add_title(self, title):
        if not title or len(title) <= 3:
            self.content.append(Paragraph("Sin título", title_style))
            self.content.append(Spacer(1, 12))
            return

        self.content.append(Paragraph(title, title_style))
        self.content.append(Spacer(1, 12))

    def add_heading(self, heading):
        if not heading or len(heading) <= 3:
            self.content.append(Paragraph("Sin encabezado", heading_style))
            return

        self.content.append(Paragraph(heading, heading_style))

    def add_sentence(self, text, red=False, style_type="normal"):
        if not text or len(text) <= 3:
            self.content.append(Paragraph("Sin mensaje", normal_style))
            return

        # Seleccionar el estilo según el tipo
        if style_type == "highlight" or red:
            selected_style = highlight_style
        elif style_type == "success":
            selected_style = success_style
        else:
            selected_style = normal_style
            
        self.content.append(Paragraph(text, selected_style))

    def add_spaced_sentence(self, text, red=False, style_type="normal"):
        if not text or len(text) <= 5:
            self.content.append(Paragraph("Sin mensaje", normal_style))
            return

        # Seleccionar el estilo según el tipo
        if style_type == "highlight" or red:
            selected_style = highlight_style
        elif style_type == "success":
            selected_style = success_style
        else:
            selected_style = normal_style
            
        self.content.append(Paragraph(text, selected_style))
        self.content.append(Spacer(1, 12))

    def add_spacer(self, height=12):
        self.content.append(Spacer(1, height))

    def add_separator(self, style="modern"):
        """
        Agregar un separador visual moderno
        
        Args:
            style: Tipo de separador ("modern", "simple", "thick")
        """
        if style == "modern":
            # Separador moderno con gradiente visual
            separator = HRFlowable(
                width="80%", 
                thickness=2, 
                color=colors.HexColor('#3498DB'), 
                spaceBefore=15, 
                spaceAfter=15,
                hAlign='CENTER'
            )
        elif style == "thick":
            # Separador grueso
            separator = HRFlowable(
                width="100%", 
                thickness=3, 
                color=colors.HexColor('#2C3E50'), 
                spaceBefore=10, 
                spaceAfter=10
            )
        else:
            # Separador simple
            separator = HRFlowable(
                width="100%", 
                thickness=1, 
                color=colors.HexColor('#BDC3C7'), 
                spaceBefore=8, 
                spaceAfter=8
            )
        
        self.content.append(separator)

    def add_list(self, items):
        if not items:
            self.content.append(Paragraph("Sin lista", normal_style))
            return

        table_data = [
            Paragraph(item, normal_style) for item in items
        ]
        table = ListFlowable(
            table_data,
            bulletType='bullet'
        )   
        self.content.append(table)
        self.content.append(Spacer(1, 12))

    def add_table(self, data, headers=None, col_widths=None):
        """
        Agregar una tabla con diseño moderno
        
        Args:
            data: Lista de listas con los datos de la tabla
            headers: Lista con los encabezados (opcional)
            col_widths: Lista con los anchos de columnas (opcional)
        """
        if not data:
            self.content.append(Paragraph("Sin datos para mostrar en la tabla", normal_style))
            return

        # Preparar los datos
        table_data = []
        
        # Agregar encabezados si existen
        if headers:
            table_data.append(headers)
        
        # Agregar datos
        for row in data:
            table_data.append(row)

        # Crear la tabla con anchos personalizados o por defecto
        if col_widths:
            table = Table(table_data, colWidths=col_widths)
        else:
            # Calcular anchos automáticamente
            num_cols = len(table_data[0]) if table_data else 1
            auto_width = (7 * inch) / num_cols  # Distribuir en 7 pulgadas
            table = Table(table_data, colWidths=[auto_width] * num_cols)

        # Estilo moderno para la tabla
        table_style = [
            # Estilo para encabezados (si existen)
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Estilo para el cuerpo de la tabla
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            
            # Alternating row colors para mejor legibilidad
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ECF0F1'), colors.HexColor('#F8F9FA')]),
            
            # Padding para mejor espaciado
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]
        
        # Si no hay encabezados, ajustar el estilo
        if not headers:
            table_style = [
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECF0F1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#ECF0F1'), colors.HexColor('#F8F9FA')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]

        table.setStyle(TableStyle(table_style))
        self.content.append(table)
        self.content.append(Spacer(1, 12))


    def create_informe(self, title="Informe Generado", author="Sistema Validador"):
        """
        Crear el informe PDF con metadatos y configuración mejorada
        
        Args:
            title: Título del documento para metadatos
            author: Autor del documento para metadatos
        """
        try:
            # Configurar metadatos del documento
            self.doc.title = title
            self.doc.author = author
            self.doc.subject = "Informe generado automáticamente"
            self.doc.creator = "Sistema Validador Python"
            
            # Construir el documento
            self.doc.build(self.content)
            
            return True
        except Exception as e:
            print(f"Error al crear el informe: {e}")
            return False
