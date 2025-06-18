import pyodbc
def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=10.96.16.13;'
        'DATABASE=BOT_AUTOTRADING;'
        'UID=hiennq;'
        'PWD=OCB@hien32112;'
        'TrustServerCertificate=yes;'
        'Encrypt=yes;'
    )