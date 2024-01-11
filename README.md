# Wisconsin Early Childhood Education (ECE) Capacity & Funding Data Explorer

## About

### OSL Data Collaboratory
This project is part of the Open Spatial Lab's 2023 Data Collaboratory. The Collaboratory is a 6-month program where OSL engages with social impact organizations to build a customized tool for data management, analysis, communication, and visualization. Engagement and feedback from Wisconsin nonprofit organizations Higher Expectations for Racine County and Milwaukee Succeeds, part of the StriveTogether network, directly informed this work. 

Based at the University of Chicago Data Science Institute, the Open Spatial Lab creates open source data tools and analytics to solve problems using geospatial data science. Read more about OSL at https://datascience.uchicago.edu/research/open-spatial-lab/. 

### Project Scope

**About**: [Higher Expectations for Racine County](https://www.higherexpectationsracinecounty.org/) engages community partners, aligns efforts, and maximizes resources to promote excellence and equity in education and employment outcomes in Racine County, WI. [Milwaukee Succeeds](https://www.milwaukeesucceeds.org/) advances education equity in Milwaukee, ensuring all children have the resources they need to succeed.

Both organizations are members of the [StriveTogether](https://www.strivetogether.org/) Cradle to Career Network. StriveTogether is a national movement with a clear purpose: helping every child succeed in school and life from cradle to career, regardless of race, zip code or circumstance. In partnership with nearly 70 communities across the country, StriveTogether provides resources, best practices and processes to give every child every chance for success. 

**Project**: OSL worked with Higher Expectations for Racine County and Milwaukee Succeeds to develop an interactive map and data tool that consolidates Wisconsin statewide early childhood education data to track policy impacts over time and across counties, zip codes, and legislative districts. Higher Expectations for Racine County and Milwaukee Succeeds will use the tool to monitor and communicate how public spending on early childhood education centers impacts accessibility of these services to Wisconsin families, particularly low-income families. 

## Repo & Data

This repo contains data used in this project, devop scripts, and page preview html files. 

`data` folder contains the following publicly available data: 
- `data/childcare centers` licensed childcare centers from the [Wisconsin Department of Children and Families Licensed Childcare Directories, 2021-2023](https://dcf.wisconsin.gov/cclicensing/lcc-directories)
- `data/community vars` community socioeconomic variables from [ACS 2021 5-year data via Social Explorer](https://www.socialexplorer.com/tables/ACS2021_5yr)
- `data/geo` spatial data boundaries.
    - WI tract and county boundaries from [US Census geo/TigerLine 2021 shapefiles](https://www2.census.gov/geo/tiger/GENZ2021/shp/
    - WI Assembly, Senate, and Congressional Districts boundaries from [2022 WI Legislative Technology Services Bureau, Geographic Information Services ](https://gis-ltsb.hub.arcgis.com/pages/download-data)
- `data/output` compressed parquet files

`scripts` contains python scripts to clean, wrangle and parse data used in this project. 


