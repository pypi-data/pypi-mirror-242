import json
import pandas as pd


def mask_column_with_function(pd_column, function):
    exec(function, globals())
    masked_column = pd_column.apply(maskInfo)
    return masked_column

def masking_all_column(masked_encrypted_csv_path,final_masked_and_encrypted_location,json_path):
    
    with open(json_path, 'r') as json_file:
        init_result =  json.load(json_file)
    makeddata = pd.read_csv(masked_encrypted_csv_path, low_memory=False)
    for col_info in init_result['content']:
            col_name = col_info['columnName']
            if col_info.get('sensitivity') == 1:
                # masked_df[col_name] = makeddata[col_name]
                print(f"Applying masking to sensitive column: {col_name}...")
                makeddata[col_name] = mask_column_with_function(makeddata[col_name], col_info['function'])            
            else:
                print(f"Skipping non-sensitive column: {col_name}")
                makeddata[col_name]
                
    saving_masked_data = final_masked_and_encrypted_location
    makeddata.to_csv(saving_masked_data, index=False)

