from app_config import config as conf
from src import init_app

configuration = conf['development']
app = init_app(configuration)

if __name__ == '__main__':
    app.run()