
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# from config import connection

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5434/epi')
 
Base = automap_base()

Base.prepare(engine, reflect=True)

jobs = Base.classes.jobs
salaries = Base.classes.salaries
skills = Base.classes.skills

session = Session(engine)