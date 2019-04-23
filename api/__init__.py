import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yml')
