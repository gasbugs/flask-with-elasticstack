"""test"""
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask

app = Flask(__name__)

app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'APM_SERVICE1',
  'SECRET_TOKEN': 'apm-server-token',
  'SERVER_URL': 'http://localhost:8200',
}

apm = ElasticAPM(app)


@app.route('/')
def root():
    """doc string"""
    return '<html><head></head><body><h1>test</h1></body><html>'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
