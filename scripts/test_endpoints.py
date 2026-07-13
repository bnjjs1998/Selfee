import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Pokedex_selfee.settings')
try:
    import django
    django.setup()
    from django.test import Client
    c = Client()
    print('Testing GET /api/group/types/')
    r = c.get('/api/group/types/')
    print('status', r.status_code)
    print(r.content.decode())
    print('\nTesting GET /api/group/grass/add/')
    r2 = c.get('/api/group/grass/add/')
    print('status', r2.status_code)
    print(r2.content.decode())
except Exception as e:
    print('ERROR', repr(e))
    sys.exit(1)
