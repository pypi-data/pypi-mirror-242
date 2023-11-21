

'''
	curl -X PUT -H "Content-Type: application/json" -d '{ "ask": "start" }' "http://127.0.0.1:40023" 
'''

from flask import Flask, request, send_file, request, make_response, send_from_directory, Response

def link (app):
	@app.route ("/", methods = [ 'put' ])
	def node ():
		try:
			data = request.get_json (force = True)
			print ("data:", data)
			
			if ("ask" in data):
				ask = data ["ask"]
			
				if (ask == "escrow petition"):
					pass;
					
				if (ask == "nodes list"):
					pass;
					
				if (ask == "vote proposal"):
					pass;
					
			
		except Exception as E:
			print ("Exception:", E)
			pass
	
		return data;


		
		
		
	