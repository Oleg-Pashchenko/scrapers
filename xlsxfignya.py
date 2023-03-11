a = """

"""
a = a.split('\n')
res = []
for i in a:
    i = i.strip()
    if i.isdigit():
        res.append(i)
import pandas as pd
df = pd.DataFrame(res)

# Create an Excel writer using pandas
writer = pd.ExcelWriter('output.xlsx')

# Write the DataFrame to a sheet named 'Sheet1'
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Save the Excel file
writer.save()