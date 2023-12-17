from nltk.corpus import wordnet as wn
from pyvis.network import Network
net = Network()


max_d=int(input("depth: "))

wrd = input("word: ")
wrd = wn.morphy(wrd)
syns = wn.synsets(wrd)
syn = wn.synset(syns[0].name())
net.add_node(wrd, size=10, label=wrd, title=wrd, color="#000064")

def graph_word(word,root_id,depth):
	wd = wn.morphy(word)
	print(wd)
	print(wn.synsets(word))
	if not wd==None:
		syns = wn.synsets(wn.morphy(word))
		for a in syns:
			syn = wn.synset(a.name())
			synonyms = {}
			for s in wn.synonyms(word):
				for i in s:synonyms[i] = syn.path_similarity(wn.synset(wn.synsets(i)[0].name()))
			hypernyms = {}
			for h in syn.hypernyms():
				hn = h.name()
				hypernyms[hn.split(".")[0]] = syn.path_similarity(wn.synset(hn))
			hyponyms = {}
			for i in syn.hyponyms():
				j = i.name()
				hyponyms[j.split(".")[0]] = syn.path_similarity(wn.synset(j))
			holonyms = {}
			for l in syn.member_holonyms():
				m = l.name()
				holonyms[m.split(".")[0]] = syn.path_similarity(wn.synset(m))

			print("synonyms: ",synonyms)
			print("hypernyms: ",hypernyms)
			print("hyponyms: ",hyponyms)
			print("holonyms: ",holonyms)

			
			for s in synonyms:
				new = not s in net.get_nodes()
				if new:
					net.add_node(s, size=5, label=s, title="synonym", color="#"+str(64+141414*depth))
				w = round(synonyms[s],4)
				net.add_edge(s, root_id, label=str(w), width=w*5)
				if new and depth<max_d:graph_word(s,s,depth+1)
			for h in hypernyms:
				new = not h in net.get_nodes()
				if new:
					net.add_node(h, size=5, label=h, title="hypernym", color="#"+str(64+140000*depth-14*depth))
				net.add_edge(h, root_id, width=0.1)
				if new and depth<max_d:graph_word(h,h,depth+1)
			for h in hyponyms:
				new = not h in net.get_nodes()
				if new:
					net.add_node(h, size=5, label=h, title="hyponym", color="#00"+str(64+1400*depth-14*depth))
				net.add_edge(h, root_id, width=0.1)
				if new and depth<max_d:graph_word(h,h,depth+1)
			for h in holonyms:
				new = not h in net.get_nodes()
				if new:
					net.add_node(h, size=5, label=h, title="holonym", color="#"+str(64+141400*depth-14*depth))
				net.add_edge(h, root_id, width=0.1)
				if new and depth<max_d:graph_word(h,h,depth+1)

net.toggle_physics(False)
net.set_edge_smooth('straightCross')
graph_word(wrd,wrd,1)
net.show('syngraph.html',notebook=False)