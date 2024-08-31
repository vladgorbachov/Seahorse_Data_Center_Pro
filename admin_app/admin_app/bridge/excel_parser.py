import pandas as pd
import os
from datetime import datetime


def parse_excel_file():
    file_path = r'X:\ENGINEERING DEPARTMENT\Bunkers\Bunkers.xlsx'
    sheet_name = '2024'

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found at {file_path}")

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Columns in Excel file (sheet {sheet_name}):", df.columns.tolist())

        required_columns = ['Date', 'Cap: 320.3 MGO tk SB (cub.m)', 'Cap: 1283 MGO tk PS (cub.m)',
                            'Cap: 182 FW SB (cub.m)', 'Cap: 229 FW PS (cub.m)']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing columns in Excel file: {', '.join(missing_columns)}")

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        current_date = datetime.now().date()

        # Ищем последнюю непустую строку с данными
        for index, row in df.iloc[::-1].iterrows():
            if not pd.isna(row['Date']) and not all(pd.isna(row[col]) for col in required_columns[1:]):
                matching_row = row
                date = matching_row['Date'].date() if isinstance(matching_row['Date'], pd.Timestamp) else current_date
                break
        else:
            raise ValueError("No valid data found in the Excel file")

        def safe_float(value):
            return float(value) if pd.notna(value) else 0.0

        fo_sb = safe_float(matching_row['Cap: 320.3 MGO tk SB (cub.m)'])
        fo_ps = safe_float(matching_row['Cap: 1283 MGO tk PS (cub.m)'])
        fw_sb = safe_float(matching_row['Cap: 182 FW SB (cub.m)'])
        fw_ps = safe_float(matching_row['Cap: 229 FW PS (cub.m)'])

        result = {
            'date': date.isoformat(),
            'fuel_ps_tank': f"{fo_ps:.2f}",
            'fuel_sb_tank': f"{fo_sb:.2f}",
            'fuel_total': f"{fo_ps + fo_sb:.2f}",
            'water_ps_tank': f"{fw_ps:.2f}",
            'water_sb_tank': f"{fw_sb:.2f}",
            'water_total': f"{fw_ps + fw_sb:.2f}"
        }
        print("Parsed data:", result)
        return result

    except pd.errors.EmptyDataError:
        print(f"The sheet '{sheet_name}' is empty.")
        return None
    except KeyError as e:
        print(f"Error: Column not found - {str(e)}")
        return None
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error parsing Excel file: {str(e)}")
        return None