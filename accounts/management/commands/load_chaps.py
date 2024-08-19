import pymssql
from django.core.management import BaseCommand
from django.conf import settings
from accounts.models import Chapter

# execute using python manage.py load_chaps 

class Command(BaseCommand):
    help = 'Loads chapter data'

    def handle(self, *args, **options):
        print('connecting...')
        conn = pymssql.connect(
            host=r'10.10.1.3',
            tds_version=r'7.0',
            user=r'tbp\bdickson',
            password='KPwbi89@STMarys',
            database='Member'
        )
        print('success connecting to ms sqlserver')
        cursor = conn.cursor(as_dict=True)
        cursor.execute(''' SELECT chp_id
                    ,chp_code
                    ,Chp_Name_Short
                    ,PrimaryChapter
                    FROM Chapters
                    where chp_name_greek != ''
                    and PrimaryChapter = 'Y'
                    order by chp_name_Short ''')
        chapters = cursor.fetchall()
        print(len(chapters))
       
        for c in chapters:
            Chapter.objects.get_or_create(code=c['chp_code'], name_short=c['Chp_Name_Short'])