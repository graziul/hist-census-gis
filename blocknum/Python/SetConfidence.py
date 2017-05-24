
####
#### TO DO: Compress options into fewest variables possible (i.e. 2 maps -> 1 variable if possible)
####

import pysal as ps
import pandas as pd
'''
Arguments
---------
dbfile  : DBF file - Input to be imported
upper   : Condition - If true, make column heads upper case
'''
def dbf2DF(dbfile, upper=True): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile) #Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    #pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    if upper == True: #Make columns uppercase if wanted 
        pandasDF.columns = map(str.upper, db.header) 
    db.close() 
    return pandasDF

dbf_file = "S:\\Projects\\1940Census\\Hartford\\GIS_edited\\Hartford_1930_Block_Choice_Map2.dbf"
df = dbf2DF(dbf_file,upper=False)

def df2dbf(df, dbf_path, my_specs=None):
    '''
    Convert a pandas.DataFrame into a dbf.
    __author__  = "Dani Arribas-Bel <darribas@asu.edu> "
    ...
    Arguments
    ---------
    df          : DataFrame
                  Pandas dataframe object to be entirely written out to a dbf
    dbf_path    : str
                  Path to the output dbf. It is also returned by the function
    my_specs    : list
                  List with the field_specs to use for each column.
                  Defaults to None and applies the following scheme:
                    * int: ('N', 14, 0)
                    * float: ('N', 14, 14)
                    * str: ('C', 14, 0)
    '''
    if my_specs:
        specs = my_specs
    else:
        type2spec = {int: ('N', 20, 0),
                     np.int64: ('N', 20, 0),
                     float: ('N', 36, 15),
                     np.float64: ('N', 36, 15),
                     str: ('C', 14, 0)
                     }
        types = [type(df[i].iloc[0]) for i in df.columns]
        specs = [type2spec[t] for t in types]
    db = ps.open(dbf_path, 'w')
    db.header = list(df.columns)
    db.field_spec = specs
    for i, row in df.T.iteritems():
        db.write(row)
    db.close()
    return dbf_path


#
# Reduce OCR variables to fewest possible
#

vars_to_compress = ['MBID','MBID2','MBID3']

df_to_compress = df[vars_to_compress]
list_to_compress = df_to_compress.values.tolist()
list_compressed = [list(set(i)) for i in list_to_compress]
for i in list_compressed:
	if '' in i:
		i.remove('')
df_compressed = pd.DataFrame.from_records(list_compressed)
min_num_vars = len(df_compressed.columns)

for i in range(1,min_num_vars+1):
	df['ocr%s' % (str(i))] = df_compressed[[i-1]]

#
# Find highest confidence block number guess
#

def get_auto_blocknum(x,conf):

	# Confidence 1: Matt's strict (100% of people are in block)
	#				Matt's loose (criteria 2 or 3) and Chris's strict (100% of streets match) agree
	if conf == 1:
		if x['MBID'] != '':
			return [x['MBID'], conf]
		if x['MBID2'] == x['blockdesc'] and x['MBID2'] != '':
			return [x['MBID2'], conf]
		if x['MBID3'] == x['blockdesc'] and x['MBID3'] != '':
			return [x['MBID3'], conf]				
		else:
			return ['', '']

	# Confidence 2: Matt's loose and Chris's loose (75% of streets match) agree
	#
	if conf == 2:
		if x['auto_bnc'] == '':
			if x['MBID2'] == x['blockdesc2'] and x['MBID2'] != '':
				return [x['MBID2'], conf]	
			if x['MBID3'] == x['blockdesc2'] and x['MBID3'] != '':
				return [x['MBID3'], conf]	
			else:		
				return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 3: Matt's loose
	#				Chris's strict and one of Chris's OCR agree
	if conf == 3:
		if x['auto_bnc'] == '':
			if x['MBID2'] != '':
				return [x['MBID2'], conf]	
			elif x['MBID3'] != '':
				return [x['MBID3'], conf]			
			for i in range(1,min_num_vars+1):
				if x['blockdesc'] == x['ocr%s' % (str(i))] and x['blockdesc'] != '':
					return [x['blockdesc'], conf]	
			else:
				return ['','']					
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 4: Chris's strict 
	#				Chris's loose and one of Chris's OCR agree
	if conf == 4:
		if x['auto_bnc'] == '':
			if x['blockdesc'] != '':
				return [x['blockdesc'], conf]				
			for i in range(1,min_num_vars+1):
				if x['blockdesc2'] == x['ocr%s' % (str(i))] and x['blockdesc2'] != '':
					return [x['blockdesc2'], conf]	
			else:
				return ['','']											
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 5: Chris's loose 
	#
	if conf == 5:
		if x['auto_bnc'] == '':
			if x['blockdesc2'] != '':
				return [x['blockdesc2'], conf]	
			else:
				return ['','']							
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 6: At least two of Chris's OCR agree
	#
	if conf == 6:
		if x['auto_bnc'] == '':
			if min_num_vars > 1:
				guess = ''
				for i in range(1,min_num_vars+1):
					for j in range(1,min_num_vars+1):
						if i != j and x['ocr%s' % (str(i))] == x['ocr%s' % (str(j))] and x['ocr%s' % (str(i))] != '':
							guess = [x['ocr%s' % (str(i))], conf]
				if guess != '':
					return [guess, conf]
				else:
					return ['','']
			else:
				return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 7: List of OCR guesses
	#
	if conf == 7:
		if x['auto_bnc'] == '':
			if min_num_vars > 1:
				guesses = [] 
				for i in range(1,min_num_vars+1):
					guesses.append(x['ocr%s' % (str(i))])
				guesses = list(set(guesses))
				if len(guesses) > 1:
					return [', '.join(guesses), conf]
				if len(guesses) == 1 & guesses[0] != '':
					return [guesses[0], conf]
				else:
					return ['','']
			if min_num_vars == 1:
				if x['ocr1'] != None:
					return [x['ocr1'], conf]
				else:		
					return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()
	else:
		return ['','']

for i in range(1,8):
	df['auto_bn'], df['auto_bnc'] = zip(*df.apply(lambda x: get_auto_blocknum(x,i), axis=1))

df2dbf(df,dbf_file)