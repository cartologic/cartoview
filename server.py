# Import CherryPy
from cartoview.wsgi import application
import cherrypy
if __name__ == '__main__':
    # Mount the application
    cherrypy.tree.graft(application, "/")
    # Unsubscribe the default server
    cherrypy.server.unsubscribe()
    # Instantiate a new server object
    server = cherrypy._cpserver.Server()
    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.max_request_body_size = 0
    server.socket_timeout = 100000
    server.socket_port = 8000
    server.thread_pool = 20
    # For SSL Support server.ssl_module = 'pyopenssl' server.ssl_certificate =
    # 'ssl/certificate.crt' server.ssl_private_key = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt' Subscribe this server
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
