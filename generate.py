#!/usr/bin/env python3
"""
generate.py — Generate a self-contained DataTables HTML catalog from an Excel file.

Usage:
    python3 generate.py data/oer-catalog-2025-2026.xlsx

The output HTML file is written to the current directory with the same base name
as the input file (e.g., oer-catalog-2025-2026.html).
"""

import sys
import os
import html
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("Error: openpyxl is required. Install it with: pip install openpyxl")


FILTER_COLUMNS = ["Campus", "Type", "Discipline", "Platform"]

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/datatables.net-dt@1/css/dataTables.dataTables.min.css">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 14px;
      color: #222;
      margin: 0;
      padding: 16px;
      background: #fff;
    }}
    h1 {{
      font-size: 1.25rem;
      font-weight: 600;
      margin: 0 0 16px;
    }}
    .filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 14px;
      align-items: center;
    }}
    .filters label {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      font-size: 12px;
      font-weight: 600;
      color: #555;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .filters select {{
      font-size: 13px;
      padding: 5px 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      background: #fff;
      cursor: pointer;
      min-width: 160px;
    }}
    .filters select:focus {{
      outline: 2px solid #4a90d9;
      outline-offset: 1px;
    }}
    .table-wrapper {{
      width: 100%;
      overflow-x: auto;
    }}
    #oer-catalog {{
      width: 100% !important;
    }}
    #oer-catalog thead th {{
      white-space: nowrap;
    }}
    #oer-catalog tbody td {{
      vertical-align: top;
      line-height: 1.4;
    }}
    #oer-catalog a {{
      color: #1a5494;
      text-decoration: none;
    }}
    #oer-catalog a:hover {{
      text-decoration: underline;
    }}
    .dataTables_wrapper .dataTables_filter input {{
      border: 1px solid #ccc;
      border-radius: 4px;
      padding: 4px 8px;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div class="filters">
{filter_selects}
  </div>
  <div class="table-wrapper">
    <table id="oer-catalog" class="display" style="width:100%">
      <thead>
        <tr>
{header_cells}
        </tr>
      </thead>
      <tbody>
{body_rows}
      </tbody>
    </table>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/datatables.net@1/js/dataTables.min.js"></script>
  <script>
  $(function () {{
    var table = $('#oer-catalog').DataTable({{
      pageLength: 25,
      lengthMenu: [10, 25, 50, 100],
      order: [[1, 'asc']],
      columnDefs: [{{ targets: '_all', defaultContent: '' }}]
    }});

    // Column index map for dropdown filters
    var filterCols = {filter_col_map};

    // Custom search function for dropdowns
    $.fn.dataTable.ext.search.push(function (settings, data) {{
      for (var col in filterCols) {{
        var val = $('#filter-' + col).val();
        if (val && data[filterCols[col]] !== val) {{
          return false;
        }}
      }}
      return true;
    }});

    // Trigger redraw on dropdown change
    $('.filters select').on('change', function () {{
      table.draw();
    }});
  }});
  </script>
</body>
</html>
"""


def make_select(col_name, options):
    """Build a <label>/<select> block for a filter dropdown."""
    col_id = col_name.lower()
    opt_tags = ['      <option value="">All {}</option>'.format(col_name)]
    for opt in sorted(options):
        esc = html.escape(str(opt), quote=True)
        opt_tags.append('      <option value="{0}">{0}</option>'.format(esc))
    return (
        '    <label>{col}\n'
        '      <select id="filter-{col_id}">\n'
        '{opts}\n'
        '      </select>\n'
        '    </label>'
    ).format(col=col_name, col_id=col_id, opts='\n'.join(opt_tags))


def generate(excel_path: str) -> str:
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    if "Catalog" not in wb.sheetnames:
        sys.exit("Error: sheet 'Catalog' not found in workbook.")
    ws = wb["Catalog"]

    rows = [row for row in ws.iter_rows(values_only=True)]
    if not rows:
        sys.exit("Error: Catalog sheet is empty.")

    headers = [str(h).strip() if h is not None else "" for h in rows[0]]
    data_rows = rows[1:]

    # Column indices
    try:
        title_idx = headers.index("OER Title")
        link_idx = headers.index("Link")
    except ValueError as e:
        sys.exit("Error: required column not found — {}".format(e))

    # Visible columns: all except Link
    visible_headers = [h for h in headers if h != "Link"]

    # Build filter column index map (using visible column indices)
    filter_col_map = {}
    for col in FILTER_COLUMNS:
        if col in visible_headers:
            filter_col_map[col] = visible_headers.index(col)

    # Collect unique values for each filter column (from original headers)
    filter_options = {col: set() for col in FILTER_COLUMNS if col in headers}
    for row in data_rows:
        for col in filter_options:
            idx = headers.index(col)
            val = row[idx]
            if val is not None and str(val).strip():
                filter_options[col].add(str(val).strip())

    # Build filter selects HTML
    filter_selects = "\n".join(
        make_select(col, filter_options[col])
        for col in FILTER_COLUMNS
        if col in filter_options
    )

    # Build header cells
    header_cells = "\n".join(
        "          <th>{}</th>".format(html.escape(h)) for h in visible_headers
    )

    # Build body rows
    body_rows_list = []
    for row in data_rows:
        if all(v is None or str(v).strip() == "" for v in row):
            continue
        link = str(row[link_idx]).strip() if row[link_idx] else ""
        cells = []
        for i, h in enumerate(headers):
            if h == "Link":
                continue
            val = row[i]
            cell_text = str(val).strip() if val is not None else ""
            if h == "OER Title" and link:
                cell_html = '<a href="{}" target="_blank" rel="noopener">{}</a>'.format(
                    html.escape(link, quote=True), html.escape(cell_text)
                )
            else:
                cell_html = html.escape(cell_text)
            cells.append("          <td>{}</td>".format(cell_html))
        body_rows_list.append("        <tr>\n{}\n        </tr>".format("\n".join(cells)))

    body_rows = "\n".join(body_rows_list)

    # Derive a readable title from the filename
    stem = Path(excel_path).stem  # e.g. oer-catalog-2025-2026
    title = stem.replace("-", " ").title()

    import json
    filter_col_map_js = json.dumps(filter_col_map)

    return HTML_TEMPLATE.format(
        title=title,
        filter_selects=filter_selects,
        header_cells=header_cells,
        body_rows=body_rows,
        filter_col_map=filter_col_map_js,
    )


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 generate.py <path/to/excel-file.xlsx>")

    excel_path = sys.argv[1]
    if not os.path.isfile(excel_path):
        sys.exit("Error: file not found: {}".format(excel_path))

    output_name = Path(excel_path).stem + ".html"
    output_path = output_name  # write to current directory

    html_content = generate(excel_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Generated: {}".format(output_path))


if __name__ == "__main__":
    main()
