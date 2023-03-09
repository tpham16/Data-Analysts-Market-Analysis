from sqlalchemy import create_engine, func
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
engine.dispose()

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