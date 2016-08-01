import sae
from wexin import wsgi

application = sae.create_wsgi_app(wsgi.application)
