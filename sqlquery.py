import pymssql

print('connecting...')
conn = pymssql.connect(
    host=r'10.10.1.3',
    tds_version=r'7.0',
    user=r'tbp\bdickson',
    password='KPwbi89@STMarys',
    database='Member'
)
print('success')
cursor = conn.cursor(as_dict=True)
cursor.execute('''SELECT *
                from Address where add_email = 'curt@tbp.org' ''')
users = cursor.fetchall()
print(len(users))