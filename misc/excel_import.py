from datetime import datetime

import pandas as pd
import openpyxl
from db.source import SourceScraper
from misc.models import ExcelImportStats


def load_excel_to_db(filename: str):
    df = pd.read_excel(filename, usecols=[0])
    file_data = df.iloc[:, 0].values.tolist()
    positions = []
    for element in file_data:
        if str(element).isdigit():
            positions.append(int(element))
    now = datetime.now()
    source_db = SourceScraper(table_name='oreht_positions')
    for position in positions:
        source_db.insert_into_source_table(position, now)
    inserted_count = source_db.insert_count_by_date(now)
    positions_count = len(positions)
    from_file_count = len(file_data)
    source_db.close_connection()
    return ExcelImportStats(inserted_count=inserted_count, positions_count=positions_count, from_file_count=from_file_count)