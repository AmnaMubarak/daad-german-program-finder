# DAAD German Masters Finder

A Python tool that aggregates **English-taught Master's programs in Germany** from the [DAAD (Deutscher Akademischer Austauschdienst)](https://www.daad.de/) — the official German government-backed database for international study programs.

Instead of manually browsing programs one by one on the DAAD website, this tool **fetches all 1,000+ programs via the DAAD API**, analyzes their language requirements, and gives you everything in a categorized, color-coded Excel file.

## What It Does

1. **Fetches all program listings** from the DAAD API (structured JSON data)
2. **Analyzes detail pages** for each program to extract language requirements not available through the API
3. **Flags key info** — whether **IELTS is required** and whether **MOI (Medium of Instruction)** certificates are accepted
4. **Categorizes programs** by field (Data Science & AI, Cybersecurity, Software Engineering, etc.)
5. **Exports** to a color-coded Excel file with separate sheets per category

## How It Works

| Step | Method | What happens |
|------|--------|-------------|
| Fetch program listings | **DAAD JSON API** | Gets structured data (name, university, city, tuition, duration) for all matching programs |
| Analyze language requirements | **HTML parsing** | Visits each program's detail page to extract IELTS, MOI, and deadline info not available in the API |
| Categorize & export | **pandas + openpyxl** | Groups programs by field, applies color-coding, and exports to Excel |

> **Why Germany only?** DAAD is Germany's official academic exchange portal. The API endpoint is under `/deutschland/` and exclusively lists programs offered at German universities.

## Project Structure

```
German-MS/
├── src/
│   ├── scrape_daad_api.py       # Fetches programs from DAAD API + analyzes detail pages
│   └── organize_programs.py     # Categorizes programs & formats Excel output
├── tests/
│   └── test_api.py              # DAAD API endpoint tester
├── output/                      # Generated Excel files (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/<your-username>/daad-german-masters-finder.git
cd daad-german-masters-finder

pip install -r requirements.txt
```

## Usage

```bash
# Step 1: Fetch programs from DAAD API
python src/scrape_daad_api.py

# Step 2: Organize and categorize the results
python src/organize_programs.py
```

The tool will ask how many programs to process. Enter a number or type `all` to process everything.

## Output

Generated files are saved to the `output/` folder:

- `german_cs_masters_programs.xlsx` — All program data with language requirement analysis
- `german_cs_masters_programs_organized.xlsx` — Categorized and color-coded version with:
  - **All Programs** overview sheet (sorted by category)
  - Individual sheets per category (Data Science & AI, Cybersecurity, Software Engineering, etc.)
  - Color-coded rows, formatted headers, frozen panes

## API

This project uses the **DAAD International Programmes API** — a public JSON endpoint:

```
https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json
```

**No API keys required.** The endpoint is publicly accessible. Detail pages are parsed for additional language requirement info not available through the API.

## Dependencies

- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing
- `pandas` — Data manipulation
- `openpyxl` — Excel file creation and formatting

## License

This project is for personal/educational use.
