from datetime import datetime

def convert_date(date_string):
    # Parse the input date string using the specified format
    date_object = datetime.strptime(date_string, "%d-%b-%Y")

    # Convert the date object to the desired format "yyyy-mm-dd"
    converted_date = date_object.strftime("%Y-%m-%d")

    return converted_date
