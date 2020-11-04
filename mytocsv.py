import pymysql

def execute(c, command):
    c.execute(command)
    return c.fetchall()

db = pymysql.connect(host='localhost', user='gill', passwd='welc0me#', db='chembl_27', charset='utf8')

c = db.cursor()

def export():
    file1 = open("sch.txt","r+")
    lines = file1.readlines()
    for line in lines:
        line = line.replace('\n',' ')
        line = line.strip()
        line = line.split(' ')
        for table in execute(c, "show tables;"):
            if line[0] == table[0]:
                line.pop(0)
                print(line)
                for l in line:
                    print(l.split('\t'))
                data1=""
                for j in line:
                    if(len(j.split()) == 1):
                        data1 = data1 + j + ", "
                        print("bb ", j)
                    else:
                        print("kk ", len(j.split()))
                        for k in j.split():
                            print ("-->", k)
                            data1 = data1 + k + ", "
                print("data :", data1[:-2])
                data = execute(c, "select " + data1[:-2] + " from " + table[0] + ";")
                #data = execute(c, "select *" + " from " + table[0] + ";")
                #print(data)
                with open(table[0] + ".csv", "w") as out:
                    out.write("\t".join(line) + "\n")
                    for row in data:
                        out.write("\t".join(str(el) for el in row) + "\n")
                    print(table[0] + ".csv written")

export()
