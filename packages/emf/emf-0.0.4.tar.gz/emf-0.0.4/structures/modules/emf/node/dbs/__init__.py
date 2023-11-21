
'''
import emf.node.dbs as dbs
dbs.rennovate ()
'''

'''
	if already built, continue
'''

import lymphatic.system.connect as connect

def rennovate ():
	[ r, c ] = connect.now ()

	if "money" not in (r.db_list().run(c)):
		r.db_create ('money').run (c)
	else:
		print ("money db already exists")

	money = r.db ('money')
	money_tables = r.db ('money').table_list().run (c)
	if "constants" not in money_tables:
		money.table_create ('constants', primary_key = 'ellipse').run (c)



	#
	
	if "ledger" not in (r.db_list().run(c)):
		r.db_create ('ledger').run (c)
	else:
		print ("ledger db already exists")
	
	ledger = r.db ('ledger')
	ledger_tables = r.db ('ledger').table_list().run (c)
	if "aggregates" not in ledger_tables:
		ledger.table_create ('aggregates', primary_key = 'ellipse').run (c)
	
	if "steps" not in ledger_tables:
		ledger.table_create ('steps', primary_key = 'ellipse').run (c)
	
	#
	#
	#
	
	if "coms" not in (r.db_list().run(c)):
		r.db_create ('coms').run (c)
	else:
		print ("coms db already exists")	

	coms = r.db ('coms')
	coms_tables = r.db ('coms').table_list().run (c)
	if "petitions" not in coms_tables:
		coms.table_create ('petitions', primary_key = 'ellipse').run (c)

	if "accounts" not in coms_tables:
		coms.table_create ('accounts', primary_key = 'ellipse').run (c)

	return;

