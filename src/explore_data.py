import pandas as pd
import os
import json

def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    
    analysis = {
        "filename": os.path.basename(file_path),
        "shape": df.shape,
        "columns": [
            {"name": col, "type": str(dtype), "missing": int(df[col].isna().sum())}
            for col, dtype in df.dtypes.items()
        ],
        "head": df.head(5).to_dict(orient="records")
    }
    return analysis

def main():
    data_dir = "data/raw/"
    files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    results = []
    
    for file in files:
        file_path = os.path.join(data_dir, file)
        print(f"Analyse de {file}...")
        results.append(analyze_csv(file_path))
        
    with open("outputs/analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("Analyse terminée. Résultats sauvegardés dans outputs/analysis_results.json")

if __name__ == "__main__":
    main()
