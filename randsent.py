from collections import defaultdict
import random
import sys
import argparse

parser = argparse.ArgumentParser(description="enable tree mode")
parser.add_argument('filename',type=str,help='name of grammar file to use')
#parser.add_argument('--t',

if sys.argv[1] == "-t":
	tree_mode=1
	filename = sys.argv[2] 
	num_sents = int(sys.argv[3])
else:
	tree_mode = 0
	filename = sys.argv[1] 
	num_sents = int(sys.argv[2])

#open grammar file
f = open(filename,'r')
d = defaultdict(list)
dp = defaultdict(list)
s=[]

#create grammar hash table
for line in f:
	code = line.split("#")[0].split()
	if code:
		#OLD: s.append([code[1],code[2:]])
		s.append([code[0],code[1],code[2:]])
for p,k,v in s:
	d[k].append(v)		#d  is hash with keys=LHS and vals=list of possible RHS
	dp[k].append(float(p))	#dp is hash with keys=LHS and vals=list of possible RHS's odds (not probability)

def weighted_choice(weights):
#returns index of weights chosen at random using vals of weights as pseudo-probability
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i
	
def node(l):
	RHS = d[l][weighted_choice(dp[l])]	#choose a random rhs given lhs
	#print "RHS=",RHS
	temp=""
	tree=[]
	if tree_mode ==1:
		tree.append(l)
		
	for r in RHS:
		#if r is not in d, it is terminal
		if r not in d:
			if tree_mode == 1:
				tree.append(r)
			else:	
				temp += (r + " ")	#it is safe to put a space after a terminal (necessary?)

		else:
			if tree_mode == 1:
				tree.append(node(r))
			else:	
				temp += node(r)
	if tree_mode == 1:
		return tree
	else:
		return temp 

for h in range(num_sents):
	sentence = node("START")
	print "h=",h,sentence
