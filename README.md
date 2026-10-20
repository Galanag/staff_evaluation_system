# Ambo University Academic & Administrative Performance Evaluation System

A standalone Django application for the academic evaluation workflow in the supplied materials, plus the Amharic six-month administrative performance summary form. It uses Django templates, custom HTML/CSS/JavaScript, SQLite for local development, and OpenPyXL for formatted `.xlsx` workbooks.

> **Starting-repository note:** I reviewed the public repository structure and its core settings/models/views. The starter is a Django 4.2 project with `config/`, an app folder named `evalutions/` (misspelled), a tracked `db.sqlite3`, and `manage.py`. Its current models provide evaluation cycles/questions/submissions/responses, while the views expose a basic dashboard and academic submission flow; the detailed Ambo Form A–E content, the six-month Amharic form, full reporting/export UI, and archive workflow were not present in the inspected views. The starter settings also contain a hard-coded development secret and `DEBUG=True`, so do not expose that starter configuration publicly. This ZIP is a clean replacement project using a corrected `evaluations/` app and a new schema; it does **not** import or migrate records from the starter's `db.sqlite3`. Keep a backup of your clone and its database before switching to this project.

## Included features

- Home page, responsive sign-in, account registration, and an authenticated dashboard.
- Light/dark theme toggle; responsive sidebar; dashboard cards and a dependency-free CSS/JavaScript chart.
- Academic Form A (students), Form B (department head), Form C (peer), Form D (self-evaluation), and Form E (weighted consolidated summary).
- The 5 / 4 / 3 / 2 / 1 / 0 / N/A rating scale. N/A is excluded from means; `0` is a valid rating.
- Academic weights from the supplied material: Students 40%, Department Head 35%, Peer 15%, Self-evaluation 10%.
- Amharic **የ6 ወር የአፈፃፀም ምዘና ማጠቃለያ ቅጽ** with employee information, period, plan execution score /70, self score /5, team score /15, supervisor score /10, automatic total /100, strengths, improvement gaps, acknowledgement/disagreement, and typed signature fields.
- Filterable registers, record detail pages, browser printing, committee/head final comments, and Excel exports for academic evaluations, Form E summaries, administrative reviews, and the archive register.
- Superuser import of staff from Excel and staff/profile administration through Django Admin.
- Archive and institutional oversight register: department / college / university archive level, registry reference, forwarding destination, instructor/department copy tracking, notes, and Excel export. This records the workflow in the application; it does not physically transfer files or send emails.
- Role-aware screens and record access. Department heads and committees see their assigned department when a department is configured; College/School/Institute administration, Dean/Vice Dean, Academic Affairs Vice President/Vice Director, Archives, and concerned offices/directorates have wider oversight access. Ordinary users see their own authored records; instructors can see their own consolidated Form E summary.
- Django test cases for scoring/basic records plus a pure-Python scoring test suite.

## Quick start (VS Code on Linux)

Open this project folder (the folder containing `manage.py`) in VS Code. In the terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Application: <http://127.0.0.1:8000/>
- Django Admin: <http://127.0.0.1:8000/admin/>

If the setup says `No module named django`, make sure the `.venv` is activated, then rerun `python -m pip install -r requirements.txt`.

### Windows PowerShell alternative

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If PowerShell blocks activation, use `\.venv\Scripts\python.exe` directly for the pip/manage.py commands or activate the environment in the VS Code Python interpreter picker.

## Optional local demo users and sample staff

For a fresh local database, the following command inserts demo users and three sample staff members:

```bash
python manage.py seed_demo
```

All seeded accounts use `DemoPass2026!` as the password:

| Username | Role | Purpose |
|---|---|---|
| `demo_admin` | Superuser | Full administration and export |
| `demo_student` | Student | Form A |
| `demo_head` | Department head | Form B, administrative review and departmental oversight |
| `demo_peer` | Peer | Form C |
| `demo_instructor` | Instructor | Form D/self-evaluation |
| `demo_committee` | Committee | Departmental review and final summary comments |

**Demo credentials are for local development only. Do not seed demo accounts into a shared or production environment.** If you ran `createsuperuser` first, keep your own administrator credentials as well.

## Set roles and link staff profiles

Registration permits basic `Student evaluator` or `Instructor / staff member` accounts. Elevated roles must be assigned deliberately:

1. Sign in as a superuser and open `/admin/`.
2. Under **User profiles**, set the role (peer, department head, committee, college administration, dean, Academic Affairs VP, University/Department Archives, or Concerned Office/Directorate as appropriate).
3. For a Department Head or Committee role, set the profile's **Department** to the exact department name used in the Staff Directory. The interface restricts those roles to that department. If their department is blank, they do not get an all-university fallback.
4. Under **Instructors / staff members**, create/import staff and optionally link a staff record to the related Django account using **Linked user**. Linking is required for the self-evaluation flow to automatically constrain an instructor to their own record. The demo instructor is linked to `AU-0001`.
5. Add the correct College/Department to the user profile. College/School/Institute administration, dean, Academic Affairs, archives and concerned offices/directorates have wider oversight visibility in this local implementation. Office/Directorate accounts are read-only in the archive workflow; Archivist and designated oversight roles can create archive entries.

## Submit academic Forms A–D

Use the sidebar or Dashboard quick actions to open the form allowed for the signed-in role. Select the instructor, provide course and academic-year metadata where applicable, rate every criterion, and submit the form. The form requires one choice per criterion; choose **N/A** when an item does not apply.

- The score shown on a saved academic record is the average numeric rating out of 5.
- The weighted contribution is calculated using `average rating / 5 × form weight`.
- Form E summarizes each evaluator group using its specified weight and displays per-focus-area means.
- The provided source names “Performing non-instructional duties” in Form E but the detailed criteria for that category were not included in the supplied Form D excerpt. This implementation does not invent a separate rating list for it; the source limitation is called out on the Form E screen.
- The source provides overall weights per evaluator group but no weights inside each focus area. For that reason Form E shows focus-area averages, but only the group-level result contributes to the total.
- The uploaded role notice describes the dean/vice dean, Academic Affairs VP/Vice Director, archives, and concerned offices/directorates in the oversight workflow, but it does not include a dedicated rating rubric for evaluating a department head or dean. Those leadership/oversight roles are represented for access, reporting and archival routing; a new scored leadership form should be added only after the University supplies its approved criteria and weights.

## Submit the Amharic six-month form

Open **6-month evaluation** (department head, committee, college administration, or superuser). Select a staff member and period. Enter:

- Plan execution score: 0–70
- Employee score: 0–5
- Team score: 0–15
- Immediate supervisor score: 0–10

The system calculates `plan execution + employee + team + supervisor = total out of 100`. Scores are checked server-side. Use the performance-level selection, strengths, improvement gaps, typed supervisor/employee names, dates and agreement/disagreement explanation. Since typed signatures are not a cryptographic signature, print the form if wet signatures are required by university procedure.

## Excel import/export

### Import the staff directory

As a superuser, visit **Staff Directory → Import staff from Excel**. Use the example template at `examples/staff_import_template.xlsx`. Required first-row column headers are `employee_id` and `name`. Optional headers are `email`, `college`, `department`, `position`, `grade`, and `job_process`. Existing employee IDs are updated; blank ID/name rows are skipped.

### Export evaluation data

- **Academic evaluation records:** use filters, then **Export Excel**. Pass a form type to get that specific academic form; the workbook includes criteria response columns prefixed with the matching form, so similar category/key names across Form B and C do not collide.
- **Form E summary:** select an instructor and academic year, then export the consolidated table.
- **Administrative records:** open the administrative register and export its filtered six-month forms.
- **Archive register:** filter by academic/administrative source, archive level and search phrase; export the filtered register.

Exports use a styled Ambo-blue header, amber separator, wrapped cells, and filter/freeze-pane support. These are `.xlsx` files, not CSVs.

### Archive an evaluation

Open an academic or six-month evaluation detail page and choose **Archive record** (department heads, committee members, college administration, dean, Academic Affairs, archives or superusers). Enter the archive level, optional reference number, destination office, copy statuses and notes. Use the **Archive register** link to search/filter entries or export the register. The source materials identify the University/Department Archives and Academic Affairs Office as parts of the record-routing process; follow local official procedure for the actual transfer and retention of records.

## Testing and quality checks

With the virtual environment active:

```bash
python manage.py check
python manage.py test
python -m unittest tests.test_scoring
```

`python manage.py check` validates Django settings, model setup, URLs and templates at startup; `python manage.py test` runs Django-based tests. The pure-Python scoring tests do not need a database once the dependencies are installed. In the build environment used to assemble this ZIP, outbound GitHub/PyPI DNS failed, so Django could not be installed there and the actual Django runtime checks were not run here. Run both commands above in your VS Code virtual environment after installing the requirements.

## VS Code debugging

The `.vscode/launch.json` file includes a **Django: runserver** launch profile. Install the recommended Python and Pylance extensions, choose `.venv` as your Python interpreter, run migrations, then start the debugger.

## Project structure

```text
staff_evaluation_system/
├── manage.py
├── requirements.txt
├── config/                 # settings, URLs, ASGI and WSGI
├── evaluations/            # models, roles/access, forms, criteria, scoring, views
│   ├── migrations/         # initial schema and archive/oversight update
│   └── management/commands/seed_demo.py
├── templates/              # landing, auth, dashboard, forms, registers, reports
├── static/css/app.css      # Ambo-brand UI and light/dark themes
├── static/js/app.js        # theme, mobile navigation, chart scaling, live total
├── examples/staff_import_template.xlsx
└── .vscode/                # recommended debugger setup
```

## Color and deployment notes

The UI uses the Ambo University blue (`#0B427A`) and warm amber (`#F7BE68`) identified in a publicly listed Ambo University brand-color reference. It uses a typographic `AU` badge rather than embedding an unverified logo file. Official site: <https://ambou.edu.et/>.

This package is aimed at a local VS Code environment. Before deployment on a shared server: set a strong random `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, configure `DJANGO_ALLOWED_HOSTS`, use HTTPS, configure secure cookies and a production database, run the Django deployment checklist, and review retention, access and approval policy with the University. Do not use seeded demo credentials in production.
