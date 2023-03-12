# Data-Analysts-Market-Analysis
This project aims to generate a pipeline and analysis of real data job data that was scraped in the United States market since 11/4/2022. The objective of this project is to analyze the current job market trends for Data Science. To better understand the data analyst job market, I will try to answer the following questions:
   1. What are the most sought-after skills for data analyst positions
   2. Which cties are hiring the most data analysts?
   3. Which companies are hiring the most data-analysts
   4. How do salary outcomes differ between remote-work and non-remote work?
   5. Can we predict standardized salary using a regression model if we know the skills required, schedule, & option for remote work?

## Built With
* sqlalchemy
* pandas
* seaborn
* matplotlib
* sklearn

## Methodology
In order to extract data for analysis, I ultized sql-alchemy to extract jobs, salaries, and skills tables from the Amazon RDS postgres database. After pulling these tables, I converted the tables into 3 pandas dataframe, joined them togther and saved them into a CSV file which can be accessed in /data.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
import functools as ft
from config import connection

engine = create_engine(connection)
Base = automap_base()

Base.prepare(engine, reflect=True)

jobs = Base.classes.jobs
salaries = Base.classes.salaries   
skills = Base.classes.skills

session = Session(engine)
# build queries to pull all amazon data
jobs_result = session.query(jobs)
skills_result = session.query(skills)
salaries_result = session.query(salaries)
# save into dataframes
jobs_df = pd.read_sql(jobs_result.statement, engine)
skills_df = pd.read_sql(skills_result.statement, engine)
salaries_df = pd.read_sql(salaries_result.statement, engine)

# join tables together on their primary key
# make two merges
m1 = pd.merge(salaries_df, jobs_df, how = "inner", on = ["id"])
tot_merge = pd.merge(m1, skills_df, how = "inner", on = ["id"])
# Write this joined dataframe to the data / folder
tot_merge.to_csv("data/joined_data.csv", index = False)
```
After extracting the data, I cleaned the data by filling in missing values. I transformed the daya by converting the categorical data into numerical data. I accomplished this by creating a new column for each possible skill specified in the description_tokens column. I utlized scikit-learn to perform one-hot encoding.

```python
# clean data
job_df['work_from_home'].fillna(False, inplace = True)


# hot-code encoding using scikit-learn
from sklearn.preprocessing import MultiLabelBinarizer
from ast import literal_eval

mlb = MultiLabelBinarizer()

x = job_df['description_tokens'].apply(literal_eval)

binary_columns = mlb.fit_transform(x)

enc_skill_df = job_df.join(pd.DataFrame(binary_columns, columns=mlb.classes_))

cleaned_salaries = enc_skill_df.dropna(subset=['salary_standardized'])
cleaned_salaries.to_csv('data/cleaned_data.csv')
```

After extracting, cleaning and transforming the dataset, I performed statistic tests and visualizations using seaborn, matplotlib and pandas. Visualizations and statistics can be accessed in eda.ipynb. A predictive model was created using sklearn to provide insight on the predictive power of data analyst salaries. 
## Visuals
A standard salary distribution of data analyst jobs in the United States showed a right shewed distribution. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/std_salaries_dis.png" alt="image" width="500"/>

A box plot of this distribution showed that the median salary is a 90000-100000. While the length of the whiskers are about the same, there are a significant amount of outliers.

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/std_salaries_boxplot.png" alt="image" width="500"/>

A Kolmogorov-Smirnov test resulted in a p-value less than 0.05, meaning that the distribution of salaries significantly deviates from the expected distribution. 

> KstestResult(statistic=0.0884061189073454, pvalue=1.3144684207219982e-15)

A box-plot comparing remote vs non-remote jobs showed that the median of non 'work from home' non-remote jobs is higher than remote jobs. However, the box-plot indicated a larger right whisker for remote positions than non-remote positions. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/nonremotevsremote_jobs_boxplot.png" alt="image" width="500"/>

A bar graph showed that the top skills for a data analysts were SQL, Tableau, Excel, and Python. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/ranked_skills.png" alt="image" width="500"/>

A box plot which compared jobs that listed SQL as a requirement showed that median salary is higher than jobs that did not. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/sql_salaries.png" alt="image" width="500"/>

A KS test of salaries of jobs requiring SQL resulted in a p-value less than 0.05. 

> KstestResult(statistic=0.14859694970660242, pvalue=2.428624055011534e-22)

A bar graph showed that top hiring locations were remote positions, followed by United States and Wichita, KS. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/top_loc.png" alt="image" width="500"/>

A box-plot of 3 selected comapanies showed various medians of salary of the following companies: Citi, Edward Jones, and Apex Systems. According to this box-plot, Edward Jones has the highest median pay. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/boxplotfor3companies.png" alt="image" width="500"/>

A bar graph showed that Upwork, Cox Communication and Edward Jones are the most-hiring companies. 

<img src="https://github.com/tpham16/Data-Analysts-Market-Analysis-/blob/1c311752c2102c96c86bf086f14cdf0799f8b7d6/images/top_companies.png" alt="image" width="500"/>


## Results
The visualizations of the data analyst job market provided important insight on the current skills and companies that are hiring. The most valuable skills were SQL, Tableau, and Python. According to this dataset, the most hiring cities were remote, United States, and Wichita, KS. Howeverm, this is not an accurate representation of the most hiring locations due to the scraped data collected ambiguous locations such as 'Anywhere' and 'United States'. The most hiring companies were Upwork, Cox Communications, and Edward Jones. Non-remote salaries were slightly higher than remote salaries. Using sklearn, a regression model was created to predict standardized salary based on the skills required, schedule type, and option for remote work. The results of this regression model revealed a negative R-squared value, which suggests that the model is performing poorly and is not a good fit for the data. 

## Next Actions
Based on these findings, I intend to address data quality issues. In this dataset, recruiting companies caused the data to skew toward freelance and contract-based data analyst work instead of real jobs. Additionally, missing city/location data should have been addressed to proceed with proper analysis. In order to improve the regression model, I would have to address the outliers of the data. Further analysis on entry and experienced data analyst positions such as skills and salaries could provide insight on the current job market. 


