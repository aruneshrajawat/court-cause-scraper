import json
from fpdf import FPDF

def generate_pdf():
    """Generate PDF from cause_list.json"""
    # Read JSON data
    try:
        with open('cause_list.json', 'r', encoding='utf-8') as f:
            cases = json.load(f)
    except FileNotFoundError:
        print("cause_list.json not found")
        return
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Court Cause List', 0, 1, 'C')
    pdf.ln(10)
    
    # Add cases
    pdf.set_font('Arial', '', 12)
    for case in cases:
        case_number = case.get('case_number', '')
        party_name = case.get('party_name', '')
        date_of_listing = case.get('date_of_listing', '')
        
        line = f"{case_number} - {party_name} - {date_of_listing}"
        pdf.cell(0, 8, line.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
    
    # Save PDF
    pdf.output('cause_list.pdf')
    print("PDF generated: cause_list.pdf")

if __name__ == "__main__":
    generate_pdf()