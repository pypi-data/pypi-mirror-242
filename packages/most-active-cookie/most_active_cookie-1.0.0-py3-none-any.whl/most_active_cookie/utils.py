import csv
from datetime import datetime


def parse_csv(csv_file):
    """
    Parse csv files and return list of (cookie, date) 
    :param csv_file: the path for csv file
    :return: list of (cookie, date)
    """
    with open(csv_file, 'r', encoding='utf-8') as csv_result:
        cookie_row = csv.DictReader(csv_result)

        headers = cookie_row.fieldnames
        # If headers do not exist properly, we will not process the file and return empty
        if headers != ['Cookie', 'Timestamp']:
            return []

        #sample file reading logic
        cookie_date_list = refine_cookie_row(list(cookie_row))
        return cookie_date_list


def refine_cookie_row(cookie_row):
    """
    Iterate through rows of csv and append to list of (cookie date).
    Will not include row with inappropriate timestamp
    :param cookie_row: the row of csv files 
    :return: list of (cookie, date)
    """
    cookie_date_list = []

    for cookie_log in cookie_row:
        cookie = cookie_log.get('Cookie')
        timestamp = cookie_log.get('Timestamp')

        if cookie and timestamp:
            try:
                # Parse timestamp using datetime
                # If we do not use datetime, we can simply just parse based on "T"
                date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z").date()
                cookie_date_list.append((cookie, date))
            except ValueError:
                # Skip invalid timestamp entries
                pass

    return cookie_date_list
