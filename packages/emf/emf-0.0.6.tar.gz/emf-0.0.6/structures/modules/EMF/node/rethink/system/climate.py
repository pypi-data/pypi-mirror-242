


'''
import EMF.rethink.system.climate as rethink_system_climate
rethink_system_climate.change ("ports", {
	"driver": 18871,
	"cluster": 0,
	"http": 0	
})
'''

'''
import EMF.rethink.system.climate as rethink_system_climate
ports = rethink_system_climate.find ("ports")
'''

import copy

climate = {
	"ports": {
		"driver": 18871,
		"cluster": 0,
		"http": 0
	}
}

def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (field):
	return copy.deepcopy (climate) [ field ]