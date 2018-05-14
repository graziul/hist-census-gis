import csv
import re
import itertools
import multiprocessing
import pickle

SL40file = open('StLouis1940Micro.csv','r')
SL30file = open('StLouis1930Micro.csv','r')


Lines40 = csv.reader(SL40file)
Lines30 = csv.reader(SL30file)


Add_ED_dict40 = {} # look up hn[ ]st_name -> ED
Add_ED_dict30 = {} # look up hn[ ]st_name -> ED
ed_30_40_dict = {} # look up 30ed -> 40ed
ed_40_30_dict = {} # look up 40ed -> 30ed

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
	if not k in Dict :
		Dict[k] = [v]
	else :
		if not v in Dict[k] :
			Dict[k].append(v)

# compares two sets of addresses in format
# hn[ ]st_name
def compare_addresses(s1, s2) :
	return s1.intersection(s2)

# compares two sets of EDs and determines true only if they "interlock"
# "interlock": the sets equal the corresponding sets we expect from looking up in the dicts
# IMPORTANT: MUST PASS 1930 EDs as 1st argument!!!
def ed_set_compare(s1, s2) :
	EDs40 = []
	for s in s1 :
		EDs40 = EDs40+ ed_30_40_dict[s]
	if not s2 == set(EDs40) :
		return False
	EDs30 = []
	for s in s2 :
		EDs30 = EDs30 + ed_40_30_dict[s]
	if not s1 == set(EDs30) :
		return False
	return True


for ind, line in enumerate(Lines40) :
	addr = line[2]+" "+line[1]
	Add_ED_dict40[addr] = line[0]

for ind, line in enumerate(Lines30) :
	addr = line[2]+" "+line[1]
	Add_ED_dict30[addr] = line[0]

overlap = compare_addresses(set(Add_ED_dict30.keys()),set(Add_ED_dict40.keys()))

for a in overlap :
	Dict_append_unique(ed_30_40_dict, Add_ED_dict30[a], Add_ED_dict40[a])
	Dict_append_unique(ed_40_30_dict, Add_ED_dict40[a], Add_ED_dict30[a])


max_n = 3

def mp_worker(c30):
	for m in range(1,max_n+1):
		combo40 = itertools.combinations(ed_40_30_dict.keys(),m)
		#print("    checking all "+str(len(list(combo40)))+" '40 combos of length "+str(m))
		#print(str(c30)+" ? ")
		for c40 in combo40 :
			if ed_set_compare(set(c30), set(c40)):
				return [c30, c40]


#find singleton matches separately!!
important_dict = {}
for l in range(1,max_n+1) :
	t = []
	combo30 = itertools.combinations(ed_30_40_dict.keys(),l)
	#print("checking all "+str(len(list(combo30)))+" '30 combos of length "+str(l))
	p = multiprocessing.Pool(64)
	t = p.map(mp_worker, combo30)
	important_dict[l] = [i for i in t if i is not None]

pickle.dump(important_dict,open('important_dict.pkl','wb'))
