from safrs import SAFRSAPI

from config import app, db
from models.swagger_init import expose

api = SAFRSAPI(app, host='127.0.0.1', port=5000, prefix='/api/docs')
app.app_context().push()
expose(api)
