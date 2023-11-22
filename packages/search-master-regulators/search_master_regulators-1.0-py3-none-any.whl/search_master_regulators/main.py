import argparse
import networkx as nx
import pandas as pd
import os, pathlib

#function to check if file exists
def checkFiles(network, geneFile):
	if os.path.exists(network) == False:
		print(f"file {network} can not be found.")
		exit()
	if os.path.exists(geneFile) == False:
		print(f"file {geneFile} can not be found.")
		exit()

#function that check and, if it do not exist, create output folder
def makeOutput(output):
	if os.path.exists(output) == False:
		try:
			os.makedirs(output)
		except:
			print(f"Failed to make folder {output}. Exiting")
			exit()

#function to parse the GRN net
def read_grn(file):
	G = None
	if file.endswith(".gml") or file.endswith(".GML"):
		G = nx.read_gml(file)
	else:
		sep = ","
		if file.endswith(".tsv") or file.endswith(".TSV") :
			sep = "\t"
		df = pd.read_csv(file, sep=sep, header = None)
		G = nx.DiGraph()
		for i, tf in enumerate(df[0]):
			G.add_edge(tf, df[1][i])
	return G

#function to read the DE gene list
def parseDE(file):
	toReturn = []
	with open(file, "r") as f:
		toReturn = [gene[:-1] for gene in f]
	if len(toReturn) == 0:
		print("No DE Genes were provided. Remember it is a one column based file")
		exit()
	return toReturn

#function to check if DE genes are in the net
def checkDEGinGRN(GRN, DEGenes):
	notInGRN = [gene for gene in DEGenes if gene not in list(GRN.nodes())]
	if len(notInGRN) == len(DEGenes):
		print("No DE genes are in the Gene Regulatory Network. Exiting")
		exit()
	if  len(notInGRN) > 0:
		print(f"The following genes are not present in the regulatory network: {str(notInGRN)[1:-1]} ({len(notInGRN)/len(DEGenes) * 100}%)")
	return [gene for gene in DEGenes if gene in list(GRN.nodes())]

#function that looks for predecessors of DE genes
def	getSubnet(GRN, DEGenes, pred):
    #the idea is to have a list (finalNodes) that starts as a copy of DEGenes. 
	#then for each node we will loop for its predecessors and append to the list. 
	# this step is performed n times, with n equals to pred as defined in the options menu
	#
	finalNodes = DEGenes.copy()
	i = 0
	while i < pred:
		for node in finalNodes:
			predecessors = GRN.predecessors(node)
			for predecessor in predecessors:
				if predecessor not in finalNodes:
					finalNodes.append(predecessor)
		i += 1
	subNet = GRN.subgraph(finalNodes)
	return subNet

#function to search for the strong connected components
def strong_connected(GRN):
	toReturn = []

	#first step: make a new grn without nodes with outdegree = 0, cause we only wants TFs directing gene expression
	nodesToKeep = [node for node in GRN.nodes() if GRN.out_degree(node) > 0]
	net = GRN.subgraph(nodesToKeep)

	#second step, loop over each weakly connected component, make a new subgraph and apply kosarajus algorithm to get strongly connected components
	for nodes in nx.weakly_connected_components(net):
		subNet = net.subgraph(list(nodes))
		#now kosaraju's, saving the largest strongly connected component
		toReturn.append(max(nx.kosaraju_strongly_connected_components(subNet), key=len))
	
	if len(toReturn) == 0:
		print("There are not strongly connected components. Exiting")
		exit()
	return toReturn

#function to parse the ppi net
def read_ppi(file):
	G = None
	if file.endswith(".gml") or file.endswith(".GML"):
		G = nx.read_gml(file)
	else:
		sep = ","
		if file.endswith(".tsv") or file.endswith(".TSV") :
			sep = "\t"
		df = pd.read_csv(file, sep=sep, header = None)
		G = nx.DiGraph()
		for i, tf in enumerate(df[0]):
			G.add_edge(tf, df[1][i])
	return G
#binarizer function
def binarize(df, threshold=0):
    df2 = df.copy()
    for col in df.columns:
        df2.loc[df2[col] <= threshold, col] = 0
        df2.loc[df2[col] > threshold, col] = 1
    return df2

def main():
	parser = argparse.ArgumentParser(prog='search_master_regulators', description='A Python script to derive Master Regulators based on David & Rebay work', epilog='Developed by Sebastian Contreras-Riquelme (github.com/Cold7)')
	parser.add_argument("-g","--genes", help="Path to a file (one column format) with Differentially Expressed Genes", required=True)
	parser.add_argument("-n","--network", help="Path to Gene Regulatory Network file. Available formats are GML or two column (TF - Gene) as TSV or CSV. No header is mandatory", required = True)
	parser.add_argument("-u","--upstream", help="Number of upstream TF of DE genes to be considered. Default: 1", type=int, default=1)
	parser.add_argument("-p","--ppi", help="Protein Protein Interaction network file. Available formats are GML or two column (TF - Gene) as TSV or CSV. No header is mandatory", required = True)
	parser.add_argument("-o","--output", help="Path for output files. If path do not exists, then it will be created. Default "+str(pathlib.Path.home())+"/MRs_output", default=str(pathlib.Path.home())+"/MR_output")

	args = parser.parse_args()

	#checking files
	print("Checking input files")
	checkFiles(args.network, args.genes)
	
	#making output folder
	print("Checking for output folder")
	makeOutput(args.output)
	#loading the GRN 
	print(f"Reading {args.network}")
	GRN = read_grn(args.network)

	#loading DE genes
	print(f"Reading {args.genes}")
	DEGenes = parseDE(args.genes)
	
	#checking if DE genes are in the GRN
	print("Checking DE genes are in the Regulatory Network")
	DEGenesInGRN = checkDEGinGRN(GRN, DEGenes)

	#doing subselection of the DE genes and closest TFs (predecessors)
	print("Extracting subnet")
	subGRN = getSubnet(GRN, DEGenesInGRN, args.upstream)
	#looking for the highly connected subnet and return candidates. 
	print("Getting candidates to be Master Regulators")
	candidates = strong_connected(subGRN) #candidates will be a list of list, cause subGRN could be a weakly conected net
	for i, candidate in enumerate(candidates):
		j = i+1
		print(f"Weakly connected network {j} has {len(list(candidate))} candidates. Saving as {args.output}/candidates_wc_{j}.txt")
		with open(args.output+"/candidates_wc_"+str(j)+".txt", "w") as f:
			for c_ in candidate:
				f.write(c_+"\n")
	#loading the PPI net
	print("Loading the Protein Protein Interaction Network")
	ppi = read_ppi(args.ppi)

	#now, we will do the summary table as davis & rebay, looking if the candidate direct and is directed by other candidate, and if they present a physiscal interaction
	for i, candidate in enumerate(candidates):
		j = i+1
		print(f"Working with candidates of weakly connected network {j}")
		summaryDict = {}
		j = i+1
		print("\tLooking for candidates that direct the expression of other candidate and if they interacts physically")
		for c_ in candidate:
			summaryDict[c_] = {"regulates expresion of another candidate":0,
			"Expression regulated by another candidate":0,
			"Binds another candidate":0
			}
			for c2_ in candidate:
				if subGRN.has_edge(c_,c2_):
					summaryDict[c_]["regulates expresion of another candidate"] += 1
				if subGRN.has_edge(c2_,c_):
					summaryDict[c_]["Expression regulated by another candidate"] += 1
				if ppi.has_edge(c_,c2_):
					summaryDict[c_]["Binds another candidate"] += 1
		df = pd.DataFrame(summaryDict).T
		print(f"\tSaving summary table for the {j} weakly connected network as {args.output}/summary_{j}.csv")
		df.to_csv(args.output+"/summary_"+str(j)+".csv")
		
		#now binarizing the dataframe, and if each gene sums 3, then it is a MR cause it accomplish all the definitions
		df = binarize(df)
		print("Defining Master Regulators")
		MRs = []
		for gene in df.index:
			if sum(df.loc[gene]) == 3:
				MRs.append(gene)
		if len(MRs) == 0:
			print("\tThere are no candidates that fullfil the three conditions.")
		else:
			print(f"\tsaving Master Regulator List on {args.output}/MRs_{j}.txt")
			with open(args.output+"/MRs_"+str(j)+".txt", "w") as f:
				for mr in MRs:
					f.write(mr+"\n")
	print("Done")




if __name__ == "__main__":
	main()
