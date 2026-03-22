

import os
from dotenv import load_dotenv

load_dotenv() # здесь мы загружаем наши переменные из .env

class SuperAdminCreds:
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME') # забираем значение наших переменных из .env
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')
