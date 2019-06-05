from config import url_address, create_app, port, db

if __name__ == '__main__':
    app = create_app()
    app.run(host=url_address, port=port)
