from app_config import configure
from src import init_app

configuration = configure['development']
app = init_app(configuration)

if __name__ == '__main__':
    app.run()