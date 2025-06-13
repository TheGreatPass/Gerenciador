from flask import Flask
from flask_cors import CORS
from blueprints.mobiliarios import mob
from blueprints.materiais import mat
from blueprints.login import auth
from blueprints.usuarios import user
from blueprints.projetos import proj

app = Flask(__name__)
CORS(app)

app.register_blueprint(mob)
app.register_blueprint(mat)
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(proj)

if __name__ == "__main__":
    app.run(debug=True)