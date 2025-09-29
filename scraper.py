import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time
import re

def get_session():
    """Create a session with headers to mimic a browser"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    return session

def create_sample_data():
    """Create sample cause list data since actual scraping requires complex form interactions"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    sample_cases = [
        {
            'court_type': 'High Court',
            'case_number': 'WP/12345/2024',
            'party_name': 'ABC Company vs State of Maharashtra',
            'date_of_listing': tomorrow.strftime('%d-%m-%Y'),
            'scraped_at': datetime.now().isoformat(),
            'note': 'Sample data - actual scraping requires form submission and captcha'
        },
        {
            'court_type': 'High Court', 
            'case_number': 'CRL/67890/2024',
            'party_name': 'State vs John Doe',
            'date_of_listing': tomorrow.strftime('%d-%m-%Y'),
            'scraped_at': datetime.now().isoformat(),
            'note': 'Sample data - actual scraping requires form submission and captcha'
        },
        {
            'court_type': 'District Court',
            'case_number': 'CC/111/2024',
            'party_name': 'XYZ Ltd vs PQR Industries',
            'date_of_listing': tomorrow.strftime('%d-%m-%Y'),
            'scraped_at': datetime.now().isoformat(),
            'note': 'Sample data - actual scraping requires form submission and captcha'
        },
        {
            'court_type': 'District Court',
            'case_number': 'SC/222/2024', 
            'party_name': 'Ram Kumar vs Shyam Singh',
            'date_of_listing': tomorrow.strftime('%d-%m-%Y'),
            'scraped_at': datetime.now().isoformat(),
            'note': 'Sample data - actual scraping requires form submission and captcha'
        }
    ]
    
    return sample_cases

def scrape_high_court(session):
    """Attempt to scrape High Court - returns sample data due to dynamic content"""
    url = "https://hcservices.ecourts.gov.in/hcservices/main.php"
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        print(f"High Court website accessible (Status: {response.status_code})")
        print("Note: Actual cause lists require form submission with captcha validation")
        
        # Return sample data since actual scraping needs complex interaction
        sample_data = create_sample_data()
        return [case for case in sample_data if case['court_type'] == 'High Court']
        
    except requests.RequestException as e:
        print(f"Error accessing High Court website: {e}")
        return []

def scrape_district_court(session):
    """Attempt to scrape District Court - returns sample data due to dynamic content"""
    url = "https://services.ecourts.gov.in/ecourtindia_v6/"
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        print(f"District Court website accessible (Status: {response.status_code})")
        print("Note: Actual cause lists require navigation to specific court and date selection")
        
        # Return sample data since actual scraping needs complex interaction
        sample_data = create_sample_data()
        return [case for case in sample_data if case['court_type'] == 'District Court']
        
    except requests.RequestException as e:
        print(f"Error accessing District Court website: {e}")
        return []

def save_to_json(data, filename='cause_list.json'):
    """Save extracted data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def scrape():
    """Main function to orchestrate the scraping process"""
    print("Starting court cause list scraping...")
    print("\n=== IMPORTANT NOTE ===")
    print("These court websites use dynamic JavaScript content and require:")
    print("1. Form submissions with specific court/date selections")
    print("2. Captcha validation")
    print("3. Session management")
    print("Generating sample data for demonstration purposes.\n")
    
    session = get_session()
    all_cause_lists = []
    
    # Scrape High Court
    print("Accessing High Court website...")
    hc_data = scrape_high_court(session)
    all_cause_lists.extend(hc_data)
    print(f"Generated {len(hc_data)} sample entries from High Court")
    
    # Add delay between requests
    time.sleep(2)
    
    # Scrape District Court
    print("Accessing District Court website...")
    dc_data = scrape_district_court(session)
    all_cause_lists.extend(dc_data)
    print(f"Generated {len(dc_data)} sample entries from District Court")
    
    # Save to JSON
    if all_cause_lists:
        save_to_json(all_cause_lists)
        print(f"\nTotal sample entries created: {len(all_cause_lists)}")
        print("\nTo get actual data, you would need to:")
        print("1. Use Selenium WebDriver for JavaScript interaction")
        print("2. Implement captcha solving")
        print("3. Handle form submissions for specific courts/dates")
    else:
        print("No data generated")

def scrape_case_by_number(case_type, case_number, year):
    """Search for specific case by number - returns sample data for MVP"""
    try:
        # For MVP, return sample case data
        # In production, this would use Selenium to interact with court websites
        sample_case = {
            'case_type': case_type,
            'case_number': case_number,
            'year': year,
            'party_name': f'Sample Party vs Another Party ({case_number})',
            'date_of_listing': datetime.now().strftime('%d-%m-%Y'),
            'court_name': 'High Court of Mumbai' if case_type == 'High Court' else 'District Court Mumbai',
            'status': 'Listed for hearing',
            'scraped_at': datetime.now().isoformat(),
            'note': 'Sample data - actual scraping requires Selenium WebDriver'
        }
        
        print(f"Generated sample data for case: {case_number}/{year}")
        return sample_case
        
    except Exception as e:
        print(f"Error in case search: {e}")
        return None

if __name__ == "__main__":
    scrape()