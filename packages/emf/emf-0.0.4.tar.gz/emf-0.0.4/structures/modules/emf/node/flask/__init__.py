



import flask
from flask import Flask

import emf.node.flask.routes as routes

def start (parameters):
	flask_port = parameters ["flask"] ["port"]

	app = Flask (__name__)

	routes.link (app)

		
	app.run (
		port = flask_port
	)



	return;