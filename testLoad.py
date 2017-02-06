import os, shutil, json, re, csv
import sys, traceback, datetime, time, math
from smellSurvey.models import * 

def checkIfParentInPath(parentFlag, question, parentQuestion):  
    
    try:
	
	print ( " *** &&&&&&  in checkIfParentInPath = " + str(question.questionId) + "::" + str(question) + " parent = " + str(parentQuestion.questionId) + "::" + str(parentQuestion) + " parent flag = " + str(parentFlag) ) 	
	
	if question.parent is None:
	    
	    #print ( " *** ^^^^^ no parent !!!! ))) " + " return " + str(parentFlag) ) 

	    return parentFlag
	
	print ( " $$ ----- $$ compare " + str( question.parent.questionId ) + " and parent = " + str(parentQuestion.questionId) ) 
	
	if question.parent.questionId == parentQuestion.questionId:
	    
	    parentFlag = True
	    
	    print ( " *** ^^^^^ FOUND PARENT!!! = " + str(parentQuestion.questionId) + "::" + str(question.parent) + " return " + str(parentFlag)) 	    
	    
	    return parentFlag
	
	else:
	    
	    question = question.parent
	    
	    return checkIfParentInPath(parentFlag, question, parentQuestion)
	
    except:
	
	traceback.print_exc(file=sys.stdout)
	
    print ( " $$$$$$$$ in end return " + str(parentFlag) ) 
	
    return parentFlag

def navigateSection(question, section, originalQuestion):  
    
    try:
        
	print ( " @@@@@@@@@@ in navigate questionnaire for question = " + str(question.questionId) + "::" + str(question) ) 
        
	questions = Question.objects.filter (questionId__gt = question.questionId, section = section).exclude(parent = question)

	if len ( questions ) == 0:
	    
	    #print ( " !!!! 111 returning = " ) 
	    
	    return ''

	nextQuestion = questions[0]
	
	parentFlag = False
	
	parentFlag = checkIfParentInPath(parentFlag, nextQuestion, originalQuestion)
	
	print ( " parentFlag *** = " + str(parentFlag))
	
	if not parentFlag:

	    print ( " !!!! 222 returning = " + str(nextQuestion) ) 

	    return nextQuestion
	
	else:
	    
	    #print ( " &&&&& 3333 parentFlag = " + str(parentFlag) )  	    
	    
	    return navigateSection(nextQuestion, section, originalQuestion)	    
			
    except:
        
        traceback.print_exc(file=sys.stdout)
        
    #print ( " && 44444 parentQuestion = " + str(parentQuestion) )  

    return nextQuestion    

question = Question.objects.filter (questionId = 401)[0]

section = question.section

originalQuestion = question

nextQuestion = navigateSection ( question, section, originalQuestion )

print ( " nextQuestion = " + str ( nextQuestion )  ) 

## this treats the OWL file as a XML file, finds the values and populates a neo4j DB
#def testXML():  
    
    #try:

        #tree = ET.parse('smellSurvey.owl')
        #root = tree.getroot()
        
        #driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j"))
        #session=driver.session()
        
        #outCypherFile = open("outCypher.txt" , "w")
        
        #nodeList = []
        #subClassMap = {}
        #valueMap = {}
        #annotationMap = {}

        #for elem in tree.iter():
            
             #if elem.tag.find("Declaration") != -1:

                #for index, child in enumerate(elem):
                     
                     #if child.tag.find("NamedIndividual") != -1:

                        #entity = child.attrib["IRI"][1:]
                        
                     #elif child.tag.find("Class") != -1:
 
                        #entity = child.attrib["IRI"][1:]
                    
                #nodeList.append(entity) 

                     ##print ("CREATE (" + entity + ":NodeName {name: '" + entity + "' })")
                    
                     ##outCypherFile.write("CREATE (" + entity + ":NodeName {name: '" + entity + "' })\n")

                    ##session.run("CREATE (" + entity + ":NodeName {name: '" + entity + "' })")   
            
             #elif elem.tag.find("SubClassOf") != -1:                 

                 #childClass = ""
                 #parentClass = ""

                 #for index, child in enumerate(elem):
                     
                     #if child.tag.find("Class") != -1:
                         
                         #if index == 0:
                             #childClass = child.attrib["IRI"][1:]
                         #elif index == 1:
                             #parentClass = child.attrib["IRI"][1:]
                             
                 #if childClass != '' and parentClass != '': 
                    
                     #print ("CREATE (" + childClass + ")-[:IS_SUBCLASS] -> (" + parentClass +")")    
                     
                     #subClassMap [childClass] = parentClass                     
                     
                     #outCypherFile.write("CREATE (" + childClass + ")-[:IS_SUBCLASS] -> (" + parentClass +")\n")
                     
                     ##session.run("CREATE (" + childClass + ")-[:IS_SUBCLASS] -> (" + parentClass +")")   
                     
                     #subClassMap [childClass] = parentClass                     

             #elif elem.tag.find("ClassAssertion") != -1:                 

                #className = ""
                #namedIndividual = ""

                #for index, child in enumerate(elem):
                    
                    #if child.tag.find("Class") != -1:
                        
                        #className = child.attrib["IRI"][1:]
                    
                    #elif child.tag.find("NamedIndividual") != -1:
                        
                        #namedIndividual = child.attrib["IRI"][1:]
                            
                #if className != '' and namedIndividual != '' : 
                    
                    #print (" child tag = " + str(child.tag) )
                    #print (" child attrib = " + str(child.attrib) )             
                    #print (" child text = " + str(child.text) )                     
                            
                    ##session.run("CREATE (" + childClass + ")-[:IS_SUBCLASS] -> (" + parentClass +")")   
                   
                    ##print ("CREATE (" + namedIndividual + ")-[:IS_VALUE_OF] -> (" + className +")")
                    
                    ##outCypherFile.write("CREATE (" + namedIndividual + ")-[:IS_VALUE_OF] -> (" + className +")\n")
                    
                    #valueMap [className] = namedIndividual                    
                    
            ##<AnnotationAssertion>
                ##<AnnotationProperty abbreviatedIRI="rdfs:seeAlso"/>
                ##<IRI>#hemorrhagic_stroke</IRI>
                ##<Literal datatypeIRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral">Onoda K, Ikeda M, Sekine H, Ogawa H. Clinical study of central taste disorders and discussion of the central gustatory pathway.J Neurol. 2012 Feb;259(2):261-6.</Literal>
            ##</AnnotationAssertion>                    
        
             #elif elem.tag.find("AnnotationAssertion") != -1:                 

               #valueName = ""
               #reference = ""

               #for index, child in enumerate(elem):
                   
                   #if child.tag.find("IRI") != -1:
                       
                       #valueName = child.text[1:]
                   
                   #elif child.tag.find("Literal") != -1:
                       
                       #reference = child.text
                           
               #if className != '' and reference != '' : 
                   
                   #print (" child tag = " + str(child.tag) )
                   #print (" child attrib = " + str(child.attrib) )             
                   #print (" child text = " + str(child.text) )                     
                           
                   ##session.run("CREATE (" + childClass + ")-[:IS_SUBCLASS] -> (" + parentClass +")")   
                  
                   ##print ("CREATE (" + reference + ")-[:IS_REFERENCE_OF] -> (" + className +")")
                   
                   ##outCypherFile.write("CREATE (" + namedIndividual + ")-[:IS_VALUE_OF] -> (" + className +")\n")
                   
                   #annotationMap [valueName] = reference

        #outCypherFile.close()
        
    #except:
        
        #traceback.print_exc(file=sys.stdout)
        
    #return    

## add patients
#def testEnterPatients():  
    
    #try:

        #tree = ET.parse('smellSurvey.owl')
        #root = tree.getroot()
        
        #patientNames = ["Patient 1", "Patient 2", "Patient 3"]

        #patientsWithAnosmia = ["Patient 1", "Patient 3"]
        
        #driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j"))
        #session=driver.session()

        #for patientName in patientNames:
                 
            #session.run("""CREATE (patient:Patient {name:{patientNameNeo4j}})", {"patientNameNeo4j": patientName}""")
                            
        #for patientWithAnosmia in patientsWithAnosmia:

            #session.run("""MATCH  (patient:Patient {name:""" + patientWithAnosmia + """})
                        #CREATE (patientName)-[hasDisorder:HASDISORDER]->(anosmia:Disorder {disorderName:"anosmia" })
                        #RETURN patient,hasDisorder,anosmia""")  

    #except:
        
        #traceback.print_exc(file=sys.stdout)
        
    #return 

## neo4j relationships
#def testNeo4jRelationships():  
    
    #try:

       ##db = GraphDatabase("http://localhost:7474", username="neo4j", password="neo4j")
       
       #db = GraphDatabase.driver("bolt://localhost:7474/db/data/")
       
       ##db = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j"))       
        
       ## Create some nodes with labels
       #user = db.labels.create("User")
       #u1 = db.nodes.create(name="Marco")
       #user.add(u1)
       #u2 = db.nodes.create(name="Daniela")
       #user.add(u2)
        
       #beer = db.labels.create("Beer")
       #b1 = db.nodes.create(name="Punk IPA")
       #b2 = db.nodes.create(name="Hoegaarden Rosee")
       ## You can associate a label with many nodes in one go
       #beer.add(b1, b2)  
       
       ## User-likes->Beer relationships
       #u1.relationships.create("likes", b1)
       #u1.relationships.create("likes", b2)
       #u2.relationships.create("likes", b1)
       ## Bi-directional relationship?
       #u1.relationships.create("friends", u2)   
       
       #q = 'MATCH (u:User)-[r:likes]->(m:Beer) WHERE u.name="Marco" RETURN u, type(r), m'
       ## "db" as defined above
       #results = db.query(q, returns=(client.Node, str, client.Node))
       #for r in results:
           #print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))       

    #except:
        
        #traceback.print_exc(file=sys.stdout)
        
    #return    

## neo4j relationships
#def testPy2Neo():  
    
    #try:

        #graph = Graph()
        
        #tx = graph.cypher.begin()
        #for name in ["Alice", "Bob", "Carol"]:
            #tx.append("CREATE (person:Person {name:{name}}) RETURN person", name=name)
        #alice, bob, carol = [result.one for result in tx.commit()]
        
        #friends = Path(alice, "KNOWS", bob, "KNOWS", carol)
        #graph.create(friends)    

    #except:
        
        #traceback.print_exc(file=sys.stdout)
        
    #return

## This does not work as the OWL format is not valid

#def testRdf():  
    
    #try:
        
        #driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j"))
        #session=driver.session()

        #g = Graph()
        #g.parse('smelldisorder_rdf.rdf')
        
        #query = """SELECT * WHERE { ?s ?p ?o . } """
        
        #print ("")
            
        #for index, row in enumerate(g.query(query)):
            
            #if index > 100:
                
                #break
            
            #subject = row[0] [ row[0].find("#") +1:]

            #objectValue = row[1][ row[1].find("#") +1:]

            #predicate = row[2][ row[2].find("#") +1:]
            
            #print ( "subject: " + subject + " -- object: " + objectValue + " -- predicate: " + predicate)
            
            ##if subject.find("profession") != -1 or objectValue.find("profession") != -1 or predicate.find("profession") != -1:

                ##print ( subject, objectValue, predicate)               

                ##if str(subject) == "type":

            
                    ##session.run("""CREATE (a:ProfessionType { professionName:""" + objectValue + """})-[r:TYPE_OF]->(m:ProfessionNode{ nodeName:""" + predicate + """})""")
                    
                    ##print ("CREATE (a:ProfessionType { professionName:" + objectValue + "})-[r:TYPE_OF]->(m:ProfessionNode{ nodeName:" + predicate + "})")
            
                    ##print ( subject, objectValue, predicate)            
                
                    ##print ("")

    #except:
        
        #traceback.print_exc(file=sys.stdout)
        
    #return  

##loadQuestionnaire()

##testRdf()

#testXML()

##testNeo4jRelationships()

##testPy2Neo()

##testEnterPatients()