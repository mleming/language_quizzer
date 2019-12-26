#!/usr/bin/python

# Pretty simple. Get a CSV, with the first column being non-English-language
# words and the second being English language definitions. This will present
# words to you, you type in the definition, and it'll cycle through. You are
# shown words in blocks; if you get a word correct enough times, it is taken
# off the queue and you are given a new word. This saves your progress in a 
# json file. If you want to start anew, just delete the json file.
# With English definitions, this tries to be smart about accepting flexible
# input, but it's not exact. Typing out the exact definition word-for-word
# should work.
# To use, run: python language_quizzer.py <csv_definitions_file.csv>

import os,sys,csv,random,re,hashlib,json
import unicodedata as ud

blocksize           = 25 # Maximum position a word is pushed back in the queue
		         # if you get it wrong or haven't gotten it right enough
guess               = 2  # Number of times in a row you need to get the word
                         # correct before it's taken off the queue
quiz_type           = "english" # "english","foreign","random"
                         # If random, you need to type it out enough times in
                         # both languages in order for it to be taken off the
                         # queue. If foreign or random, make sure you have a
                         # sticky key set to change between the english keyboard
                         # and the foreign language keyboard if the alphabet is
                         # different.

csv_words_filename = sys.argv[1]
hashcache = "progress_%s.json" % (hashlib.md5(csv_words_filename.encode()).hexdigest())

wordlist = []

try:
	with open(hashcache) as file:
		wordlist = json.load(file)
	print "Loaded wordlist from cache"
except:
	with open(csv_words_filename) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',',quotechar='"')
	    for row in csv_reader:
		wordlist.append([row[0],row[1],guess-1,guess-1])
	random.shuffle(wordlist)
	with open(hashcache,'w') as outfile:
		json.dump(wordlist, outfile)
	print "Cached wordlist"

def get_correct_responses(definition):
	correct_responses = [definition]
	definition = re.sub(r' *\([^)]*\) *', '', definition)
	correct_responses.append(definition)
	for d in definition.replace(";",",").split(","):
		d = d.lstrip().rstrip()
		correct_responses.append(d)
		if "to " in d:
			correct_responses.append(d.replace("to ",""))
	return correct_responses

while len(wordlist) > 0:
	w = wordlist[0]
	if quiz_type == "foreign":
		non_english = True
	elif quiz_type == "english":
		non_english = False
	elif quiz_type == "random":
		non_english = random.choice([True,False])
	else:
		raise Exception('Invalid quiz_type option: %s' % quiz_type)
	if w[2 + (non_english)] >= guess and quiz_type == "random":
		non_english = not non_english
	print w[non_english]
	correct_responses = get_correct_responses(w[not non_english])
	response = raw_input("Input: ")
	if response.decode('utf-8') in correct_responses:
		w[2 + (non_english)] += 1
		print "%.5d, Correct (%s)" % (len(wordlist),w[not non_english])
	else:
		w[2] = 0
		w[3] = 0
		print "%.5d, Wrong (%s)" % (len(wordlist),w[not non_english])
	del wordlist[0]
	if ((w[2] < guess or w[3] < guess) and quiz_type == "random") or\
		(w[2] < guess and quiz_type == "english") or\
		(w[3] < guess and quiz_type == "foreign"):
		wordlist.insert(min(random.randint(min(10,blocksize),blocksize),len(wordlist)),w)
	with open(hashcache,'w') as outfile:
		json.dump(wordlist, outfile)
	
