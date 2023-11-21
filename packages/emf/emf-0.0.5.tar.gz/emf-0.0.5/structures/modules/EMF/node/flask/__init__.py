



import flask
from flask import Flask



import asyncio
from websockets.server import serve

import EMF.node.flask.routes as routes

def start (parameters):
	flask_port = parameters ["flask"] ["port"]

	app = Flask (__name__)

	routes.link (app)

	#
	#
	#
	
	

	async def echo(websocket):
		async for message in websocket:
			await websocket.send(message)

	async def main():
		async with serve(echo, "localhost", 8765):
			await asyncio.Future()  # run forever

	asyncio.run(main())
	
	#
	#
	#

		
	app.run (
		port = flask_port
	)



	return;