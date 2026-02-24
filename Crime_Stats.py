# This file is meant to showcase visualizations based on the SQL files that belong to this portfolio.
# You can run this file with the 3 CSV files on Github. While it is meant to compliment the SQL file, you can see most of the same data in this file alone.


#importing all the libraries we may need
import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as pplot
import matplotlib.ticker as mticker

#adding a few mods to make the read_csv generic
import os
import zipfile #one file is too large for github and had to be zipped

# Get the path of the current script
script_dir = os.path.dirname(__file__)

# Paths to CSV files in the portfolio
crime_codes_path = os.path.join(script_dir, "data", "Crime_Codes.csv")
mo_codes_path = os.path.join(script_dir, "data", "MO_Codes.csv")
zip_path = os.path.join(script_dir, "data", "Crime_Data_from_2020_to_Present.zip")

# Read CSVs
CCodes = pd.read_csv(crime_codes_path)
MOCodes = pd.read_csv(mo_codes_path)

# Read CSV from ZIP
with zipfile.ZipFile(zip_path, 'r') as z:
    print("Files in ZIP:", z.namelist())
    with z.open(z.namelist()[0]) as f:  # read the first CSV inside the ZIP
        CStats = pd.read_csv(f)

#A quick cleaning tool
CStats.columns = CStats.columns.str.strip().str.replace(' ', '_')
CCodes.columns = CCodes.columns.str.strip().str.replace(' ', '_')
MOCodes.columns = MOCodes.columns.str.strip().str.replace(' ', '_')


# The first thing we need to do is replicate the SQL file where we cleaned up the names of the columns.


CStats.rename(columns={'Rpt_Dist_No': 'District_No'}, inplace=True)

CStats.rename(columns={'Crm_Cd': 'Crime_Code'}, inplace=True)

CStats.rename(columns={'Crm_Cd_Desc': 'Crime_Code_Desc'}, inplace=True)

CStats.rename(columns={'Mocodes': 'MO_Codes'}, inplace=True)

CStats.rename(columns={'Premis_Cd': 'Premisis_Code'}, inplace=True)

CStats.rename(columns={'Premis_Desc': 'Premisis_Desc'}, inplace=True)

CStats.rename(columns={'Weapon_Used_Cd': 'Weapon_Code'}, inplace=True)


# Let's verify the new names


CStats.columns.tolist()


# Now we can take a look at the DFs


CStats

MOCodes

CCodes


# Everything looks good, but we need to verify that the column types are correct.


CStats.info()


# We now see that the dates were not recognized so we need to fix this manually.

CStats['Date_Rptd'] = pd.to_datetime(CStats['Date_Rptd'], format='%m/%d/%Y %I:%M:%S %p')
CStats['DATE_OCC'] = pd.to_datetime(CStats['DATE_OCC'], format='%m/%d/%Y %I:%M:%S %p')
CStats['TIME_OCC'] = pd.to_datetime(
    CStats['TIME_OCC'].astype(str).str.zfill(4),
    format='%H%M').dt.time
CStats.info()

CStats


#  Perfect! Now we can create some visualizations based on the SQL data we created.
#  First thing is Crimes by Year

#First we can add a year column
CStats['OCC_Year'] = CStats['DATE_OCC'].dt.year

#Now we count the occurences and store them in a DF for the chart
crimes_per_year = CStats['OCC_Year'].value_counts().sort_index()

crimes_per_year = crimes_per_year.iloc[:-1]  # drops 2025, the data is incomplete

#In this cell we will plot our chart
#I ran the chart a few times and each time added a new parameter to make it look nicer
#In this cell we will plot our chart
pplot.figure(figsize=(10,6))

colors = sb.color_palette("bright", len(crimes_per_year))  # one color per year

# Use matplotlib directly instead of seaborn for the bars
pplot.bar(x=crimes_per_year.index, height=crimes_per_year.values, color=colors)

pplot.xlabel('Year', labelpad=10, fontsize=15)
pplot.ylabel('Number of Crimes', labelpad=10, fontsize=15)
pplot.title('Number of Crimes per Year', fontsize=30)
pplot.xticks(rotation=45)
pplot.gca().yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}k')
)
pplot.show()


# The crime data here is easy to see now. Crimes in California increased from 2020 to 2022. There was a small dropoff in 2023 and then a severe drop in 2024. 
#  Now let's take a look at the types of crimes committed

#The first thing we need to do is a merge (Python's version of a Join)
Merged_Codes = CStats.merge(CCodes, left_on = 'Crime_Code', right_on = 'Code', how = 'left')
Merged_Codes
#If you scroll to the end you can see the added info


#Now we need to count the crime codes - the list provided for us seems to be incomplete so we will only look at named codes
Code_Count = Merged_Codes['Code'].value_counts().head(10).reset_index()
Code_Count.columns = ['Crime_Code','Instances']
Code_Count = Code_Count.merge(CCodes[['Code', 'Description', 'Category']], left_on = 'Crime_Code', right_on = 'Code', how = 'left')


#Here we chart
pplot.figure(figsize=(12,6))
sb.barplot(
    data=Code_Count,
    x='Description',
    y='Instances',
    hue='Category',   # assigns colors by Category
    dodge=False        # so bars are stacked by category color (not side by side)
)
pplot.xlabel('Crime Committed',labelpad=10, fontsize=15)
pplot.ylabel('Instances',labelpad=10, fontsize=15)
pplot.title('Top 10 Crimes by Count with Category', fontsize=30)
pplot.xticks(rotation=45, ha='right')
pplot.legend(title='Category')
pplot.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}k'))
pplot.show()


#  What can we learn from this chart?
#  Most of the crime is theft, with Auto thefts being the most by a longshot.
#  However, there are a few violent crimes here as well.

#  The next section takes a deeper look into demographics.

#First we recreate the buckets like we had in SQL
age_bins = [1, 18, 22, 60, np.inf]
age_labels = ['Adolescent', 'Young Adult', 'Adult', 'Senior']

#Now we can create a column for them in our DF
CStats['age_group'] = pd.cut(CStats['Vict_Age'], bins = age_bins, labels = age_labels, right = False)

#We are also only interested in Male and Female data, to keep things simple
BGender = CStats[CStats['Vict_Sex'].isin(['M','F'])]
BGender = BGender[BGender['age_group'].notna()]

#Now we can create a DF that groups everything for us
demog_crime = (BGender.groupby(['AREA_NAME', 'Vict_Sex', 'age_group'], observed=True).size().reset_index(name='Incidents'))
#And let's take a look
demog_crime

#This chart can tell us a lot but it's a little messy
#Let's try a pivot table and make it a little easier to read
demog_pivot = demog_crime.pivot_table(
    index = ['AREA_NAME','age_group'],
    columns = ['Vict_Sex'],
    values = ['Incidents'],
    fill_value = 'N/A',
    observed=True
)
demog_pivot


#Ok, so the data is nice to read but not visually appealing.
#Let's make a chart

#For the chart to be readable we need to cut down the num of locations - how about a top 5?
top5_locations = BGender['AREA_NAME'].value_counts().nlargest(5).index
top5_locations


#Now that we have our locations let's store all the data for those places in a new DF for our chart
top5_stats = BGender[BGender['AREA_NAME'].isin(top5_locations)]

#Now we can run the group by and then the pivot
top5_demog = (
    top5_stats.groupby(['AREA_NAME', 'Vict_Sex', 'age_group'], observed=True).size().reset_index(name='Incidents') )

#Now we add a column with percentages of crime in that area per age group
top5_demog['percent'] = (
    top5_demog.groupby(['AREA_NAME', 'Vict_Sex'])['Incidents'].transform(lambda x: x / x.sum() * 100) )

#Now we pivot the data and then generate the chart
top5_pivot = top5_demog.pivot_table(
    index=['AREA_NAME', 'Vict_Sex'],
    columns='age_group',
    values='percent',
    fill_value=0,
    observed=True
)


#Now we need to make the chart
pplot.figure(figsize=(20, 8))

top5_pivot.plot(kind='bar', stacked=True, colormap='viridis', width=0.85)
pplot.legend(
    title='Age Groups',
    bbox_to_anchor=(1.02, 1),
    loc='upper left'
)
pplot.xlabel('Location and Gender', fontsize=12, labelpad=10)
pplot.ylabel('Percentage of Crimes by Age Group', fontsize=12, labelpad=10)

pplot.xticks(rotation=45, ha='right', fontsize=10)
pplot.tight_layout()

text_color ='#D35400'

ax = pplot.gca()
for container in ax.containers:
    for rect in container:
        height = rect.get_height()
        if height > 4:
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                rect.get_y() + height / 2,
                f'{height:.1f}%',
                ha='center',
                va='center',
                fontsize=7,
                color=text_color,
                fontweight='bold'
            )
pplot.show()

# The overwhelming majority of crime is committed against adults (which makes sense as the age range is the greatest for adults)
# There is also a relatively even distribution across the different locations.
