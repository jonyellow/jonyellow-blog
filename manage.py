#启动程序
from app import create_app,models

#创建app
app = create_app()

#程序的启动位置。
if __name__ == "__main__":
    app.run()
