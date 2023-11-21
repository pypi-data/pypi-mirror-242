"""most_active_cookie module supports extracting most active cookie in target date."""

from datetime import datetime
import os
import click

from most_active_cookie.utils import parse_csv
from most_active_cookie.active_cookie_extractor import ActiveCookieExtractor


@click.command()
@click.argument('file_path')
@click.option('-d', '--date', help='Insert Your Date.')
def cli(file_path, date):
    """
    cli function to support command line interface
    :param file_path: path of csv file
    :date: target date to find active cookie
    """
    # detect cases when csv is not provided
    if os.path.splitext(file_path)[-1].lower() != ".csv":
        click.echo('You should provide appropriate csv file')
    # detect cases when target date is not properly provided
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        click.echo('Please provide date with appropriate date format Y-m-d')
    cookie_list = parse_csv(file_path)
    active_cookie = ActiveCookieExtractor(cookie_list, target_date).extract_active_cookies()
    # print response based on the result
    if not active_cookie:
        click.echo('No cookie found in given date')
    for cookie in active_cookie:
        click.echo(cookie)
