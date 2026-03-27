# src/data_loader.py

import pandas as pd
from sqlalchemy import create_engine

def load_data():
    engine = create_engine(
        "postgresql://postgres:root@localhost:5432/creditpath_db"
    )
    
    df = pd.read_sql("SELECT * FROM loan_data", engine)
    
    # clean column names
    df.columns = df.columns.str.lower().str.strip()
    
    return df