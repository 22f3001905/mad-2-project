from server import app
app.app_context().push()

from app.utils import basic_setup
basic_setup()
