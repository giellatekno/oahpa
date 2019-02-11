DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fkv_oahpa',
        'USER': 'fkv_oahpa',
        'PASSWORD': 'Kainun%',
        'HOST': 'localhost',
        'PORT': '3040',
        'OPTIONS': {
         'read_default_file': '/etc/my.cnf',
         # 'charset': 'utf8',
         'init_command': 'SET storage_engine=INNODB', #  ; SET table_type=INNODB',
         }
    }
}

FILE_CHARSET = 'utf8'
DEFAULT_CHARSET = 'utf8'
DATABASE_CHARSET =  'utf8'

