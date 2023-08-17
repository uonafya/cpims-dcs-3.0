import sys
import csv
import simplejson
from os.path import dirname


try:
    script, input_file_name, model_name = sys.argv
except ValueError:
    print("\nRun via:\n\n%s input_file_name model_name" % sys.argv[0])
    print("\ne.g. %s airport.csv app_airport.Airport" % sys.argv[0])
    print("\nNote: input_file_name should be a path relative this script.")
    sys.exit()

in_file = dirname(__file__) + '/' + input_file_name
out_file = dirname(__file__) + '/' + input_file_name + ".json"

print("Converting %s from CSV to JSON as %s" % (in_file, out_file))

f = open(in_file, 'r')
fo = open(out_file, 'w')

reader = csv.reader(f)

header_row = []
entries = []


for row in reader:
    if not header_row:
        header_row = row
        continue

    pk = row[0]
    model = model_name
    fields = {}
    for i in range(len(row) - 1):
        active_field = row[i + 1]

        # convert numeric strings into actual numbers by
        # converting to either int or float
        if active_field.isdigit():
            try:
                new_number = int(active_field)
            except ValueError:
                new_number = float(active_field)
            fields[header_row[i + 1]] = new_number
        else:
            afield = active_field.strip()
            afield = True if afield == 'TRUE' else afield
            afield = False if afield == 'FALSE' else afield
            fields[header_row[i + 1]] = afield

    row_dict = {}
    row_dict["pk"] = int(pk)
    row_dict["model"] = model_name

    row_dict["fields"] = fields
    entries.append(row_dict)

fo.write("%s" % simplejson.dumps(entries, indent=4))

f.close()
fo.close()
