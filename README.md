# Data-Analytics-Portfolio
This is a portfolio to show off my skills as a data analyst. Includes SQL and Python.  
It includes data cleaning, analysis, and visualization tasks designed to demonstrate practical skills in handling real-world datasets.

**Data Sets**
Crime_Data_from_2020_to_Present.csv - This is data from a government website in the US that tracked crime data in Los Angeles, California from 2020 to 2025.

Crime_Codes.csv - This is a key for the crime codes in the main data set. It includes the code, a string description of the code, the category and subcategory of the code. This table doesn't cover every single code but is what was publicly available.

MO_Codes.csv - This data set has the Modus Operandi codes, which describe different aspects of each crime listed. Some of the crimes contain multiple MO codes.

**SQL**

I wrote and ran the code in the Microsoft SQL Server Management Studio (21.6.17)

In order to run the SQL code you will need to:
1. Download 3 CSV files. 2 of them are listed here and the third can be downloaded from:
   https://drive.google.com/file/d/1QPj582YPi00Sp0MuM9nwt6YZrm0EUXYo/view?usp=drive_link
2. Create a new database titled "Portfolio"
3. All 3 files must be imported as flat files into SQL
4. The names of each table are:

Crime_Data_Raw = "Crime_Data_from_2020_to_Present.csv"

Crime_Codes = "Crime_Codes.csv"

MO_Codes = "MO_Codes.csv"

First run the file titled:  
"Renaming_Columns.sql" - This renamed some of the columns in the main table to make them easier to understand.

Then you can ran any and all parts of:  
"CrimeStats.sql" - A look at different aspects of the crime stats. There are instructions inside for what each piece does.

**Python**
There are two options for running the python code.

Option 1: Running the .py file.  
You can download the 3 csv files and then update the directory in the read.csv commands to the path where you saved the files.

Option 2: Running in Jupyter Notebook  
You can download the .ipynb and upload it to Jupyter Notebook along with the 3 csv files.


