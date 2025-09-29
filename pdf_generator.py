from fpdf import FPDF
import json
import os
from datetime import datetime

def generate_case_pdf(query_data):
    """Generate PDF for case data"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # Title
    pdf.cell(0, 10, 'Court Case Details', 0, 1, 'C')
    pdf.ln(10)
    
    # Query details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"Case Type: {query_data['case_type']}", 0, 1)
    pdf.cell(0, 8, f"Case Number: {query_data['case_number']}", 0, 1)
    pdf.cell(0, 8, f"Year: {query_data['year']}", 0, 1)
    pdf.cell(0, 8, f"Query Date: {query_data['created_at']}", 0, 1)
    pdf.ln(5)
    
    # Case data
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 8, 'Case Information:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    case_data = query_data['response_data']
    if isinstance(case_data, dict):
        for key, value in case_data.items():
            pdf.cell(0, 6, f"{key.replace('_', ' ').title()}: {value}", 0, 1)
    else:
        pdf.cell(0, 6, str(case_data), 0, 1)
    
    # Save PDF
    pdf_filename = f"case_{query_data['id']}.pdf"
    pdf_path = os.path.join('static', pdf_filename)
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    pdf.output(pdf_path)
    return pdf_path