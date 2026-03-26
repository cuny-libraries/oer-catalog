# CUNY OER Catalog

A structured catalog of CUNY Open Educational Resources, published as a self-contained HTML file with sortable, searchable, and filterable tables powered by [DataTables](https://datatables.net/).

Each academic year has its own standalone HTML file generated from an Excel source workbook.

---

## Repository structure

```
oer-catalog-2024-2025.html   # Generated catalog (open in any browser or embed in LibGuides)
data/
  oer-catalog-2024-2025.xlsx # Source Excel workbook for AY 2024–2025
generate.py                  # Script used by CI to regenerate HTML
.github/workflows/
  generate.yml               # Automatically regenerates HTML when a workbook is uploaded
README.md
```

---

## Adding or updating a catalog (no technical setup required)

The HTML is generated automatically whenever a workbook is uploaded to the `data/` folder on GitHub. No Python or command-line knowledge is needed.

**The workbook must contain a sheet named `Catalog`** with these columns (in any order):
`Campus`, `OER Title`, `Type`, `Discipline`, `Author`, `Platform`, `Link`

### To update an existing year

1. Go to the repository on GitHub and open the `data/` folder.
2. Click the existing file (e.g., `oer-catalog-2024-2025.xlsx`).
3. Click the pencil/edit icon, then **"Upload a new version"** (or delete the old file and upload the new one).
4. Scroll down and click **"Commit changes"**.

GitHub will automatically regenerate `oer-catalog-2024-2025.html` within a minute or two.

### To add a new academic year

1. Go to the repository on GitHub and open the `data/` folder.
2. Click **"Add file → Upload files"**.
3. Drop in the new workbook, named for the academic year:
   ```
   oer-catalog-2025-2026.xlsx
   ```
4. Click **"Commit changes"**.

GitHub will automatically generate a new `oer-catalog-2025-2026.html` at the root of the repository.

---

## Deploying to the server

Once the HTML has been generated (check the **Actions** tab to confirm the workflow completed), a staff member with SSH access pulls the changes:

```bash
cd /var/www/html/oer
git pull
```

---

## Embedding in a LibGuide

Use a **Rich Text** box or **Media/Widget** box in your LibGuide and paste the following iframe snippet:

```html
<iframe
  src="https://ols.cuny.edu/oer/oer-catalog-2024-2025.html"
  width="100%"
  style="border: none; min-height: 600px;"
  title="CUNY OER Catalog 2024–2025"
></iframe>
```

For future years, update the `src` filename to match the new HTML file (e.g., `oer-catalog-2025-2026.html`).
