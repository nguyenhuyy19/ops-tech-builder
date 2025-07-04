import pandas as pd
import os
import json


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path, encoding='utf-8', skip_blank_lines=True)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return df


def normalize_headers(df):
    mapping = {
        'P.O.#': 'PO Number',
        'PurchaseOrder': 'PO Number',
        'PO No': 'PO Number',
        'Vendor Name': 'Vendor',
        'Supplier': 'Vendor',
        'VendorID': 'Vendor',
        'Total': 'Amount',
        'Amount ($)': 'Amount',
        'AMT': 'Amount'
    }
    df.columns = [mapping.get(str(col).strip(), str(col).strip()) for col in df.columns]
    return df


def extract_clean_records(df):
    key_fields = ['PO Number', 'Vendor', 'Amount']
    missing_fields = [field for field in key_fields if field not in df.columns]
    if missing_fields:
        raise ValueError(f"Missing required columns: {missing_fields}")

    df = df[key_fields].dropna(subset=key_fields, how='any')

    clean_records = []
    for _, row in df.iterrows():
        try:
            po_number = str(row['PO Number']).strip()
            vendor = str(row['Vendor']).strip()
            amount = round(float(row['Amount']), 2)

            if po_number and vendor and amount >= 0:
                clean_records.append({
                    "PO Number": po_number,
                    "Vendor": vendor,
                    "Amount": amount
                })
        except (ValueError, TypeError):
            continue

    return clean_records


def save_json(records, output_path):                       #optional
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def process_file(file_path, output_json_path=None):
    try:
        print(f"Processing: {file_path}")
        df = load_file(file_path)
        df = normalize_headers(df)
        records = extract_clean_records(df)
        print(f"Extracted {len(records)} records.")

        if records:
            total_amount = sum(r['Amount'] for r in records)
            unique_vendors = len(set(r['Vendor'] for r in records))
            print(f"Total amount: {total_amount}")
            print(f"Unique vendors: {unique_vendors}")

            if output_json_path:
                save_json(records, output_json_path)

        else:
            print("No valid records found.")

        return records

    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    input_path = r"C:\Users\nguyenhuy\Desktop\P_log.csv"
    output_json_path = r"C:\Users\nguyenhuy\Desktop\output_result.json"

    if os.path.exists(input_path):
        records = process_file(input_path, output_json_path)
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        print(f"File not found: {input_path}")


if __name__ == "__main__":
    main()

