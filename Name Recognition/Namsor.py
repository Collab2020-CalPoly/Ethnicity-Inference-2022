from csv import reader
 
'''
Hey, sorry for the not optimized / messy / jumbled code. I wanted to keep all iterations of code in here
in case they proved useful. I used this file originally to get all of the names from the initial file
of all the professors to put in a Pandas dataframe, then adapted the parsing to help normalize all the results
into the four groups (white, black, asian, other) and to help build a confusion matrix for each functions results.
Currently, the executed code will help build some the confusion matrix.
'''
 
def map_func(item):
    if not item.strip().isnumeric():
        return "\'" + item.strip() + "\'"
    else:
        return item.strip()
 
def main():
    name = "Results_Comparison_Verify"
    #with open(name+".out", 'w') as f:
    with open(name+'.out', 'w') as f:
        #with open("testGroup_lastfirst.csv")
        with open(name+'.csv', 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            col_names = []
            col_names_str = ""
            # all single character variables and respective counts were for the confusion matrix to see per "verified" race group, what the certain function predicted across all groups
            a = 'asian'
            b = 'black'
            o = 'other'
            w = 'white'
            wcount = 0
            bcount = 0
            acount  = 0
            ocount = 0
            for index, row in enumerate(csv_reader):
                # row variable is a list that represents a row in csv
                real = row[17] # reading from results_comparison_verify.csv, column 'Drew Verify Photos'
                pred = row[15] # individual function's results, for example row[15] is the prediction from NamSor
                if len(row) == 0:
                    continue
                if index == 0:
                   col_names_str = ', '.join(row).strip()
                   #print(row[17])
                else:
                    #if index == 1:
                    #print(index, row[4], row[5])
                    #row = map(map_func, row)
                    #writeLineToFile(col_names_str, name, ', '.join(row).strip(), f)
                    #writeLineToML(row[0], row[1], f)
                    #writeRace(row[5], row[9], row[13], row[17], f)
                    #namSor(row[5], row[4], f)
                    #if (len(row[17]) == 5):
                        #count += 1
                    #elif (len(row[17]) > 5):
                        #print(row[17])
                    #print(row[2], row[3])
                    #print("'%s'" %(row[3]))
                    #if 'white' == row[3] and row[17] == 'white':
                    #    count += 1
                    #if len(row[17]) == 5:
                    #    count += 1
                    if len(real) == 5 and real == o:
                        if pred == w:
                            wcount += 1
                        if pred == b:
                            bcount += 1
                        if pred == a:
                            acount += 1
                        if pred == o:
                            ocount += 1
            print("w: %d, b: %d, a: %d, o: %d" %(wcount, bcount, acount, ocount))
 
 
# used to rewrite the output from NamSor's predictions into more readable strings
def namSor(topRace, secRace, fd):
    if (topRace == "B_NL"):
        topRace = "black\n"
    elif (topRace == "W_NL"):
        topRace = "white\n"
    elif (topRace == "A"):
        topRace = "asian\n"
    elif (topRace == "HL"):
        topRace = "other\n"
 
    fd.write(topRace)
 
 
# used for renormalizing all results to get the highest confident prediction from all of the means
def writeRace(asian_mean, black_mean, white_mean, other_mean, fd):
    #max_mean = max(asian_mean, black_mean, white_mean, other_mean)
    if (asian_mean > black_mean and asian_mean > white_mean and asian_mean > other_mean):
        fd.write("asian\n")
    elif (black_mean > asian_mean and black_mean > white_mean and black_mean > other_mean):
        fd.write("black\n")
    elif (white_mean > asian_mean and white_mean > black_mean and white_mean > other_mean):
        fd.write("white\n")
    elif (other_mean > asian_mean and other_mean > black_mean and other_mean > white_mean):
        fd.write("other\n")
    else:
        fd.write("SAME\n")
 
 
# used for creating the Pandas dataframes
def writeLineToML(first, last, file_d):
    #str = "INSERT INTO %s (%s) VALUES (%s);" % (table_name, col_names_str, vals)
    str = "{\'first\': \'%s\', \'last\': \'%s\'}, " % (first, last)
    file_d.write(str)
    #file_d.write(str+"\n")

 
 
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
 
# See PyCharm help at https://www.jetbrains.com/help/pycharm/