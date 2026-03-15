from fpdf import FPDF
import datetime

class BillingReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PREDICCIÓN DE PRESUPUESTO CLOUD', 0, 1, 'L')
        self.ln(5)

def generate_billing_pdf(inputs, prediction):
    pdf = BillingReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    pdf.cell(0, 10, f"Fecha de Proyección: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1)
    pdf.ln(5)
    
    # Tabla de insumos
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, "Variables de Infraestructura Analizadas:", 0, 1)
    pdf.set_font('Arial', '', 10)
    for key, value in inputs.items():
        pdf.cell(0, 8, f"- {key}: {value}", 0, 1)
    
    pdf.ln(10)
    pdf.set_fill_color(255, 240, 200)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 15, f" COSTO ESTIMADO MENSUAL: ${prediction:,.2f} USD", 1, 1, 'C', fill=True)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, "Nota: Esta predicción se basa en un modelo de regresión lineal entrenado con datos históricos de consumo de recursos computacionales.")
    
    filename = "proyeccion_costos.pdf"
    pdf.output(filename)
    return filename