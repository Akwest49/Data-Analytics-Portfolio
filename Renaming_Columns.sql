--Look at the table to see what we can clean up - started with column names
SELECT
TOP 100
*
FROM Portfolio.dbo.Crime_Data_Raw

--Cleaned up column names to make the data a bit more understandable
EXEC sp_rename 
  'dbo.Crime_Data_Raw.Rpt_Dist_No',
  'District_No',
  'COLUMN';

EXEC sp_rename 
  'dbo.Crime_Data_Raw.Crm_Cd',
  'Crime_Code',
  'COLUMN';

EXEC sp_rename 
  'dbo.Crime_Data_Raw.Crm_Cd_Desc',
  'Crime_Code_Desc',
  'COLUMN';


EXEC sp_rename 
  'dbo.Crime_Data_Raw.Mocodes',
  'MO_Codes',
  'COLUMN';

EXEC sp_rename 
  'dbo.Crime_Data_Raw.Premis_Cd',
  'Premisis_Code',
  'COLUMN';

EXEC sp_rename 
  'dbo.Crime_Data_Raw.Premis_Desc',
  'Premisis_Desc',
  'COLUMN';

EXEC sp_rename 
  'dbo.Crime_Data_Raw.Weapon_Used_Cd',
  'Weapon_Code',
  'COLUMN';

