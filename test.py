from neo4j import GraphDatabase
import pandas as pd
from tqdm import tqdm

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12341234"

driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session()


##############################build KG 

session.run("MATCH (n) DETACH DELETE n")# clean all

# read triples
df = pd.read_csv('./data/chatdoctor5k/train.txt', sep='\t', header=None, names=['head', 'relation', 'tail'])

len = len(df)
i = 1

for index, row in df.iterrows():
	print(i,"/",len)
	head_name = row['head']
	tail_name = row['tail']
	relation_name = row['relation']

	query = (
		"MERGE (h:Entity { name: $head_name }) "
		"MERGE (t:Entity { name: $tail_name }) "
		"MERGE (h)-[r:`" + relation_name + "`]->(t)"
	)
	session.run(query, head_name=head_name, tail_name=tail_name, relation_name=relation_name)
	i += 1