from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable, ListFlowable, ListItem
from reportlab.lib.units import inch

styles = getSampleStyleSheet()
tittle_style = styles["Title"]
heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

class Informe():
    def __init__(self, filename, folder_path, pagesize=A4):
        self.filename = filename
        self.folder_path = folder_path
        self.doc = SimpleDocTemplate(f"{folder_path}/{filename}.pdf", pagesize=pagesize)
        self.content = []

        

    def add_title(self, title):
        if not title or len(title) <= 3:
            self.content.append(Paragraph("Sin título", tittle_style))
            self.content.append(Spacer(1, 12))
            return

        self.content.append(Paragraph(title, tittle_style))
        self.content.append(Spacer(1, 12))

    def add_heading(self, heading):
        if not heading or len(heading) <= 3:
            self.content.append(Paragraph("Sin encabezado", heading_style))
            return

        self.content.append(Paragraph(heading, heading_style))

    def add_sentence(self, text, red=False):
        if not text or len(text) <= 3:
            self.content.append(Paragraph("Sin mensaje", normal_style))
            return

        message_style = ParagraphStyle("MessageStyle", parent=normal_style, textColor=colors.red if red else colors.black)
        self.content.append(Paragraph(text, message_style))

    def add_spaced_sentence(self, text, red=False):
        if not text or len(text) <= 5:
            self.content.append(Paragraph("Sin mensaje", normal_style))
            return

        message_style = ParagraphStyle("MessageStyle", parent=normal_style, textColor=colors.red if red else colors.black)
        self.content.append(Paragraph(text, message_style))
        self.content.append(Spacer(1, 12))

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

    def add_table(self, data):
        raise NotImplementedError("add_table method not implemented")


    def create_informe(self):
        self.doc.build(self.content)
