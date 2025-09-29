import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

def debug_response(url, session):
    """Debug function to analyze website response"""
    try:
        response = session.get(url, timeout=10)
        print(f"\n=== DEBUG INFO for {url} ===")
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)}")
        print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for tables
        tables = soup.find_all('table')
        print(f"Tables found: {len(tables)}")
        
        # Check for common cause list indicators
        cause_indicators = soup.find_all(text=lambda text: text and any(
            keyword in text.lower() for keyword in ['cause', 'case', 'list', 'hearing']
        ))
        print(f"Cause list indicators: {len(cause_indicators)}")
        
        # Check for forms (might need interaction)
        forms = soup.find_all('form')
        print(f"Forms found: {len(forms)}")
        
        # Save HTML for manual inspection
        filename = f"debug_{url.split('/')[-1] or 'main'}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML saved to: {filename}")
        
        return response, soup
        
    except Exception as e:
        print(f"Debug error for {url}: {e}")
        return None, None

def enhanced_scrape_high_court(session):
    """Enhanced scraper with multiple strategies"""
    url = "https://hcservices.ecourts.gov.in/hcservices/main.php"
    cause_list = []
    
    response, soup = debug_response(url, session)
    if not soup:
        return cause_list
    
    # Strategy 1: Look for any div/section with case-like content
    case_containers = soup.find_all(['div', 'section', 'article'], 
                                   class_=lambda x: x and any(
                                       keyword in x.lower() for keyword in ['case', 'cause', 'list']
                                   ))
    
    # Strategy 2: Look for specific table classes/IDs
    specific_tables = soup.find_all('table', {'class': ['causelist', 'case-list', 'hearing-list']})
    specific_tables.extend(soup.find_all('table', {'id': ['causelist', 'case-list', 'hearing-list']}))
    
    # Strategy 3: All tables (original approach)
    all_tables = soup.find_all('table')
    
    print(f"Case containers: {len(case_containers)}")
    print(f"Specific tables: {len(specific_tables)}")
    print(f"All tables: {len(all_tables)}")
    
    # Try each strategy
    for strategy, elements in [("Case containers", case_containers), 
                              ("Specific tables", specific_tables), 
                              ("All tables", all_tables)]:
        print(f"Trying {strategy}...")
        for element in elements:
            rows = element.find_all('tr') if element.name == 'table' else element.find_all(['p', 'div'])
            for row in rows:
                cells = row.find_all(['td', 'th', 'span', 'div'])
                if len(cells) >= 2:  # Reduced requirement
                    text_content = [cell.get_text(strip=True) for cell in cells]
                    # Look for case number patterns
                    if any(text and ('/' in text or text.isdigit()) for text in text_content):
                        case_data = {
                            'court_type': 'High Court',
                            'case_number': text_content[0] if text_content else '',
                            'party_name': text_content[1] if len(text_content) > 1 else '',
                            'date_of_listing': text_content[2] if len(text_content) > 2 else '',
                            'scraped_at': datetime.now().isoformat(),
                            'raw_data': text_content
                        }
                        cause_list.append(case_data)
    
    return cause_list

def enhanced_scrape_district_court(session):
    """Enhanced district court scraper"""
    url = "https://services.ecourts.gov.in/ecourtindia_v6/"
    cause_list = []
    
    response, soup = debug_response(url, session)
    if not soup:
        return cause_list
    
    # Similar enhanced strategies as high court
    # Look for any element containing case-like data
    all_elements = soup.find_all(['table', 'div', 'section'])
    
    for element in all_elements:
        text = element.get_text(strip=True)
        # Look for case number patterns in text
        if any(pattern in text.lower() for pattern in ['case no', 'vs', 'petitioner', 'respondent']):
            rows = element.find_all('tr') if element.name == 'table' else [element]
            for row in rows:
                cells = row.find_all(['td', 'th']) if row.name == 'tr' else [row]
                if cells:
                    text_content = [cell.get_text(strip=True) for cell in cells]
                    case_data = {
                        'court_type': 'District Court',
                        'case_number': text_content[0] if text_content else '',
                        'party_name': text_content[1] if len(text_content) > 1 else '',
                        'date_of_listing': text_content[2] if len(text_content) > 2 else '',
                        'scraped_at': datetime.now().isoformat(),
                        'raw_data': text_content
                    }
                    cause_list.append(case_data)
    
    return cause_list

def get_enhanced_session():
    """Enhanced session with better headers"""
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

def debug_scrape():
    """Debug version of main scrape function"""
    print("Starting DEBUG court cause list scraping...")
    
    session = get_enhanced_session()
    all_cause_lists = []
    
    # Debug High Court
    print("\n=== DEBUGGING HIGH COURT ===")
    hc_data = enhanced_scrape_high_court(session)
    all_cause_lists.extend(hc_data)
    print(f"Found {len(hc_data)} entries from High Court")
    
    time.sleep(3)
    
    # Debug District Court
    print("\n=== DEBUGGING DISTRICT COURT ===")
    dc_data = enhanced_scrape_district_court(session)
    all_cause_lists.extend(dc_data)
    print(f"Found {len(dc_data)} entries from District Court")
    
    # Save debug results
    if all_cause_lists:
        with open('debug_cause_list.json', 'w', encoding='utf-8') as f:
            json.dump(all_cause_lists, f, indent=2, ensure_ascii=False)
        print(f"Debug data saved with {len(all_cause_lists)} entries")
    else:
        print("Still no data found - check saved HTML files")

if __name__ == "__main__":
    debug_scrape()