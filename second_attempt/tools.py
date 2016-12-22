from __future__ import division
try:
	import cPickle as pickle
except:
	import pickle
	

import os
import similar

root = os.getcwd() + '//sets'
def dumppickle(item, path):
	output = open(root + path,'wb')
	pickle.dump(item,output)
	output.close()
def loadpickle(path):
	pkl_file = open(root + path,'rb')
	data = pickle.load(pkl_file)
	pkl_file.close()
	return data
	
def generate_itemSimOnTypeSet():
    prefs = {}
    result = {}
    try:
        with open(os.getcwd() + '//ml-100k' + '/u.item') as item:
            for line in item:
                typeVector = line.split('|')[5:24]
                itemId = line.split('|')[0]
                prefs[itemId] = typeVector
                result.setdefault(itemId, {})
    except IOError as err:
        print('File error: ' + str(err))
    
    for key1, value1 in prefs.items():
        for key2, value2 in prefs.items():
            if key1 != key2:
                s = similar.sim_itemType(value1, value2, 19)
                print
                key1, key2, s
                result[key1][key2] = s
	dumpPickle(result, '/itemSimOnType.pkl')
