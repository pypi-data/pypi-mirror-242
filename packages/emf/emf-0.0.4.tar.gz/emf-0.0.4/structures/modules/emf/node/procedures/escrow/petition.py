
'''
	escrow_petition ({
		unsigned_message: {
			#
			#	for aggregate 1 implies that this petition is to
			#	add an escrow before the aggregate 1 (balance sheet)
			#	is built.
			#
			for_aggregate: 1,
			
			escrow: {
				escrow: 1,
				from: {address},
				to: {address}
			}
		},
		signed_message: {signed message}
	})
'''

'''
validators: [{
	[ address ]: {
		#
		#	The fraction of currency that the validator possesses.
		#	The fraction sum need to be >= 1/2.
		#	
		#		(obviously there are other voting mechanisms possible)
		#
		fraction: ""
	},
}]
'''

'''
	import emf.node.procedures.escrow.petition as escrow_petition
'''
def now ():
	return;