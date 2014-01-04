import pickle
outfile = open("cograms.txt","w")
vcs = pickle.load(open("cograms.p", "rb"))
outfile.write(str(vcs))
