"""
Edited Crunchbase investment predictor script.
Original by Jerry Neumann
"""
# whichvc
#
# Step 1: get VCs
#    for each VC, get companies, round and date
#    list of all VCs with >=20 investments in last 5 years
#    form: [(vc permalink, vc name, [(co permalink, round, date),(...),...]),(...),...]

import sys, urllib2, cPickle as pickle, simplejson as json, re, nltk, os 
api_key = os.getenv("crunchbase_key") 

def getCBinfo(namespace, permalink):
	api_url="http://api.crunchbase.com/v/1/%s/%s.js?api_key=%s" % (namespace, permalink, api_key)
	return json.loads(urllib2.urlopen(api_url).read())

# get vc list
vcs=json.loads(urllib2.urlopen('http://api.crunchbase.com/v/1/financial-organizations.js?api_key='+api_key).read())

topvcs=[]
badvcs=[]
for vc in vcs:
	name = vc['name']
	pl = vc['permalink']
	print pl
	try:
		entry = getCBinfo('financial-organization',pl)
	except:
		print "bad."
		badvcs.append(pl)
		continue
	invs = entry.get('investments')
	invpls = set()
	invests = []
	if invs:
		for inv in invs:
			fr = inv.get('funding_round')
			if fr:
				co = fr['company']['permalink']
				round = fr['round_code']
				month = fr.get('funded_month','0')
				year = fr.get('funded_year','0')
				date ="%s/%s" % (month,year)
				invpls.add(co)
				invests.append((co,round,date))
	if len(invpls) > 19:
		topvcs.append((pl,name,invests))
	print topvcs
with open("vctree/opvcs.p","w") as f:
	pickle.dump(topvcs,f)
				
# Step 2: make list of companies to get data for
costoget = set()
for pl1,vc,invs in topvcs:
	for pl,r,d in invs:
		costoget.add(pl)
		
# Step 3: get company data
ptn=re.compile(r'\ba\b|\ban\b|\bthe\b|\band\b|\bthat\b|\bthis\b|\bto\b|\bas\b|\bfor\b|\bof\b|\bin\b|\byou\b|\byour\b|\bbut\b|\bwith\b|\bon\b|\bis\b|\bby\b|\bfrom\b|\btheir\b|\bit\b|\bits\b|\btheir\b|\bor\b|\bat\b|\bwhich\b|\bcan\b|\binc\b|\bhas\b|\bhave\b|\balso\b|\bthan\b|\ball\b|\bbe\b|\bthey\b|\bwas\b|\bsuch\b|\binto\b')
ptn2=re.compile(r'\&#[0-9A-F]{4};')
ptn3=re.compile(r'\b[0-9]+') #words beginning with digits--get rid of digits
ptn4=re.compile(r'[!\?:;]') # end of clause or sentence to make into periods ,;:!?
ptn5=re.compile(r'[\"$\(\)&\/,]') # other punctuation: get rid of
ptn6=re.compile(r'\.[ ]+(?=[A-Z])') # Break into sentences

j=0
bad=[]
cograms=[]
for pl in costoget:
	try:
		entry = getCBinfo('company',pl)
	except:
		print "Fail on ",pl
		bad.append(pl)
		continue
		
	j=j+1
	if j%10==0: print j
	
	tl = entry.get('tag_list')
	grams = set([x.strip() for x in tl.replace('-',' ').split(',')]) if tl else set()
	
	txt = entry.get('overview')
	# clean tags and text
	#    1. strip eol, apostrophes, numbers, HTML
	#    2. all other punctuation to spaces
	#    3. Break into sentences
	if txt:
		txt2 = nltk.clean_html(txt.replace("\n"," ").encode('ascii','ignore').replace('\\/','/').replace("'",""))
		txt3 = ptn5.sub(" ",ptn4.sub(".",ptn3.sub(" ",ptn2.sub("",txt2))))
		sents = ptn6.split(txt3)
	
		# tokenize sentences
		for sent in sents:
			sent1 = ptn.sub("",sent.lower().replace("."," "))
			sent2 = sent1.split()
			grams.update(set(nltk.bigrams(sent2)))
			grams.update(set(nltk.trigrams(sent2)))
	
#	gramcnt = {}
#	for gram in grams: gramcnt[gram]=gramcnt.get(gram,0)+1
	
	# save (pl,{gram:x,gram:y,gram:z,...})
	cograms.append((pl,list(grams)))
	
with open("vctree/cograms.p","w") as f:
	pickle.dump(cograms,f)
	
totgrams = {}
for co,grams in cograms:
	for gram in grams:
		totgrams[gram] = totgrams.get(gram,0) + 1

cograms2 = []
for co,grams in cograms:
	grams2 = [i for i in grams if totgrams[i]>1]
	cograms2.append((co,grams2))

with open("vctree/cograms2.p","w") as f:
	pickle.dump(cograms2,f)	
	
cograms3 = []
for co,grams in cograms:
	grams3 = [i for i in grams if totgrams[i]>2]
	cograms3.append((co,grams3))

with open("vctree/cograms3.p","w") as f:
	pickle.dump(cograms3,f)
	
	
totgrams3 = {}
for co,grams in cograms3:
	for gram in grams:
		totgrams3[gram] = totgrams3.get(gram,0) + 1
