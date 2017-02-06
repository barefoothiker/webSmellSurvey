from neo4j.v1 import GraphDatabase, basic_auth


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j"))

session=driver.session()

for name in ["Alice", "Bob", "Carol"]:
    session.run("CREATE (person:Person {name:{name}}) RETURN person", name=name)
