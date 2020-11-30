from py2neo import Graph, Node, Relationship

EdgeType = dict()
EdgeType["molecule_dictionary", "chembl_id_lookup"] = "has_chembl_id"

EdgeType["compound_records", "molecule_dictionary"] = "has_molecule"
EdgeType["compound_records", "source"] = "has_source"

EdgeType["drug_mechanism", "molecule_dictionary"] = "has_molecule"
EdgeType["drug_mechanism", "target_dictionary"] = "has_target"
EdgeType["drug_mechanism", "compound_records"] = "has_comp_record"

EdgeType["compound_structural_alerts", "molecule_dictionary"] = "has_molecule"
EdgeType["compound_properties", "molecule_dictionary"] = "has_molecule"
EdgeType["molecule_synonyms", "molecule_dictionary"] = "has_molecule"
EdgeType["compound_structures", "molecule_dictionary"] = "has_molecule"

EdgeType["drug_indication", "molecule_dictionary"] = "has_molecule"
EdgeType["drug_indication", "compound_records"] = "has_comp_record"

EdgeType["activities", "assays"] = "has_assay"
EdgeType["activities", "molecule_dictionary"] = "has_molecule"

EdgeType["assays", "chembl_id_lookup"] = "has_chembl_id"
EdgeType["assays", "target_dictionary"] = "has_target"
EdgeType["assays", "source"] = "has_source"

EdgeType["target_dictionary", "chembl_id_lookup"] = "has_chembl_id"

EdgeType["target_components", "target_dictionary"] = "has_target"
EdgeType["target_components", "component_sequences"] = "has_comp_seq"

EdgeType["mechanism_refs", "drug_mechanism"] = "has_drug_mech"

EdgeType["indication_refs", "drug_indication"] = "has_drug_indi"


def exportCSV(file):
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            i = 0
            #query = '''USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///Users/sarvani/Desktop/workspace/chembl/Csv_files/'''
            query = '''USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///chembl27_csv/'''
            for word in line.split():
                if i==0:
                    query = query + word + ".csv\" AS row FIELDTERMINATOR '\t' CREATE (:"+word+"{"
                    i=i+1
                else:
                    query = query + word + ":row." + word + ", "
            query = query[:-2]
            query = query + "});"
            i=0
            graph.run(query)

def deleteProcessed():
    query = "match (n:processed) with n limit 100000 remove n:processed return count(*) as processed"
    if query != "":
        values = graph.run(query).data()
        value = values[0]["processed"]
        while(value==100000):
            values = graph.run(query).data()
            value = values[0]["processed"]

def relationships():
    csv = []
    keys = []
    with open("primarykey.txt") as f:
        lines = f.readlines()
        for line in lines:
            i=0
            for word in line.split():
                if i==0:
                    csv.append(word)
                    i=i+1
                else:
                    keys.append(word)
    with open("sch.txt") as f:
        lines = f.readlines()
        for line in lines:
            i=0
            query = ""
            for word in line.split():
                if i==0:
                    file = word
                    i=i+1
                else:
                    for key in range(0, len(keys)):
                        if keys[key] == word and csv[key]!=file:
                            edge_type = EdgeType[file, csv[key]]
                            print(edge_type, "\n")
                            query = "MATCH (a:"+csv[key] + ") WITH a MATCH (p:" + file + "{" + word + ": a." + word +"} ) WHERE NOT p:processed WITH a, p LIMIT 100000 MERGE (p) - [:" + edge_type + "] -> (a) SET p:processed RETURN COUNT(*) AS processed"
                            print(query)
                            values = graph.run(query).data()
                            print(values)
                            value = values[0]["processed"]
                            print(value)
                            while(value==100000):
                                print(value)
                                values = graph.run(query).data()
                                value = values[0]["processed"]
                            print(value)
                            deleteProcessed()
                            print("Deleted processed")
                            print(csv[key] + word)

def delete():
    #query = "MATCH ()-[r:child_of]-() with r limit 100000 DELETE r return count(r) as deletedrelations"
    query = "MATCH ()-[]-() with r limit 100000 DELETE r return count(r) as deletedrelations"
    if query != "":
        values = graph.run(query).data()
        value = values[0]["deletedrelations"]
        while(value==100000):
            values = graph.run(query).data()
            value = values[0]["deletedrelations"]
            print(value)
        print("deleted")

graph = Graph()
#exportCSV("sch.txt")
relationships()
#delete()
