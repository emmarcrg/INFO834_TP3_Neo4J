from neo4j import GraphDatabase

class API : 
    '''
    Cette classe définit l'ensemble de l'API, par définition, lorsqu'on la lance, elle lance le driver 
    '''
    def __init__ (self, mdp):
        # On lance le driver et une session
        uri = "neo4j://localhost:7687"
        
        # Connexion au driver 
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", mdp))
        self.session = self.driver.session()
    
    def createTable (self,type, noms, links, type_link): 
        '''
        type : le type de l'objet que nous créons => string
        noms : nom du ou des objet que nous créons => dictionnaire
        links : ensemble des liens que nous créons => dictionnaire
        type_link : type du lien qui relie nos objets => string ; les liens sont supposés réciproques
        '''
        self.type_link = type_link
        nodes = []

        # Construire les nœuds
        for nom in noms:
            simple_name=nom.split('-')[0]
            nodes.append(f"({simple_name}:{type} {{ name: '{nom}'}})")
            
        # Joindre les nœuds et relations avec des virgules
        cqlCreate = "CREATE " + ", ".join(nodes)
        print(cqlCreate)
        
        self.session.run(cqlCreate)
    
    def setLiens(self, links, type_link):
        relationships = []
        # Construire les relations
        for link in links:
            relationships.append(f"({link})-[:{type_link} {{{type_link}: {links[link][1]}}}]->({links[link][0]})")
        
        cqlCreate = "CREATE " + ", ".join(relationships)
        print(cqlCreate)
        
        self.session.run(cqlCreate)
        
    def getalldata(self, type):
        cqlGetAll = f"MATCH (x:{type}) RETURN x.name"
        print(cqlGetAll)
        data = self.session.run(cqlGetAll)
        return data

    def getEdge (self, type, universite):
        cqlGetEdge = "MATCH (x:"+type+" {name:'"+universite+"'})-[r]->(y:university) RETURN y.name"
        print(cqlGetEdge)
        data = self.session.run(cqlGetEdge)
        return data

    def close_connection(self): 
        # Ferme la session et le driver
        self.session.close()
        self.driver.close() 

if __name__ == '__main__':
    # On cache le mot de passe
    with open('logs.txt', 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            mdp = ligne
    api = API(mdp)
    '''
    api.createTable("university", 
                    {"cornell": "Cornell University", "yale": "Yale University", "princeton": "Princeton University", "harvard": "Harvard University"}, 
                    { "cornell" : ("yale", 259),  "cornell" : ("princeton", 210),  "cornell" : ("harvard", 327),
                     "yale" : ("cornell", 259),  "yale" : ("princeton", 133),  "yale" : ("harvard", 133),
                     "harvard" : ("cornell", 327),  "harvard" : ("princeton", 260),  "harvard" : ("yale", 133),
                     "princeton" : ("cornell", 210),  "princeton" : ("harvard", 260),  "princeton" : ("yale", 133)}, 
                    "connects_in")
    
    print("Obtention de toutes les données")
    all = api.getalldata("university")
    for node in all :
        print(node)
    
    print("Obtention des edges avec Harvard")
    spec = api.getEdge("university", "Harvard University")
    for node in spec :
        print(node)'''
        
    
    api.close_connection()