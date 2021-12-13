from flask import Flask, g, session
from routing.user_routes import user_app
from routing.analytics_routes import analytics_app
from routing.backend_user_routes import backend_user_app
from routing.database import Database, init_db

app = Flask(__name__)

blueprints = [
    user_app,
    analytics_app,
    backend_user_app
]

[app.register_blueprint(bp) for bp in blueprints]

while True:
    try:
        init_db()
        break
    except Exception as e:
        pass
d = Database(app)

# d.user.get_db().cursor()
# d.admin.get_db().cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    print(type(d.admin))
    print(type(d.admin.get_db()))
    return "none"


#app.run()







