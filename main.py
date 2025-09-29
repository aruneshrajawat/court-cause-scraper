from scraper import scrape
from pdf_generator import generate_pdf
from case_checker import check_case

def main():
    """Main function to run all operations in sequence"""
    print("Starting court cause list processing...")
    
    # Step 1: Scrape data
    scrape()
    
    # Step 2: Generate PDF
    generate_pdf()
    
    # Step 3: Check case
    check_case()

if __name__ == "__main__":
    main()