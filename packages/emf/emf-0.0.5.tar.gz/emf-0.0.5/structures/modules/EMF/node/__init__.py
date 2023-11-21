

'''
	plan:
		[] EMF-node start

		import EMF.node as EMF_node
		EMF_node.start ({
			"flask": {
				"port": 40023
			},
			"rethink": {
				"ports": {
					"driver": "40024",
					"cluster": "40025",
					"http": "40026"
				} 
			},
			"trustees": [
				"localhost:40027"			
			]
		})
'''



import EMF.node.flask as node_flask

import lymphatic.system.climate as ly_system_climate
import pathlib
import lymphatic.system.start as ly_system_start

import EMF.node.dbs as dbs


def start (parameters):
	
	print ("flask port")
	
	
	rethink_ports = parameters["rethink"]["ports"]
	
	ly_system_climate.change ("ports", {
		"driver": rethink_ports ["driver"],
		"cluster": rethink_ports ["cluster"],
		"http": rethink_ports ["http"]
	})
	

	ly = ly_system_start.now (
		process = {
			"cwd": pathlib.Path (__file__).parent.resolve ()
		},
		rethinkdb = [
			#f"--pid-file {}"
		],
		#wait = True
	)
	#ly.stop ()
	
	dbs.rennovate ()
	
	print ('starting flask?')

	node_flask.start (parameters)

	return;