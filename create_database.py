import csv
import glob
import os
import sqlite3

# Connect to SQLite3 database.
conn = sqlite3.connect('salaries.sqlite')
conn.text_factory = str  # allows utf-8 data to be stored

# Get full path to current directory.
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get a path for a folder with .csv files.
data_folder = os.path.join(current_dir, 'data')

# Create a cursor.
c = conn.cursor()

# Iterate through all csv files.

for csvfile in glob.glob(os.path.join(data_folder, '*.csv')):
    # Get a table name equals to file name without extension.
    tablename = os.path.splitext(os.path.basename(csvfile))[0]
    tablename = tablename.replace('-', '_')

    with open(csvfile, "r") as f:
        reader = csv.reader(f)
 
        header = True
        for row in reader:
            if header:
                # Gather column names from the first row of the csv.
                header = False
 
                sql = "DROP TABLE IF EXISTS %s" % tablename
                c.execute(sql)

                sql = "CREATE TABLE {} (".format(tablename)
                for column in row:
                    # Replace spaces and dashes in column names.
                    column = column.lower().replace('-', '_').replace(' ', '_')
                    if column.endswith('salary'):
                        sql += '{} REAL, '.format(column)
                    else:
                        sql += '{} TEXT, '.format(column)
                # This is a workaround to remove the latest comma and complete the query.
                sql = sql[:-2] + ")"

                c.execute(sql)
 
                for column in row:
                    if column.lower().endswith("_id"):
                        index = "%s__%s" % (tablename, column)
                        sql = "CREATE INDEX %s on %s (%s)" % (index, tablename, column)
                        c.execute(sql)
 
                insertsql = "INSERT INTO %s VALUES (%s)" % (
                    tablename,
                    ", ".join(["?" for column in row])
                )
 
                rowlen = len(row)
            else:
                # Skip lines that don't have the right number of columns.
                if len(row) == rowlen:
                    data = []
                    # Make REAL-type values from dollars.
                    for element in row:
                        item = element.replace('$', '').replace(',', '')
                        try:
                            item = float(item)
                        except ValueError:
                            # String has been found.
                            pass
                        data.append(item)
                    c.execute(insertsql, data)
 
        conn.commit()

c.close()
conn.close()
