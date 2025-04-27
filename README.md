# covid_dashboard

OU IB3502-242533B Python Opdracht 2.0 

Update: 2025-04-27_004

The main program (Main) is Covid_Dashboard.IPynb. Three tabs are displayed here:
 1. Corona
 2. Heatmap
 3. Sewage water

The three tabs have the following functionality:

1. Corona:
The original assignment with Corona overviews.
 1. Selection by year
 2. Selection Total Reported, Hospital Admission and Deceased. This option can be selected combined
 3. Level: Netherlands, all provinces and per Povincie.
 4. For the provinces it is possible to select on Municipalities of Months.
 5. Charts are shown based on the selections via the Covid_Dashbord_presenter module.

2. Heatmap:
The first addition to the original assignment. Here too it is about direct Corona effects.
 1. Selection by year
 2. Selection on: Total Reported, Hospital Admission of Deceased.
 3. Selection on Provincis or Municipalities
 4. The output is a heat map of the Netherlands based on the selections via the Covid_Dashbord_presenter module.


3. Sewage:
The second addition to the original assignment. This is about measured Corona pollution in the sewage water.
 1. Selection on year.
 3. Selection on Provincis or Municipalities
 4. The output is a heat map of the Netherlands based on the selections via the Covid_Dashbord_presenter module.


This project consists of the following modules:

 1. Covid_Dashbord_presenter.py
 2. Data_service.py
 3. Data_loader.py
 4. Dataphrame_cleaner.py
 5. Dataphrame_combiner.py

These five modules together have a clear and separate responsibility.

1. Covid_dashboard_presenter.py
 - Visualizes data through graphs.
 - Uses data_service to collect data.
 - Type: Presentation layer (UI).

2. Data_service.py
 - Connect Loader, Cleaner and Combiner.
 - Provides a complete data set for visualization.
 - Type: orchestration layer (logic).

3. Data_loader.py
 - Reads CSV files of infections and hospital admissions and sewage water infections.
 - Type: Extract layer.

4. Dataphrame_cleaner.py
 - filters and normalizes rough data rames.
 - Type: Transform layer.

5. Dataphrame_combiner.py
 - Combines cleaned data frames on common columns.
 - Type: Merge layer.

Coherence:
Each layer is linked separately and fulfills a single responsibility. This makes the whole maintainable, expandable and testable.


---

### 🤖 About AI assistance in this project

This project was partly created with the help of AI assistance, under human direction.
The code has been generated, optimized and structured on the basis of clear guidelines, experience and project context.

AI has been used here as a tool to accelerate repetitive tasks, to provide points for improvement and to guarantee consistency.
The human factor - in particular the interpretation of context, control over choices and moral considerations - remained leading in the process.



---

### 🧪 Jupyter-notebooks use in this project

Because the code is structured as a Python Package (with `SRC/`), you must first add the correct path for imports in notebooks.
Add this at the start of every notebook that uses `From SRC ...`

`` Python
Import SYS
From Pathlib Import Path
sys.path.Apend (str (path (). Resolve (). Parent / "SRC"))
`` `

The Snap-it notebook already contains this as the first cell.


---

### 🛠 Installation instruction for package support (optional, recommended for developers)

If you unpack this folder on a new environment and work with Jupyter-notebooks, then perform the following in a terminal in the main folder:

`` Bash
PIP install -e.
`` `

This ensures that Python knows where the `SRC/` modules are and that `From SRC ...` works in notebooks.

📁 You can then use the notebooks immediately, without extra configuration. Large datas sets remain locally; No extra upload is required.
