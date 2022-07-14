import xlrd
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# BEGIN - configuration

TRANSACTION_NAMES = {
    'ca493af4': 'GenChallenge',
    '7ce42bfb': 'VerProof',
}

EXECUTION_TIME_ITEMS = [
    ('25%', lambda df: df.quantile(0.25)[0]),
    ('50%', lambda df: df.quantile(0.50)[0]),
    ('75%', lambda df: df.quantile(0.75)[0]),
    ('95%', lambda df: df.quantile(0.95)[0]),
    ('96%', lambda df: df.quantile(0.96)[0]),
    ('97%', lambda df: df.quantile(0.97)[0]),
    ('98%', lambda df: df.quantile(0.98)[0]),
    ('99%', lambda df: df.quantile(0.99)[0]),
    ('100%', lambda df: df.max()[0]),
    ('avg', lambda df: df.mean()[0]),
    ('std', lambda df: df.std()),
]

LATENCY_TIME_ITEMS = [
    ('0%', lambda df: df.min()[0]),
    ('20%', lambda df: df.quantile(0.20)[0]),
    ('40%', lambda df: df.quantile(0.40)[0]),
    ('60%', lambda df: df.quantile(0.60)[0]),
    ('80%', lambda df: df.quantile(0.80)[0]),
    ('100%', lambda df: df.max()[0]),
    ('avg', lambda df: df.mean()[0]),
    ('std', lambda df: df.std()),
]

# END - configuration

if __name__ == "__main__":

    # Read Excel
    workbook = xlrd.open_workbook('input.xlsx')
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])

    # print(sheet.name, sheet.nrows, sheet.ncols)
    row_name = sheet.col_values(0)
    assert str(row_name[0]) == 'filename'
    row_data_first_4_bytes = sheet.col_values(2)
    assert str(row_data_first_4_bytes[0]) == 'DataFirst4Byte'
    row_transaction_execution_times = sheet.col_values(5)
    assert str(row_transaction_execution_times[0]) == 'TransactionTime'
    row_transaction_latency_times = sheet.col_values(8)
    assert str(row_transaction_latency_times[0]) == 'TransactionLatency'

    transaction_execution_times = {sig: {} for sig in TRANSACTION_NAMES.keys()}
    transaction_latency_times = {sig: {} for sig in TRANSACTION_NAMES.keys()}

    for i in range(0, len(row_name)):
        filename = str(row_name[i])
        sig = row_data_first_4_bytes[i]

        if sig == 'DataFirst4Byte':
            # skip the table header
            continue

        if sig not in TRANSACTION_NAMES:
            print("Warning: unrecognized transaction " + row_data_first_4_bytes[i])
            continue

        if filename in transaction_execution_times[sig]:
            transaction_execution_times[sig][filename].append(int(row_transaction_execution_times[i]) / 1000000)
            transaction_latency_times[sig][filename].append(int(row_transaction_latency_times[i]) / 1000000)
        else:
            transaction_execution_times[sig][filename] = [int(row_transaction_execution_times[i]) / 1000000]
            transaction_latency_times[sig][filename] = [(int(row_transaction_latency_times[i]) / 1000000)]

    # write Excel

    workbook = xlsxwriter.Workbook('output.xlsx')

    for sig, transaction_name in TRANSACTION_NAMES.items():

        sheet = workbook.add_worksheet(transaction_name + '_execution')

        row_id = 0
        col_id = 0

        sheet.write(row_id, col_id, 'filename')
        col_id += 1

        for item in EXECUTION_TIME_ITEMS:
            sheet.write(row_id, col_id, item[0])
            col_id += 1

        for filename in sorted(transaction_execution_times[sig].keys()):
            df = pd.DataFrame(transaction_execution_times[sig][filename])
            row_id += 1
            col_id = 0
            sheet.write(row_id, col_id, filename)
            col_id += 1

            for item in EXECUTION_TIME_ITEMS:
                sheet.write(row_id, col_id, item[1](df))
                col_id += 1

        sheet = workbook.add_worksheet(transaction_name + '_latency')

        row_id = 0
        col_id = 0

        sheet.write(row_id, col_id, 'filename')
        col_id += 1

        for item in LATENCY_TIME_ITEMS:
            sheet.write(row_id, col_id, item[0])
            col_id += 1

        for filename in sorted(transaction_latency_times[sig].keys()):
            df = pd.DataFrame(transaction_latency_times[sig][filename])
            row_id += 1
            col_id = 0
            sheet.write(row_id, col_id, filename)
            col_id += 1

            for item in LATENCY_TIME_ITEMS:
                sheet.write(row_id, col_id, item[1](df))
                col_id += 1

    workbook.close()
