
from neo4j import GraphDatabase, basic_auth
import pandas as pd
# 1. build neo4j knowledge graph datasets
driver = GraphDatabase.driver(
  "bolt://18.205.161.69:7687",
  auth=basic_auth("neo4j", "nickel-slinging-midwatches"))

session = driver.session()

session.run("MATCH (n) DETACH DELETE n")# clean all

# read triples
df = pd.read_csv('./data/chatdoctor5k/train.txt', sep='\t', header=None, names=['head', 'relation', 'tail'])

i = 0
for index, row in df.iterrows():
	print(i)
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