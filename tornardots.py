from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tellstickservices import app, handle_opts, app_init


if __name__ == "__main__":
  handle_opts()
  app_init()

  http_server = HTTPServer(WSGIContainer(app))
  http_server.listen(5000, '0.0.0.0')
  IOLoop.instance().start()
