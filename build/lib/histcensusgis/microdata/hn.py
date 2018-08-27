import codecs
import sys
import re
import time
import math
import urllib
import dbf
import time
import math
import pickle
import fuzzyset
from histcensusgis.s4utils.AmoryUtils import *
import numpy as np

def standardize_hn(s):
	# recommended usage:
	# dfHNList = df['general_house_number_in_cities_o'].apply(standardize_hn1,"columns")
	# df['hn']      = [x[0] for x in dfHNList]
	# df['hn_flag'] = [x[1] for x in dfHNList]
	debug = False
	if(not type(s) == str) :
		try:
			row = s
			s = s['hn']
		except:
			s = str(s)
	orig_s = s
	s = s.strip()
	hnFlag = ''
	s = re.sub('[0-9]/[0-9]|[Rr][Ee][Aa][Rr]','',s)
	s = re.sub('\.$','',s)
	s = re.sub('\([0-9]\)','',s)
	s = s.strip()
	if(re.search("[0-9][0-9][ \-]+[0-9][A-Za-z]$",s)) :
	# Throwing syntax errors
	# if debug : print("%s became " %s,end="")
		s = re.sub("[0-9][A-Za-z]$","",s).strip()
		if debug : print(s)
	if(re.search("^[0-9][0-9][0-9]+[ \-]?[A-Za-z]$",s)) :
	# if debug : print("%s became " %s,end="")
		s = re.sub("[ \-]?[A-Za-z]$","",s).strip()
		if debug : print(s)
	
	s = re.sub("-?\(?([Cc]ontinued|[Cc][Oo][Nn][\'Tte]*[Dd]?\.?)\)?",'',s)
	rangeHN = re.search("([0-9]+)([\- ]+| [Tt][Oo] )[0-9]+",s)
	if(rangeHN) :
		s = rangeHN.group(1)
	s = s.strip()
	if(not orig_s == s) :
		hnFlag = orig_s
	return s, hnFlag

def make_int(s):
	try :
		s = int(s)
		return s
	except ValueError:
		try:
			if s == 'nan':
				return np.nan
			else:
				return int(float(s))
		except ValueError:
			return None

# Handle house number outliers (Amory)
def handle_outlier_hns(df, street_var, outlier_var, year, HN_SEQ, ED_ST_HN_dict):

	### THIS IS A CITYWIDE LIMIT ON THE NUMBER OF PEOPLE THAT CAN LIVE AT A SINGLE ADDRESS ###
	# Limit increased - Buffalo Insane Asylum had >2000 cases
	sys.setrecursionlimit(5000)

	### THIS IS MAXIMUM GAP IN HOUSE NUMBER
	MAX_GAP = 100

	#HN_SEQ = []
	#ST_SEQ = []
	#DW_SEQ = []
	INCONS_st = []
	SINGLE_HN_ERRORS = []
	ED_ST_HN_dict = {}
	SUBUNIT_HN_ERRORS = []

	missingTypes=0

	def is_none(n) :
		if(type(n)==str) :
			return n=='' or n==None
		else :
			return n==None or math.isnan(n)

	def get_linenum(df,ind) :
		if ind>=0 and ind<len(df) :
			return df.loc[ind,'line_num']
		else :
			return None

	def get_name(df,ind) :
		if ind>=0 and ind<len(df) :
			if df.loc[ind,'street'] == "" :
				return None
			else :
				return df.loc[ind,'street']
		else :
			print ("GET NAME OUT OF BOUNDS "+str(ind))
			return -1 #different return values for out of bounds vs. stname missing

	def get_hn(df,ind) :
		if ind>=0 and ind<len(df) :
	#        print(ind)
			return df.loc[ind,'hn']
		else :
			# SHOULD RETURN -1 HERE OR SOMETHING, CONSEQUENCES?
			return None
	#df['hn'] = df.index.to_series().apply(lambda s: get_hn(s))

	#Defaults to str for return value; returns -1 on fail, which is >1 away from any valid dwelling_num
	#The value may be incorrect e.g. in apt buildings the apt. # may be in the dwelling field
	#However in these cases the housenum is unlikely to be wrong also.
	def get_dwelling(df,ind,numeric=False) : 
		if ind>=0 and ind<len(df) :
			if(numeric) :
				debug = False
				dw = re.search('([0-9]+)([ \-/]*[A-Za-z.]|[ \-/]+[0-9]| 1/2)?([ \-/]+[Rr]ear)?$',df.loc[ind,'dn'])
				if(not dw==None) :
					if(dw.group(1)!=df.loc[ind,'dn']) :
						if(debug) : print("dwelling# %s was fixed to: %s" % (df.loc[ind,'dn'],""))
						dw = dw.group(1)
					else :
						dw = dw.string
				else : dw = df.loc[ind,'dn']
				try :
					dw = int(dw)
					if(debug) : print(dw)
					return dw
				except ValueError :
					if(not dw=='') :
						if(debug) : print("Exception. dwelling# at %s is: %s" %(ind,df.loc[ind,'dn']))
					return -1
			else :
				return df.loc[ind,'dn']
		else :
			#-2 is adjacent to -1. Use -3 instead.
			return -3

	def get_fam(df,ind) :
		if ind>=0 and ind<len(df) :
			return df.loc[ind,'fam_id']
		else :
			return -1

	def get_relid(df,ind) :
		if ind>=0 and ind<len(df) :
			return df.loc[ind,'rel_id']
		else :
			return -1

	def get_ed(df,ind) :
		#ED can eventually go where imageid is in the input .txt varlist ([ind][0])
		if ind>=0 and ind<len(df) :
			return df.loc[ind,'ed']
		else :
			return -1

	def same_hh_chk(df,ind,chk) :
		dwel, fam, relid, ind_dwel, chk_dwel, ind_fam, chk_fam, ind_relid, chk_relid = (-1,)*9
		if(get_dwelling(df,ind)!="") :
			ind_dwel = get_dwelling(df,ind)
		if(get_dwelling(df,chk)!="") :
			chk_dwel = get_dwelling(df,chk)
		if(get_fam(df,ind)!="") :
			ind_fam = get_fam(df,ind)
		if(get_fam(df,chk)!="") :
			chk_fam = get_fam(df,chk)
		if(get_relid(df,ind)!="") :
			ind_relid = get_relid(df,ind)
		if(get_relid(df,chk)!="") :
			chk_relid = get_relid(df,chk)
		if(not -1==ind_dwel and not -1==chk_dwel) :
			dwel = (ind_dwel==chk_dwel)
		if(not -1==ind_fam and not -1==chk_fam) :
			fam = (ind_fam==chk_fam)
		if(not -1==ind_relid and not -1==chk_relid) :
			relid = (ind_relid==chk_relid)
		#if all available hh_chk vars check out, and they are not all undefined (-1)
		if(dwel==-1 and fam==-1 and relid==-1) :
			return -1
		else :
			return [(dwel==-1 or dwel) and (fam==-1 or fam) and (relid==-1 or relid),dwel,fam,relid]
		

	#evaluative function to determine HN sequences#
	def seq_end_chk(cur_num,chk_num) : #returns True if cur_num and chk_num are in DIFFERENT SEQs
		error_type = 0
		if(is_none(cur_num)) : #if housenum undefined, consider it the end of seq
			error_type = 1
		elif (not (cur_num+chk_num) % 2 == 0) : #one num even, next odd; or vice-versa
			error_type = 2
		elif (abs(cur_num-chk_num) > MAX_GAP) : #gap between two nums exceeds MAX_GAP
			error_type = 3
		return (not error_type==0, error_type)

	  
	#recursive function to walk through HN sequences#
	def num_seq(df,ind,chk_num,chk_dir,debug=False) : #chk_dir = 1|-1 depending on the direction to look
		if(ind>=0 and ind<len(df)) :
			cur_num = get_hn(df,ind)
			end = seq_end_chk(cur_num,chk_num)
			if(end[0]) : #if cur num doesn't fit in SEQ...
				if(end[1]==1) : 
					#try to fill in blank HNs#
					sameHH = same_hh_chk(df,ind,ind-chk_dir)
					#if debug: print(str(sameHH)+" "+str(ind))
					#check that at least dwelling# and relID are the same, as well as stname...#
					# Throws error when sameHH = -1
					if type(sameHH) is not int:
						if(sameHH[1] and sameHH[3] and get_name(df,ind)==get_name(df,ind-chk_dir)) :
							if debug: print("at %s changed %s to %s" %(ind,cur_num,chk_num))
							df.set_value(ind, 'hn', chk_num)
							return num_seq(df,ind+chk_dir,chk_num,chk_dir)
						if(False) : # if dwel and relID are not same but dwel is sequential, interpolate HNs #
							False
				nextNum = seq_end_chk(get_hn(df,ind+chk_dir),chk_num) #...see if next num does
				if(not nextNum[0] and get_name(df,ind)==get_name(df,ind-1) and get_name(df,ind)==get_name(df,ind+1)) :
				#do we want to check sequence of dwelling nums? e.g. 4584230_01092
				#seems like an error but is actually correct because non-consecutive dwelling no.
				#YES. TODO: improve HN swatches using other vars. if stname AND imageid changes, it's probably
				#the end of the HN swatch even if it could keep going. same goes for stname AND dwelling_num_SEQ changing?
				#Likewise, if HN swatch would stop but the error is explained by dwelling_num_SEQ changing while stname stays the same
			
					SINGLE_HN_ERRORS.append([ind,end[1]])
					return num_seq(df,ind+chk_dir,chk_num,chk_dir)
				else :
					if(get_dwelling(df,ind+chk_dir)==get_dwelling(df,ind) and get_dwelling(df,ind-chk_dir)==get_dwelling(df,ind) and get_dwelling(df,ind)!=-1) :
						if(chk_dir==1 and get_name(df,ind+chk_dir)==get_name(df,ind) and get_name(df,ind-chk_dir)==get_name(df,ind)) :#HNs may only replace other HNs "downstream"
							SUBUNIT_HN_ERRORS.append([ind,ed_hn_outlier_chk(get_ed(df,ind),get_name(df,ind),get_hn(df,ind))])
							#HOW TO DEAL WITH THESE
							#Reveals places where there are HN typos as well as apt/unit numbers in HN
							#Therefore, we can fix based on whether one of the two addresses for a given dw# and stname is obviously an outlier
							#However, must deal with false positive problem created by stupid dw#s. Sometimes enumerator just stops updating dw#
							#for like a whole page, across multiple STs, etc.
							#IF HN IS A SIGNIFICANT OUTLIER

							#This makes weird stuff happen with the Hangover Code, so put it on hold for now:
							#return dwel_seq(ind,chk_dir)
					return ind-chk_dir
			else :
				return num_seq(df,ind+chk_dir,cur_num,chk_dir)
		else :
			return ind-chk_dir

	#wrapper function for num_seq recursion#
	def seq_match_num(df,ind) : 
	#    print(ind)
		num = get_hn(df,ind)
		if is_none(num) : #if housenum undefined, consider it a singleton seq
			return [ind,ind]
		seq_start = num_seq(df,ind-1,num,-1)
		seq_end = num_seq(df,ind+1,num,1)

		return [seq_start,seq_end]#[seq_start,seq_end,get_hn(seq_start),get_hn(seq_end)]

	#Returns just the NAME component of the street phrase, if any#
	def isolate_st_name(st) :
		if(not (st == None or st == '' or st == -1)) :

			TYPE = re.search(r' (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$',st)
			if(TYPE) :
				st = re.sub(TYPE.group(0), "",st)
			st = re.sub("^[NSEW]+ ","",st)
			st = st.strip()
		return st

	#returns True if st does not share a NAME with any other street in ed
	def st_name_ed_check(st, ed, st_ed_dict) :
		debug = True
		NAME = isolate_st_name(st)
		if(NAME in st_ed_dict.keys()) :
			for s in st_ed_dict[NAME].keys() :
				if(s != st and str(ed) in st_ed_dict[NAME][s]) :
					if(debug) : print("%s is in same ed as %s" %(s,st))
					return False
		else :
			if(debug) : print("could not find %s in dict" %NAME)
		return True

	def st_seq(df,ind,st_ed_dict) :
		global missingTypes
		name = get_name(df,ind)
		i=ind
		#TODO: Modify code so that it CHECKS AGAINST OTHER STNAMES IN ED / CITY
		while(get_name(df,i-1)==name or isolate_st_name(get_name(df,i-1))==isolate_st_name(name)) :
			if(get_name(df,i-1)==name) :
				i = i-1
			else :
				if(not seq_end_chk(get_hn(df,i),get_hn(df,i-1))[0] and len(get_name(df,i-1)) < len(get_name(df,i)) and st_name_ed_check(get_name(df,i), get_ed(df,i),st_ed_dict)) : #more sophisticated check?
					i = i-1
					#print("at %s changed %s to %s" %(i,get_name(i),name))
					df.set_value(i, 'street', name)
					missingTypes= missingTypes+1
				else :
				  # print("at %s DID NOT change %s to %s" %(i-1,get_name(i-1),name))
				   break
					
		start = i
		while(get_name(df,ind+1)==name or isolate_st_name(get_name(df,ind+1))==isolate_st_name(name)) :
			
			if(get_name(df,ind+1)==name) :
				ind = ind+1
			else :
				if(not seq_end_chk(get_hn(df,ind),get_hn(df,ind+1))[0] and len(get_name(df,ind+1)) < len(get_name(df,ind)) and st_name_ed_check(get_name(df,ind), get_ed(df,ind),st_ed_dict)) : #more sophisticated check?
					ind = ind+1
				   # print("at %s changed %s to %s" %(ind,get_name(ind),name))
					missingTypes= missingTypes+1
					df.set_value(ind, 'street', name)
				else :
				  # print("at %s DID NOT change %s to %s" %(ind+1,get_name(ind+1),name))
				   return [start,ind]
		return [start,ind]#[start,ind,name]

	#if chk_dir is -1 or 1, does a uni-directional search for end of sequence and returns index
	#otherwise, checks in both directions and returns list of start and end indices
	def dwel_seq(ind,chk_dir=0) :        
		start=ind
		if(chk_dir!=0) :
			while (abs(get_dwelling(df,start+chk_dir,numeric=True)-get_dwelling(df,start,numeric=True))<=1) :
				start = start+chk_dir
			return start
		else :
			while (abs(get_dwelling(df,start-1,numeric=True)-get_dwelling(df,start,numeric=True))<=1) :
				start = start-1
			end = ind
			while (abs(get_dwelling(df,end+1,numeric=True)-get_dwelling(df,end,numeric=True))<=1) :
					end = end+1
			return [start,end]

	#try to fix single hn errors based on sequence before and after error

	def hn_seq_err_fix(df,ind) :
		hn = str(get_hn(df,ind))
		p = str(get_hn(df,ind-1)) #prev num
		n = str(get_hn(df,ind+1)) #next num
		if(n==p) :
				print("thing: "+df.loc[ind,'line_num']+" "+p+" "+hn+" "+n)
		#if dwelling num is same as previous or consecutive; if not, don't try to fix
		#also check if that dwelling num was enumerated elsewheres, compare if so
		#also check if the housenum is changing mid-household (should stay same obv)
		for i,digit in enumerate(hn) :
			False
			#even if we can't conclusively fix hn based on digit comparison, we should
			#still keep track of discrepancies with the rest of the sequence, which may also be wrong

	#start_time = time.time()
	##    eds = [x[7] for x in df]
	##    for ed in np.unique(eds) :
	##        ED = eds[eds.index(ed):len(eds) - list(reversed(eds)).index(ed)]
	##        assert(len(np.unique(ED))==1)
	def get_ED_HN_OUTLIERS(df):
		ED_HN_OUTLIERS = df.groupby(['ed','street'])
		start_time = time.time()
		for ED_ST,df_HN in ED_HN_OUTLIERS : 
			ED_ST_HN_dict[ED_ST] = get_cray_z_scores([x for x in df_HN['hn'] if not math.isnan(x)])
			if(ED_ST_HN_dict[ED_ST]==None) :
				False
				#do something about ED_STs that could not have z-scores calculated
				#this will consist of ED_STs that do not have more than 2 valid HNs
	#    print("Finding ED_ST_HN outliers took %s seconds ---" % (time.time() - start_time))
		return(ED_ST_HN_dict)

	# Use until other functions created with similar funcationality (see Clean.py Line 36)
	def is_HN_OUTLIER(ed,st,hn,ED_ST_HN_dict_r):
		try:
			score = ED_ST_HN_dict_r[(ed,st)][hn]
			if score > 16:
				return True
			else:
				return False
		except:
			return True


	def ed_hn_outlier_chk(ed,st,hn) :
		if(st=='' or is_none(hn) or (ed,st) not in ED_ST_HN_dict.keys()) :
			return -1
		if(ED_ST_HN_dict[(ed,st)] is None):
			return -1
		else :
			return ED_ST_HN_dict[(ed,st)][hn]

	def get_DW_SEQ(df):
		ind = 1
		DW_SEQ = []
		while ind<len(df) :
			DW_SEQ.append(dwel_seq(ind))
			ind = DW_SEQ[len(DW_SEQ)-1][1]+1
		return DW_SEQ
	#DW_SEQ = get_DW_SEQ()

	#print(DW_SEQ[:20])
	#print(len(DW_SEQ))

	def get_HN_SEQ(df,year,street,debug=False):
		df['street'] = df[street]
		ED_HN_OUTLIERS = get_ED_HN_OUTLIERS(df)
		ind = 0
		HN_SEQ = []
		while ind<len(df) :
			try:
				HN_SEQ.append(seq_match_num(df,ind))
			except RuntimeError :
				print("STACK OVERFLOW...? ind was: "+str(ind)+", which is linenum "+str(get_linenum(df,ind))+" on page "+str(df.loc[ind,'line_num']))
			ind = HN_SEQ[len(HN_SEQ)-1][1]+1
		if debug:
			avg_seq_len = round(np.mean(np.diff(HN_SEQ)),1)
			print("Average HN sequence length is %s" % (str(avg_seq_len)))
		del df['street']
		return HN_SEQ, ED_HN_OUTLIERS
	#HN_SEQ = get_HN_SEQ(df)

	#print("subunit")
	#print(SUBUNIT_HN_ERRORS[:20])
	#print(len(SUBUNIT_HN_ERRORS))

	def get_ST_SEQ(df,st_ed_dict):
		missingTypes = 0
		ind = 0
		ST_SEQ = []
		while ind<len(df) :
			ST_SEQ.append(st_seq(df,ind,st_ed_dict))
			ind = ST_SEQ[len(ST_SEQ)-1][1]+1
		return ST_SEQ

	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df, year, street_var, debug=True)
	df['hn_outlier1'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'], s[street_var], s['hn'], ED_ST_HN_dict[street_var]),axis=1)
 
	return df, HN_SEQ, ED_ST_HN_dict

####
#### BELOW WAS COMMENTED OUT AT BOTTOM OF "HNclean.py"! 
####

#ST_SEQ = get_ST_SEQ()	
#print("missing TYPES: "+str(missingTypes))

### ERROR CHECKING LOOP: check swatches that do not match up ###
'''
hn_set = set(map(tuple,HN_SEQ))
INCONS_st = [x for x in map(tuple,ST_SEQ) if x not in hn_set] #st swatches that lack a corresponding HN swatch

st_set = set(map(tuple,ST_SEQ))
INCONS_hn = [x for x in map(tuple,HN_SEQ) if x not in st_set] #HN swatches that lack a corresponding st swatch

print("finished forming INCONS sets")

st_seq_starts = [row[0] for row in INCONS_st]
hn_seq_starts = [row[0] for row in INCONS_hn]
st_seq_ends = [row[1] for row in INCONS_st]
hn_seq_ends = [row[1] for row in INCONS_hn]
same_hh_chk
print("Finished making INCONS start and end lists")


CONS_starts = [x for x in st_seq_starts if x in hn_seq_starts]
CONS_ends = [x for x in st_seq_ends if x in hn_seq_ends]

print("Finished making CONS start and end lists")

CONS = list(zip(CONS_starts,CONS_ends))

print(INCONS_st[:10])
print(INCONS_hn[:10])
print(CONS[:10])

HANGOVERS = set()

#OVERLAP: ST and HN swatches intersect but do not contain each other exactly
OVERLAPS = [x for x in CONS if x not in INCONS_st and x not in INCONS_hn]
for o in OVERLAPS :
	debug = True
	st_swatches = INCONS_st[st_seq_starts.index(o[0]):st_seq_ends.index(o[1])+1]
	hn_swatches = INCONS_hn[hn_seq_starts.index(o[0]):hn_seq_ends.index(o[1])+1]
	if(True) : #len(st_swatches)==2 and len(hn_swatches)==2) :
		for s in st_swatches :
			for h in hn_swatches :
				#DO check that inconsistent observations are not mid-hh changes
				#Have to also identify hangovers where the start/end indices of the swatches do NOT EXACTLY line up
				#going along with this, eliminate the >1 obs restriction
				if(not(h[0]==h[1] or s[0]==s[1]) and (s[0]==h[1] or h[0]==s[1])) : #generalized hangover (FIX: only swatches longer than 1 household)
					if (debug) : print('Found a ', end="")
					if (s[0]==h[1]) : #hangover
						hang_ind = s[0]
						hang_dir = 1
					else : #reverse hangover
						hang_ind = h[0]
						hang_dir = -1
						if (debug) : print('reverse ', end="")
					if (debug) : print('hangover at %d, ' % hang_ind, end="")
					same_hh = same_hh_chk(hang_ind,hang_ind-hang_dir)
					if(same_hh[0]) :
						if (debug) : print('that passed same_hh_chk with all available vars, ', end="")
						
						#check to make sure abutting hn for (st that we are assuming is the correct stname) is not an outlier
						st_zscore = ed_hn_outlier_chk(get_ed(hang_ind-hang_dir),get_name(hang_ind-hang_dir),get_hn(hang_ind-hang_dir))
						if(st_zscore<4) :
							if(st_zscore==-1) :
								False
								#DO SOMETHING ABOUT THIS
							if (debug) : print('and was added to HANGOVERS.\n', end="")
							#All cases checked with these criteria were valid ready-to-be-fixed hangovers, except 86289
							test = HANGOVERS.copy()
							HANGOVERS.add(frozenset([hang_ind,hang_ind-hang_dir]))
							if(test == HANGOVERS) :
								print("OH DEAR, THE SAME HANGOVER WAS IDENTIFIED TWICE")
						else :
							if (debug) : print('but there was something suspicious about abutting hn: %s.\n' %st_zscore, end="")
					else :
						if (debug) : print('dwel: %s fam: %s rel: %s\n' %(same_hh[1],same_hh[2],same_hh[3]), end="")
						#if these are all false, we can still fix by seeing if there is another record with same
						#hn, dwel_id and fam_id as the hangover record. If there's nothing suspicious about the other
						#record, we can assume that one is the correct stname

						#Another Validation to think about: look at other HNs for the given st and Block
						#compare even-/odd-ness. Which decades do we have block ID for?
						
					#same hh chk works, but may be too restrictive?
					# for example, at line 18600 the dwelling is same but other two vars are different
					# and it is a valid hangover
					
					if(len(st_swatches)==2 and len(hn_swatches)==2) : #both guaranteed "otherwise well-defined" 
						print(str(o)+" "+str(hn_swatches[1][0]==st_swatches[0][1])+" "+str(hn_swatches[0][1]==st_swatches[1][0]))
					else :
						print(str(o)+" "+str(len(hn_swatches))+" "+str(len(st_swatches)))

##CONS = []
##ind = 0
##while ind<len(df) :
##    if 
print("Hangovers: "+str(len(HANGOVERS)))

errors = 0

#More useful outlier identification: outlying HH nums for a given st and ed
#e.g. St A in ED y has normal HN range 1000-2000. HN 5689 is flagged as outlier.
#This is then used as an additional piece of info when resolving Hangovers



for inc in INCONS_st[:0] :
	#find housenums that are outliers within a st-swatch (or otherwise normal housenum swatch - only one address diff)
	#compute standard deviation, median of housenums within st swatch
	#Standard Deviation should be calculated with respect to how much housenum deviates from previous num, as opposed
	# to how much it deviates from the distribution as a whole?
	
	#HOW WILL USING ALL HOUSENUMS AND NOT JUST 1 FOR EACH HOUSEHOLD AFFECT RESULTS?
	inc_nums = [row[2] for row in df[inc[0]:inc[1]+1]]
	print("inc nums: "+str(inc_nums))
	z = get_cray_z_scores(inc_nums)
	
		
		#if z_score > 4, consider an outlier?
	
last = INCONS_hn[0]
print("# of incons "+ str(len(INCONS_hn)))
for inc in INCONS_hn[:0] :
	if True : ### inc[0] - last[1] == 1 : #consecutive unmatched swatches: what kind of error defines these??
		print(str(last)+" & "+str(inc)+" : ")
		inc_STs = df[inc[0]:inc[1]+1]
		last_ST = inc_STs[0]
##        for st in inc_STs : #check if address is same but dwelling num different.
##            if st[2] == last_ST[2] and st[3] == last_ST[3] and not st[4] == last_ST[4] :
##                print("Found a probable wrong housenum, dwelling nums are: "+str(st[4])+" & "+str(last_ST[4]))
##            last_ST = st
		STs_freq = Counter([row[3] for row in inc_STs]).most_common()
		if len(STs_freq) == 2 :
			print(STs_freq)
			ratio = float(STs_freq[1][1])/float(STs_freq[0][1])
			if ratio <= .1 :
				errors = errors+1
				print("found a probable wrong stname, ratio: "+str(ratio))
	last = inc

print(errors)
'''
