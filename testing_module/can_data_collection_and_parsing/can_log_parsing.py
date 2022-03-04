'''
This module will take raw log data from .txt file and
will output the processed data in a .csv file
'''

import codecs
import csv
from .stark_parser import stark_parser_function

def parse_can_data():

    with codecs.open("testing_module/can_data_collection_and_parsing/can_data.txt", "r", "UTF8") as inputFile:
        inputFile = inputFile.readlines()


    can_ids = []
    can_data = []

    for line in inputFile:
        req = []
        req = [s for s in line.split(" ") if s != ""]
        can_ids.append(req[3])
        can_data.append("".join(req[6:6+8]))

    trimmed_can_ids = []
    for s in can_ids:
        if s[0] == "0":
            for i in range(len(s)):
                if s[i] != "0":
                    trimmed_can_ids.append(s[i:])
                    break
        else:
            trimmed_can_ids.append(s)

    with codecs.open("testing_module/can_data_collection_and_parsing/parsed_can_data.csv", "w", "UTF8") as outputFile:
        header = ["Name", "Value"]
        writer = csv.writer(outputFile)
        writer.writerow(header)

        for i in range(len(trimmed_can_ids)):
            response = stark_parser_function(trimmed_can_ids[i],can_data[i])
            for key in response.keys():
                writer.writerow([key,response[key]])
