--We are working with Crime Data from California for this example
--The first step was to take a look at our tables

--This table contains the main body of data: all incidents of crime
SELECT *
FROM [Portfolio].dbo.Crime_Data_Raw
ORDER BY DR_NO

/* This table shows us the Crime Codes and their meaning
There are also categories and subcategories for these crimes so we can
break down the data for better statistical analysis */ 
SELECT *
FROM [Portfolio].dbo.Crime_Codes

/*This final table has a list of MO (Modus Operandi) codes and their corresponding
meanings. Once again we have a new dyanmic from which to look at the data and understand.*/
SELECT *
FROM [Portfolio].dbo.MO_Codes

--Now let's verify the range of dates here
SELECT
MAX(Date_Rptd),
MIN(Date_Rptd)
FROM [Portfolio].dbo.Crime_Data_Raw
--The oldest date is Jan 2020 and the latest is July 2025 - This gives us a 5 year span
--The dates are formatted as YYYY/MM/DD

--Let's start with the simplest question: How much crime was committed in each year
SELECT
YEAR(Date_Rptd) AS 'Year',
COUNT(*) AS 'Crime Count'
FROM [Portfolio].dbo.Crime_Data_Raw
GROUP BY YEAR(Date_Rptd)
ORDER BY YEAR(Date_Rptd)
--We can see from the results that the crime data for 2025 is incomplete
--We also see that the crime increased from 2020 to 2023 but sharply declined in 2024

--For the next few data sets let's take a look at the breakdown in types of crime and location within California.
--Then we will add back in the element of time.

SELECT
Crime_Code AS 'Crime Code',
COUNT(*) AS 'Crime Count'
FROM [Portfolio].dbo.Crime_Data_Raw
GROUP BY Crime_Code
ORDER BY COUNT(*) DESC

--This information shows us the number of crimes, but let's add in some more details
--First let's turn our original code into a CTE (removing the order by of course)

WITH CrimeCodeCount
AS (
	SELECT
	Crime_Code AS 'Crime Code',
	COUNT(*) AS 'Crime Count'
	FROM [Portfolio].dbo.Crime_Data_Raw
	GROUP BY Crime_Code
)
--Now we can join the information from our Crime Code table to understand the most prominent crimes
SELECT
CCC.[Crime Code],
C_C.Description,
C_C.Category,
C_C.Subcategory,
CCC.[Crime Count]
FROM CrimeCodeCount AS CCC
JOIN [Portfolio].dbo.Crime_Codes AS C_C
ON CCC.[Crime Code] = C_C.Code
ORDER BY CCC.[Crime Count] DESC

--Now let's try a more complex querry and look at the victims of these crimes
--We are going to start by putting all the ages into "buckets"
WITH AgeGroups
AS
(
	SELECT
	Vict_Age AS 'Age',
	CASE
		WHEN Vict_Age > 1 AND Vict_Age < 17 THEN 'Adolescent'
		WHEN Vict_Age > 17 AND Vict_Age < 21 THEN 'Young Adult'
		WHEN Vict_Age > 21 AND Vict_Age < 60 THEN 'Adult'
		WHEN Vict_Age > 60 THEN 'Senior'
		ELSE 'No Age Data'
	END AS 'Vict_Age_Groups',
	AREA_NAME AS 'Location',
	Vict_Sex AS 'Gender'
	FROM [Portfolio].dbo.Crime_Data_Raw
)
--Now let's see the breakdown by City, Gender and Age
SELECT
[Location],
[Gender],
[Vict_Age_Groups],
COUNT(*) AS 'Crime Count'
FROM AgeGroups
WHERE ([Gender] = 'M' OR [Gender] = 'F') AND [Vict_Age_Groups] <> 'No Age Data'
--We want the data clean and easy to read so we limited to Men, Women and Data where we knew the age
GROUP BY [Location], [Gender], [Vict_Age_Groups]
ORDER BY [Location], [Gender], [Crime Count] desc

/* This code is great because we can swap in and out any of our variables to see
the different data sets and any combination of them
(Crimes by location, crimes by gender victim, crimes by age, etc...)

Let's copy and paste and try another variation. */

CREATE VIEW dbo.RankedGroups
AS
	WITH AgeGroups_Ranked
	AS
	(
		SELECT
		Vict_Age AS 'Age',
		CASE
			WHEN Vict_Age > 1 AND Vict_Age < 17 THEN 'Adolescent'
			WHEN Vict_Age > 17 AND Vict_Age < 21 THEN 'Young Adult'
			WHEN Vict_Age > 21 AND Vict_Age < 60 THEN 'Adult'
			WHEN Vict_Age > 60 THEN 'Senior'
			ELSE 'No Age Data'
		END AS 'Vict_Age_Groups',
		AREA_NAME AS 'Location',
		Vict_Sex AS 'Gender'
		FROM [Portfolio].dbo.Crime_Data_Raw
	)
	SELECT
	DENSE_RANK() OVER(PARTITION BY [Location], [Gender] ORDER BY COUNT(*) DESC) AS DRank,
	[Location],
	[Gender],
	[Vict_Age_Groups],
	COUNT(*) AS 'Crime Count'
	FROM AgeGroups_Ranked
	WHERE ([Gender] = 'M' OR [Gender] = 'F') AND ([Vict_Age_Groups] <> 'No Age Data')
	GROUP BY [Location], [Gender], [Vict_Age_Groups]

--In this variation we added in a rank to the original data
--Now we can filter out the top 2 victim age groups per gender and city
--I also added a total victims by gender at the bottom

SELECT
*
FROM Portfolio.dbo.RankedGroups
WHERE DRank in('1','2')

UNION ALL

SELECT
NULL,
'Total Victims by Gender',
Gender,
' ',
SUM([Crime Count])
FROM Portfolio.dbo.RankedGroups
GROUP BY Gender

--Thankfully children are not the main victims of crime in any city
--There were also aproximately 15k more crimes against men (this sum includes all age groups)

/* Time for a new challenge, in our original database the MO codes are all 
listed in a single cell. So in order to understand the codes and the frequencies we 
need to split them into multiple rows.

We also need to add in the DR_NO so we don't lose how many crimes were committed vs instances 
of each MO. Unfortunately, we need to remove the "NULL" DR_NO data, as we cannot add in new
ID numbers.
*/

SELECT
DR_NO,
CR.value AS MO
FROM Portfolio.dbo.Crime_Data_Raw
CROSS APPLY STRING_SPLIT(MO_Codes, ' ') CR 
WHERE CR.value <> ' ' AND DR_NO is not null
ORDER BY DR_NO

--Let's save this as a view for future use
USE Portfolio --best practice so as not to create in the wrong database by accident
GO

CREATE VIEW dbo.Split_MO
AS
(
	SELECT
	DR_NO,
	CR.value AS MO
	FROM Portfolio.dbo.Crime_Data_Raw
	CROSS APPLY STRING_SPLIT(MO_Codes, ' ') CR 
	WHERE CR.value <> ' ' AND DR_NO is not null
)

--Now we can look at our data in aggregate
SELECT
SpMO.MO,
MOCo.MO_Description,
COUNT(MO) AS 'MO Count'
FROM Portfolio.dbo.Split_MO SpMO
JOIN Portfolio.dbo.MO_Codes MOCo
ON SpMO.MO = MOCo.MO_Code
GROUP BY SpMO.MO, MOCo.MO_Description
ORDER BY COUNT(MO) DESC

--This data tells us how many times each MO appeared in a crime
--Lucky for California there was only one instance of "Biological Agent"