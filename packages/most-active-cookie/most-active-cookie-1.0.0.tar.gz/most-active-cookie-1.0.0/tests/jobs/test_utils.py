from datetime import datetime
import pytest

from most_active_cookie.utils import parse_csv, refine_cookie_row


@pytest.mark.parametrize('file_path',
[('../resources/csv_parsing_cookie_case.csv')])
def test_parse_csv(
    file_path
):
    cookie_list = parse_csv(file_path)
    assert cookie_list == [('AtY0laUfhglK3lC7', datetime.strptime('2018-12-09', '%Y-%m-%d').date())]

@pytest.mark.parametrize('cookie_row',
[([{'Cookie': 'AtY0laUfhglK3lC7', 'Timestamp': '2018-12-09T14:21:00+00:00'}])])
def test_refine_cookie_row(
    cookie_row
):
    cookie_list = refine_cookie_row(cookie_row)
    assert cookie_list == [('AtY0laUfhglK3lC7', datetime.strptime('2018-12-09', '%Y-%m-%d').date())]
