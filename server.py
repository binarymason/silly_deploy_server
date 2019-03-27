import flask
from shelljob import proc

app = flask.Flask(__name__)

DEPLOY_SECRET = 'yourmom'
WHITELISTED_CLIENTS = ['127.0.0.1']

@app.route( '/deploy', methods=['POST'])
def deploy():
  client_address = flask.request.remote_addr
  auth = flask.request.headers.get('Authorization')

  if client_address in WHITELISTED_CLIENTS and auth == DEPLOY_SECRET:
    g = proc.Group()
    g.run([ "bash", "-c", "scripts/deploy.sh" ])
    return flask.Response(stream_output(g), mimetype= 'text/plain')
  else:
    return "nope\n", 403


def stream_output(proc_group):
  while proc_group.is_pending():
    for proc, line in proc_group.readlines():
      yield str(line, 'utf-8')

if __name__ == "__main__":
    app.run()
