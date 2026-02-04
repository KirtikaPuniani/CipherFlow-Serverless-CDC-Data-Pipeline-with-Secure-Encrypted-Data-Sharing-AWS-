#Idempotent CDC merge logic

import pandas as pd

def appy_cdc_merge(existing_df: pd.DataFrame, cdc_df: pd.DataFrame, pk: str):
    '''
    Applying insert, update, delete operations from cdc file to master dataframe.
    cdc_df must contain an "operation" column with values "insert", "update", "delete".
    pk is the primary key column name.
    '''
    if existing_df.empty:
        existing_df = pd.DataFrame(columns = cdc_df.columns.drop("operation"))
        
    existing_df = existing_df.set_index(pk)
    
    for _, row in cdc_df.iterrows():
        key = row[pk]
        operation = row['operation']
        
        if operation == "D":
            if key in existing_df.index:
                existing_df.drop(key, inplace=True)
        
        elif operation in ("I", "U"):
            existing_df.loc[key] = row.drop("operation")
    
    return existing_df.reset_index()