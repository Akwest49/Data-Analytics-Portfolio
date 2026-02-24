# Data-Analytics-Portfolio

This repository is a **portfolio project** demonstrating my skills as a data analyst. It includes **SQL and Python** work, showing data cleaning, analysis, and visualization of real-world crime datasets.

---

## 📁 Data Sets

All CSV files are included in the `data/` folder.

- **Crime_Data_from_2020_to_Present.csv** – Crime data from Los Angeles, California, spanning 2020–2025.  
- **Crime_Codes.csv** – Key for the crime codes in the main dataset, including code, description, category, and subcategory.  
- **MO_Codes.csv** – Modus Operandi codes describing different aspects of each crime. Some crimes have multiple MO codes.

---

## 🛠 SQL

All SQL code was written and tested in **Microsoft SQL Server Management Studio (v21.6.17)**.

### Steps to run:

1. Create a new database called `Portfolio`.  
2. Import all 3 CSV files as tables with the following names:
   - `Crime_Data_Raw` → `Crime_Data_from_2020_to_Present.csv`  
   - `Crime_Codes` → `Crime_Codes.csv`  
   - `MO_Codes` → `MO_Codes.csv`  

3. Run the file `Renaming_Columns.sql` first — it renames columns in the main table for clarity.  
4. Then run `CrimeStats.sql` to explore different analyses. Instructions are included in the file.

> All files are included in this repository, so no external downloads are needed.

---

## 🐍 Python

All Python code works with the CSV files **already in the `data/` folder**. The scripts use **relative paths**, so you can clone the repo and run them without changing any directories.

### Options to run:

**Option 1: Running the Python script**

python Crime_Stats.py

**Option 2: Running the Jupyter Notebook**

1. Open `Crime_Stats.ipynb` in **Jupyter Notebook** or **Jupyter Lab**.  
2. Make sure the `data/` folder is in the same directory as the notebook (it is if you cloned the repo).  
3. Run the cells — the notebook reads all CSVs and the ZIP file automatically using relative paths.  
4. Explore analyses, charts, and outputs interactively.  

> No directory changes are needed. The notebook is ready to run immediately after cloning the repo.
