from neo4j import GraphDatabase

uri = "neo4j://TP3:7474"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

driver.close() 