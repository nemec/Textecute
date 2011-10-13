#Inserts your specified text into a "memo" textfile
def execute(arg = ''):
    f = open("/home/dan/doc/memo" , "a")
    if arg != '':
        f.write(arg+"\n")
    f.close()
    return "Inserted into memo file."
