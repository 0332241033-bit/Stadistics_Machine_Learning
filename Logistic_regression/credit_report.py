from fpdf import FPDF
import datetime

class CreditReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'DICTAMEN DE EVALUACIÓN DE CRÉDITO IA', 0, 1, 'C')
        self.ln(10)

def generate_credit_pdf(inputs, result, probability):
    pdf = CreditReport()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, "Datos del Solicitante:", 0, 1)
    pdf.set_font('Arial', '', 10)
    for k, v in inputs.items():
        pdf.cell(0, 7, f"- {k.replace('_', ' ').title()}: {v}", 0, 1)
    
    pdf.ln(10)
    # Color según resultado: Verde para aprobado (Ham), Rojo para riesgo (Spam/Riesgo)
    color = (200, 255, 200) if result == "APROBADO" else (255, 200, 200)
    pdf.set_fill_color(*color)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 15, f" ESTATUS: {result}", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Probabilidad de Impago calculada: {probability:.2%}", 0, 1, 'C')
    
    filename = "dictamen_credito.pdf"
    pdf.output(filename)
    return filename