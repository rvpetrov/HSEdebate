from oauth2client.service_account import ServiceAccountCredentials
from gspread import authorize, Worksheet
from mysql import connector
from os.path import dirname

regs_url = "YOUR-GOOGLE-SHEET-LINK"
rooms_url = "YOUR-GOOGLE-SHEET-LINK"
stats_url = "YOUR-GOOGLE-SHEET-LINK"

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", "https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=(dirname(__file__) + "/creds.json"), scopes=scope)
client = authorize(credentials)

conn = connector.connect(
    host="127.0.0.1",
    port=0,
    user="YOUR-MYSQL-USER",
    database="YOUR-MYSQL-DATABASE",
    password="YOUR-MYSQL-PASSWORD"
)
cur = conn.cursor()


def __connect_to_sheet__(url: str, *, __is_for_stat: None | str = None) -> Worksheet:
    spreadsheet = client.open_by_url(url=url)
    if __is_for_stat is None:
        worksheet = spreadsheet.get_worksheet(0)
    else:
        worksheet = spreadsheet.get_worksheet(0) if __is_for_stat == "speaks" else spreadsheet.get_worksheet(1)
    return worksheet
