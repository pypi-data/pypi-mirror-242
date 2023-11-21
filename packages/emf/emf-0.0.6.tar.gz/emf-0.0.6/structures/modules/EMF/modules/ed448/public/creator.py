

'''
	from DUOM.ED448.PUBLIC_KEY.CREATE import CREATE_PUBLIC_KEY
	PUBLIC_KEY = CREATE_PUBLIC_KEY ({
		"PRIVATE KEY PATH": "",
		"PUBLIC KEY PATH": "",
		"PUBLIC KEY FORMAT": "DER"
	})
'''

'''
	#
	#	write public key to path
	#
	import EMF.modules.ed448.public.creator as ed448_public_key_creator
	public_key = ed448_public_key_creator.create (
		private_key_path = "",
		public_key_path = "",
		public_key_format = ""
	)
	if (public_key ["success"] == "yes"):
		public_key_class = public_key ["class"]
		public_key_string = public_key ["string"]
		
'''

'''
	FORMAT:
		DER
		PEM
'''
from Crypto.PublicKey.ECC 	import EccKey
from Crypto.PublicKey 		import ECC

import EMF.modules.ed448.private.scan as private_scan


def write (path, key_string, format):
	import os
	if (os.path.exists (path)):
		return [ False, "The path for the public key is not available." ];
	
	if (format == "DER"):
		f = open (path, 'wb')
	elif (format == "PEM"):
		f = open (path, 'w')
	else:
		raise Exception (f"format '{ format }' was not accounted for.")
	
	f.write (key_string)
	f.close ()
	
	return [ True, "" ];

#
#	S & V = { SIGNER, SIGNATORY } & { APPROVER, RATIFIER, VERIFIER }
#
#	SIGNER & VALIDATOR
#


def create (
	private_key_path = "",
	public_key_path = "",
	public_key_format = ""
):	
	private_key = private_scan.start (private_key_path)

	public_key_instance = private_key.instance.public_key ()
	public_key_string = public_key_instance.export_key (format = public_key_format)
	
	[ WRITTEN, NOTE ] = write (public_key_path, public_key_string, public_key_format)
	if (WRITTEN == False):
		return {
			"success": "no",
			"alarm": NOTE 
		}
		
			
	return {
		"success": "yes",
		
		"instance": public_key_instance,
		"string": public_key_string
	}
