from parent_classes.tool import Tool
import csv

class CreateCSVFromData(Tool):
    name = "create_csv_from_data"
    description = "Creates a CSV file from the provided data. The data should be a list of dictionaries, where each dictionary represents a row in the CSV file. The keys of the dictionaries will be used as the column headers."
    parameters = {
        "data": "array of objects",
        "filename": "string"
    }
    
    @staticmethod
    def run(data, filename):
        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            return {"status": "error", "message": "Data must be a list of dictionaries."}
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            with open(f"temp/{filename}", mode='w', newline='', encoding='utf-8') as csvfile:
                if data:
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            return {"status": "success", "message": f"CSV file 'temp/{filename}' created successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}