import requests
import json

API_URL = "https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json"

params = {
    'q': 'Computer Science',
    'degree[]': '2',
    'lang[]': '2',
    'limit': '10',
    'offset': '0',
    'display': 'list',
    'sort': '4'
}

print("Testing API with params:")
print(json.dumps(params, indent=2))
print("\nMaking request...")

response = requests.get(API_URL, params=params, timeout=30)
print(f"Status Code: {response.status_code}")
print(f"\nResponse URL: {response.url}")
print(f"\nResponse Content (first 2000 chars):")
print(response.text[:2000])

if response.status_code == 200:
    try:
        data = response.json()
        print(f"\n\nJSON Keys: {list(data.keys())}")
        print(f"Number of results: {data.get('numFound', 0)}")
        if 'results' in data and len(data['results']) > 0:
            print(f"\nFirst program:")
            print(json.dumps(data['results'][0], indent=2))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
