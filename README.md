# DAAD German Master's Programs Scraper

A Python-based scraper that collects and organizes **English-taught Computer Science Master's programs** in Germany from the [DAAD (Deutscher Akademischer Austauschdienst)](https://www.daad.de/) database.

## What It Does

- Fetches Master's program listings from the DAAD international programmes database
- Extracts detailed information for each program (university, city, duration, tuition, deadlines)
- Analyzes language requirements — flags whether **IELTS is required** and whether **Medium of Instruction (MOI)** certificates are accepted
- Exports everything to a **color-coded, categorized Excel file** with separate sheets per category (Data Science & AI, Cybersecurity, Software Engineering, etc.)

## Project Structure

```
German-MS/
├── src/
│   ├── scrape_daad_api.py      # Main scraper (DAAD API + detail pages)
│   ├── scrape_daad.py           # Alternative HTML-based scraper
│   └── organize_programs.py     # Categorizer & Excel formatter
├── tests/
│   └── test_api.py              # DAAD API endpoint tester
├── output/                      # Generated Excel files (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Scripts

| Script | Description |
|--------|-------------|
| `src/scrape_daad_api.py` | **Main scraper** — uses the DAAD JSON API to fetch programs, then scrapes detail pages for language requirements. Outputs to `output/` |
| `src/scrape_daad.py` | **Alternative scraper** — uses HTML scraping instead of the API for the search results page |
| `src/organize_programs.py` | **Post-processor** — reads the scraped Excel file, categorizes programs by field, applies color-coding and formatting |
| `tests/test_api.py` | **API tester** — quick script to test the DAAD API endpoint and inspect the response structure |

## Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/daad-german-masters-scraper.git
cd daad-german-masters-scraper

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Step 1: Scrape programs from DAAD
python src/scrape_daad_api.py

# Step 2: Organize and categorize the results
python src/organize_programs.py
```

The scraper will ask how many programs to process. Enter a number or type `all` to process everything.

## Output

Generated files are saved to the `output/` folder:

- `german_cs_masters_programs.xlsx` — Raw scraped data with all program details
- `german_cs_masters_programs_organized.xlsx` — Categorized and color-coded version with:
  - **All Programs** overview sheet (sorted by category)
  - Individual sheets for each category (Data Science & AI, Cybersecurity, Software Engineering, etc.)
  - Color-coded rows, formatted headers, frozen panes

## API Used

This project uses the **DAAD International Programmes API** — a public, unauthenticated JSON endpoint:

```
https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json
```

**No API keys are required.** The endpoint is publicly accessible.

## Dependencies

- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing
- `pandas` — Data manipulation
- `openpyxl` — Excel file creation and formatting

## License

This project is for personal/educational use.
