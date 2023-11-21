from datetime import datetime
import pytest

from most_active_cookie.active_cookie_extractor import ActiveCookieExtractor
from most_active_cookie.utils import parse_csv

@pytest.mark.parametrize('file_path,target_date',
[('../resources/wrong_csv_header_case.csv', '2018-12-08')])
def test_wrong_timestamp(
    file_path,
    target_date
):
    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    cookie_list = parse_csv(file_path)
    active_cookie = ActiveCookieExtractor(cookie_list, target_date).extract_active_cookies()
    assert set(active_cookie) == set([])
