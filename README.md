# CUNY OER Catalog

A structured catalog of CUNY Open Educational Resources, published as a self-contained HTML file with sortable, searchable, and filterable tables powered by [DataTables](https://datatables.net/).

Each academic year has its own standalone HTML file generated from an Excel source workbook.

---

## Repository structure

```
oer-catalog-2024-2025.html   # Generated catalog (open in any browser or embed in LibGuides)
data/
  oer-catalog-2024-2025.xlsx # Source Excel workbook for AY 2024–2025
generate.py                  # Script to regenerate HTML from an Excel file
README.md
```

---

## Generating the HTML for a new year

**Requirements:** Python 3 and `openpyxl`.

```bash
pip install openpyxl
```

1. Drop the new Excel file into `data/`, named for the academic year:
   ```
   data/oer-catalog-2026-2027.xlsx
   ```
   The workbook must contain a sheet named **Catalog** with these columns:
   `Campus`, `OER Title`, `Type`, `Discipline`, `Author`, `Platform`, `Link`

2. From the repo root, run:
   ```bash
   python3 generate.py data/oer-catalog-2026-2027.xlsx
   ```
   This writes `oer-catalog-2026-2027.html` to the current directory.

3. Commit both files and push:
   ```bash
   git add oer-catalog-2026-2027.html data/oer-catalog-2026-2027.xlsx
   git commit -m "Add AY 2026-2027 OER catalog"
   git push
   ```

---

## Deploying updates to the server

On the server, pull the latest changes:

```bash
cd /path/to/oer-catalog
git pull
```

No build step or server restart is needed — the HTML file is fully self-contained.

---

## Embedding in a LibGuide

Use a **Rich Text** box or **Media/Widget** box in your LibGuide and paste the following iframe snippet, replacing the `src` URL with the raw GitHub Pages or server URL for the HTML file:

```html
<iframe
  src="https://cuny-libraries.github.io/oer-catalog/oer-catalog-2024-2025.html"
  width="100%"
  style="border: none; min-height: 600px;"
  title="CUNY OER Catalog 2024–2025"
></iframe>
```

> **Tip:** GitHub Pages must be enabled for the repository (Settings → Pages → deploy from `main` branch, `/ (root)`). The HTML file will then be available at `https://cuny-libraries.github.io/oer-catalog/<filename>.html`.

---

## Updating catalog content

Catalog editors update the Excel file. A staff member with SSH access to the server then:

1. Replaces the Excel file in `data/` with the updated version.
2. Runs `python3 generate.py data/oer-catalog-YYYY-YYYY.xlsx` to regenerate the HTML.
3. Commits both files and pushes to GitHub.
4. SSHs into the server and runs `git pull`.
