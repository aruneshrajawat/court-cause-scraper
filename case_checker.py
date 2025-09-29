import json
from datetime import datetime, timedelta

def check_case():
    """Check if a case is listed for tomorrow"""
    # Read JSON data
    try:
        with open('cause_list.json', 'r', encoding='utf-8') as f:
            cases = json.load(f)
    except FileNotFoundError:
        print("cause_list.json not found")
        return
    
    # Get user input
    case_number = input("Enter case number: ").strip()
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
    
    # Check if case is listed tomorrow
    for case in cases:
        if (case.get('case_number', '').strip().lower() == case_number.lower() and 
            tomorrow in case.get('date_of_listing', '')):
            print("✅ Your case is listed tomorrow.")
            return
    
    print("❌ Your case is NOT listed tomorrow.")

if __name__ == "__main__":
    check_case()