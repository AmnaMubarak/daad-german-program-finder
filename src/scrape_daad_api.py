import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
from urllib.parse import urljoin

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

API_URL = "https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json"
BASE_URL = "https://www2.daad.de"

def get_all_programs():
    """Fetch all Computer Science Master's programs using the API"""
    print("Fetching all programs from DAAD API...")
    
    params = {
        'q': 'Computer Science',
        'degree[]': '2',  # Master's degree
        'lang[]': '2',    # English
        'cert': '',
        'admReq': '',
        'langExamPC': '',
        'langExamLC': '',
        'langExamSC': '',
        'langDeAvailable': '',
        'langEnAvailable': '',
        'fee': '',
        'sort': '4',
        'dur': '',
        'limit': '100',
        'offset': '0',
        'display': 'list',
        'isElearning': '',
        'isSep': ''
    }
    
    all_programs = []
    offset = 0
    page = 1
    
    while True:
        params['offset'] = str(offset)
        
        try:
            response = requests.get(API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'courses' in data and len(data['courses']) > 0:
                programs = data['courses']
                print(f"Page {page}: Found {len(programs)} programs")
                all_programs.extend(programs)
                
                total = data.get('numResults', 0)
                if offset + len(programs) >= total:
                    break
                    
                offset += len(programs)
                page += 1
                time.sleep(0.5)
            else:
                break
                
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    print(f"\n✓ Total programs found: {len(all_programs)}")
    return all_programs

def extract_program_details(program_data):
    """Extract detailed information from a program's detail page"""
    program_id = program_data.get('id', '')
    program_name = program_data.get('courseName', program_data.get('name', ''))
    
    if 'link' in program_data:
        detail_url = BASE_URL + program_data['link']
    else:
        detail_url = f"{BASE_URL}/deutschland/studienangebote/international-programmes/en/detail/{program_id}/"
    
    print(f"  Fetching details from: {program_name[:60]}...")
    
    try:
        time.sleep(0.5)
        response = requests.get(detail_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        full_text = soup.get_text(separator='\n', strip=True)
        
        details = {
            'Program Name': program_name,
            'University': program_data.get('academy', program_data.get('institution', '')),
            'City': program_data.get('city', ''),
            'Program URL': detail_url,
            'Language': 'English',
            'Duration': program_data.get('programmeDuration', ''),
            'Tuition Fees': program_data.get('tuitionFees', ''),
            'Beginning': program_data.get('beginning', ''),
            'Application Deadline': '',
            'Language Requirements': '',
            'IELTS Required': 'Unknown',
            'MOI Accepted': 'Unknown',
            'Full Page Text': full_text
        }
        
        for dt in soup.find_all(['dt', 'th']):
            label = dt.get_text(strip=True).lower()
            dd = dt.find_next_sibling(['dd', 'td'])
            if not dd:
                continue
            value = dd.get_text(strip=True)
            
            if 'duration' in label or 'length' in label:
                details['Duration'] = value
            elif 'tuition' in label or 'fee' in label:
                details['Tuition Fees'] = value
            elif 'beginning' in label or 'start' in label:
                details['Beginning'] = value
            elif 'deadline' in label:
                details['Application Deadline'] = value
        
        lang_keywords = ['language requirement', 'language skills', 'english proficiency', 
                         'language certificate', 'proof of english']
        
        for keyword in lang_keywords:
            pattern = re.compile(keyword, re.IGNORECASE)
            section = soup.find(text=pattern)
            
            if section:
                container = section.find_parent(['div', 'section', 'article', 'dl', 'ul'])
                if container:
                    lang_text = container.get_text(separator=' ', strip=True)
                    details['Language Requirements'] = lang_text
                    break
        
        lang_req_lower = details['Language Requirements'].lower()
        full_text_lower = full_text.lower()
        
        if 'ielts' in full_text_lower:
            if any(phrase in full_text_lower for phrase in ['not required', 'not necessary', 'waived', 'alternative']):
                details['IELTS Required'] = 'No - Alternatives accepted'
            elif 'ielts' in lang_req_lower and any(phrase in lang_req_lower for phrase in ['required', 'must', 'need']):
                details['IELTS Required'] = 'Yes'
            else:
                details['IELTS Required'] = 'Mentioned'
        else:
            details['IELTS Required'] = 'Not Mentioned'
        
        moi_keywords = ['medium of instruction', 'moi', 'english-taught', 'taught in english',
                        'instruction in english', 'proof of english instruction', 
                        'bachelor.*english', 'previous degree.*english']
        
        for keyword in moi_keywords:
            if re.search(keyword, full_text_lower):
                details['MOI Accepted'] = 'Yes'
                break
        
        if details['MOI Accepted'] == 'Unknown':
            if any(phrase in full_text_lower for phrase in ['proof of language', 'demonstrate english', 
                                                              'english proficiency', 'certificate of english']):
                if 'ielts' not in lang_req_lower or 'toefl' not in lang_req_lower:
                    details['MOI Accepted'] = 'Possible - Check Details'
        
        return details
        
    except Exception as e:
        print(f"    Error: {e}")
        return {
            'Program Name': program_name,
            'University': program_data.get('academy', program_data.get('institution', '')),
            'City': program_data.get('city', ''),
            'Program URL': detail_url if 'detail_url' in locals() else '',
            'Language': 'English',
            'Duration': program_data.get('programmeDuration', ''),
            'Tuition Fees': program_data.get('tuitionFees', ''),
            'Beginning': program_data.get('beginning', ''),
            'Application Deadline': '',
            'Language Requirements': f'Error fetching: {str(e)}',
            'IELTS Required': 'Unknown',
            'MOI Accepted': 'Unknown',
            'Full Page Text': ''
        }

def main():
    print("=" * 70)
    print("DAAD Computer Science Master's Programs Scraper")
    print("=" * 70)
    print()
    
    programs_api_data = get_all_programs()
    
    if not programs_api_data:
        print("No programs found!")
        return
    
    print(f"\nFound {len(programs_api_data)} programs total.")
    print("Processing all programs will take significant time.")
    
    user_input = input("\nHow many programs to process? (Enter number or 'all'): ").strip()
    
    if user_input.lower() == 'all':
        num_to_process = len(programs_api_data)
    else:
        try:
            num_to_process = int(user_input)
            num_to_process = min(num_to_process, len(programs_api_data))
        except:
            num_to_process = 10
            print(f"Invalid input. Processing first {num_to_process} programs.")
    
    print(f"\n{'=' * 70}")
    print(f"Processing {num_to_process} programs...")
    print(f"{'=' * 70}\n")
    
    all_details = []
    
    for i, program in enumerate(programs_api_data[:num_to_process], 1):
        print(f"[{i}/{num_to_process}] Processing program...")
        details = extract_program_details(program)
        all_details.append(details)
    
    if all_details:
        df = pd.DataFrame(all_details)
        
        column_order = ['Program Name', 'University', 'City', 'Duration', 'Tuition Fees', 
                       'Beginning', 'Application Deadline', 'Language', 
                       'IELTS Required', 'MOI Accepted', 'Language Requirements',
                       'Program URL', 'Full Page Text']
        
        column_order = [col for col in column_order if col in df.columns]
        df = df[column_order]
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_file = os.path.join(OUTPUT_DIR, 'german_cs_masters_programs.xlsx')
        df.to_excel(output_file, index=False)
        
        print(f"\n{'=' * 70}")
        print(f"✓ SUCCESS!")
        print(f"{'=' * 70}")
        print(f"Data saved to: {output_file}")
        print(f"Total programs processed: {len(all_details)}")
        print()
        
        ielts_not_required = df[df['IELTS Required'].str.contains('No', na=False)].shape[0]
        moi_accepted = df[df['MOI Accepted'] == 'Yes'].shape[0]
        
        print("Summary:")
        print(f"  - Programs where IELTS may not be required: {ielts_not_required}")
        print(f"  - Programs that may accept MOI: {moi_accepted}")
    else:
        print("No program details extracted!")

if __name__ == "__main__":
    main()
