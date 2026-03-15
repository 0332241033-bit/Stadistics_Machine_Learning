from fpdf import FPDF
import datetime


def _safe_pdf_text(text):
    """Convert text to a representation supported by FPDF core fonts (latin-1)."""
    return str(text).encode("latin-1", "replace").decode("latin-1")

class SegmentReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ANALISIS DE SEGMENTACION IA', 0, 1, 'C')
        self.ln(10)

def generate_pdf(category, description, coords):
    pdf = SegmentReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    safe_category = _safe_pdf_text(category)
    safe_description = _safe_pdf_text(description)
    
    pdf.cell(0, 10, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.ln(5)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, f" RESULTADO: {safe_category}", 1, 1, 'L', fill=True)
    
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, f"Descripcion: {safe_description}")
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Coordenadas PCA (Espacio Reducido):", 0, 1)
    pdf.set_font('Courier', '', 10)
    pdf.cell(0, 8, f"PC1: {coords[0]:.4f} | PC2: {coords[1]:.4f}", 0, 1)
    
    filename = "reporte_actual.pdf"
    pdf.output(filename)
    return filename