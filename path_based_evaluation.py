import pandas as pd
import re
import json
from datetime import datetime

def load_path_sets(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def evaluate_model_response(root_cause, target_node, path_sets, top_n=3):


    path_scores = [(path, abs(path.index(root_cause) - path.index(target_node)))
                   for path in path_sets if root_cause in path and target_node in path]
    path_scores.sort(key=lambda x: x[1])  # Sort by closeness between nodes

    top_paths = {f"Top {i+1} Path": x[0] for i, x in enumerate(path_scores[:top_n])}

    

    return top_paths
	
def process_csv_data(file_path,path_sets, top_n=3):
    

    data = pd.read_csv(file_path, encoding='ISO-8859-1')        
    results = []

    for _, row in data.iterrows():
        print(row)
        root_node=row["Root Node"]
        target_node=row["Target Node"]
        valid_paths = evaluate_model_response(root_node,target_node,path_sets, top_n)
        print(valid_paths)
        result_row = {
            **valid_paths  # Unpack top paths directly into the row
        }
        results.append(result_row)

    return pd.DataFrame(results)

# Usage Example
path_sets = load_path_sets(r'C:\Users\Dell\Downloads\path_sets.json')
file_path = r"C:\Users\Dell\Desktop\RCA\Training_RAG_Focused_Strict_evaluation.csv"
processed_data = process_csv_data(file_path, path_sets, top_n=3)  # Adjust top_n as needed

# Generating a timestamped filename for output
output_file_path = f"mixtral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
processed_data.to_csv(output_file_path, index=False)
print(f"Data saved to {output_file_path}")