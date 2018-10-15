# ChEMBL
**Pre-requisites**: 

1. MySQL installed in your local system. 
2. Neo4J-Desktop App installed in your local system. (refer https://neo4j.com/ if you have any queries)
3. Install py2neo using the command (sudo pip install py2neo).

**Step-1**: Download the Chembl_24 database and load the dump file into Mysql in your local system.

**Step-2**: Run mytocsv.py file in the terminal 

(This will create the CSV files with required columns. The required columns list should be in sch.txt file)

**Note**: Change the user, password and db according to your MySQL information.

**Step-3**: Open Neo4j-Desktop and create new graph and hit manage. Go to the settings and change the following lines.

1. Uncomment this line "dbms.directories.import=import"
2. Change the value of this line "dbms.security.auth_enabled=false" to true.
3. Change the value of this line "dbms.memory.heap.max_size=1G" to 40G
4. Add this line "dbms.security.allow_csv_import_from_file_urls=true"

Now, start the graph.

**Step-4**: Run graphs.py file (Before that comment the line relationship() at the end of the page.)

**Step-5**: After execution uncomment relationship() and comment export() and run the file again.

**Note**: This may take some time.

After the execution of that file, the data we require is loaded into Neo4J. Now, you can play with the graph by giving Cypher commands.

The Cypher commands to get particular data corresponding to each drug in https://www.ebi.ac.uk/chembl/drugstore are there in commands.txt file.