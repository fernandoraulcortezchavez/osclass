##########################################################
##CENTRO DE ENSEÑANZA TÉCNICA Y SUPERIOR            ######
##Ingeniería en Cibernética Electrónica             ######
##Fernando Raúl Cortez Chávez                       ######
##06/12/17                                          ######
##Diseño de algoritmos                              ######
###### Ordenador de csv                          #########

import csv

FILE_NAME = "Crimes_-_2001_to_present.csv"
OUT_FILE_NAME = "Sorted_"

def main():
    # Read crime entries file, split them by chunks of 1 million lines and sort each file
    chunk_names = splitIntoSortedFiles()

    # Merge sort the chunk files
    mergeListFiles(chunk_names)
    
                
def splitIntoSortedFiles():
    with open(FILE_NAME, 'r', newline='\n') as f:
        reader = csv.reader(f)

        # Counter of the current sorted chunk file
        fileNumber = 0

        # List that holds the lines of the current slice of the original csv file
        data = []

        # List that will hold the correct index of the elements in data sorted in incremental order according to its 10-th cell/value
        indexList = []

        # Current index of the current slice of the csv file
        index = 0

        # List that will hold the names of the sorted output file chunks
        chunk_names = []

        # Iterate over all the lines in the csv file
        for i, line in enumerate(reader):
            # Remove header
            if i == 0:
                continue
            
            indexList.append((int(line[10]), index))
            index += 1
            data.append(line)
            
            # If already reached 999999 lines, sort them and write a new file
            if i % 100000 == 99999:
                
                # Get the indexes from radix sort
                correctIndexes = radixSort(indexList)

                # Create a new name for the current chunk to be written and add its name to the chunk_names list
                outfile_name = OUT_FILE_NAME + str(fileNumber) + ".csv"
                chunk_names.append(outfile_name)

                # Initialize a new sorted chunk file and its csv writer
                out = open(outfile_name, 'w', newline = "")
                writer = csv.writer(out)

                # Write the i-th correct line of data
                for i in range(len(correctIndexes)):
                    writer.writerow(data[correctIndexes[i]])
                out.close()

                # Update auxiliary variables
                data = []
                indexList = []
                fileNumber += 1
                index = 0
                
                
        # Get the indexes from radix sort from the lines of the last chunk
        correctIndexes = radixSort(indexList)

        # Create a new name for the last chunk to be written and add its name to the chunk_names list
        outfile_name = OUT_FILE_NAME + str(fileNumber) + ".csv"
        chunk_names.append(outfile_name)
        
        # Initialize a new sorted chunk file and its csv writer
        out = open(OUT_FILE_NAME + str(fileNumber) + ".csv", 'w')
        writer = csv.writer(out)

        # Write the i-th correct line of data
        for i in range(len(correctIndexes)):
            writer.writerow(data[correctIndexes[i]])
        out.close()

        return chunk_names

def mergeTwoFiles(file1, file2, out_name):
    """Function that takes in two file name strings and and output file name string, and combines the two input files in increasing
       order according to its 10-th cell"""
    with open(file1, 'r') as first_file:
        with open(file2, 'r') as second_file:
            with open(out_name, 'w', newline = '') as output_file:
                reader1, reader2 = csv.reader(first_file), csv.reader(second_file)
                writer = csv.writer(output_file)

                current_line1 = next(reader1)
                current_line2 = next(reader2)

                # Mege the files as in Merge Sort: Compare the current lower lines of each file and the lowest is written first
                # then another line from the chosen file is retrieven. The process continues until one file runs out of lines
                while current_line1 != None and current_line2 != None:
                    # Check that the obtained line is not an empty line or other irregular row
                    if len(current_line1) < 11: 
                        try:
                            current_line1 = next(reader1)
                        except StopIteration:
                            current_line1 = None
                        continue
                            
                    if len(current_line2) < 11:
                        try:
                            current_line2 = next(reader2)
                        except StopIteration:
                            current_line2 = None
                        continue
                            
                    if int(current_line1[10]) > int(current_line2[10]):
                        writer.writerow(current_line2)
                        # Get the next line of the other file
                        try:
                            current_line2 = next(reader2)
                        except StopIteration:
                            current_line2 = None
                    else:
                        writer.writerow(current_line1)
                        # Get the next line of the other file
                        try:
                            current_line1 = next(reader1)
                        except StopIteration:
                            current_line1 = None

                # One of the readers ran out of lines, so write the remaining lines of the other reader as they are
                if current_line1 == None:
                    for remaining_line in reader2:
                        writer.writerow(remaining_line)
                if current_line2 == None:
                    for remaining_line in reader2:
                        writer.writerow(remaining_line)
                
def mergeListFiles(filename_list, output_file_number = 0):
    if len(filename_list) == 1:
        return filename_list[0]

    # Split the filename_list into two halves
    number_of_files = len(filename_list)
    first_halve = filename_list[0 : number_of_files//2]
    second_halve = filename_list[number_of_files//2 : ]

    # Merge the files in each halve of the original list
    first_merge_name = mergeListFiles(first_halve, output_file_number * 2 + 1)
    second_merge_name = mergeListFiles(second_halve, output_file_number * 2 + 2)

    # Merge the two merged halves
    output_file_name = "Merge_" + str(output_file_number) + ".csv"
    mergeTwoFiles(first_merge_name, second_merge_name, output_file_name)
    return output_file_name

    

def __countRadix(numberTupleList, position):
    count = []

    # Initialize a list that will count each number's frequency
    for i in range(9 + 1):
        count.append([])

    # Obtain length of the list
    length = len(numberTupleList)

    # Increment by 1 the frequency of the current item
    for i in range(length):
        currentNumber = numberTupleList[i][0]
        digit = getDigit(currentNumber, position)
        count[digit].insert(0, numberTupleList[i])
        #count[digit].insert(0, numberTupleList[i][1])

    # Sort the list
    currentIndex = 0
    newTupleList = []
    for i in range(9 + 1):
        while len(count[i]) > 0:
            #incorrectIndex = count[i].pop(len(count[i]) - 1)
            tup = count[i].pop(len(count[i]) - 1)
            newTupleList.append(tup)
            #swapTwoListElements(incorrectIndex, currentIndex, numberTupleList)
            currentIndex += 1

        if currentIndex == length:
            break

    return newTupleList

def getDigit(integer, positionRigthToLeft):
    return (integer // (10 ** positionRigthToLeft)) % 10

def radixSort(numbersTupleList, maxDigits = 5):
    for i in range(maxDigits):
        numbersTupleList = __countRadix(numbersTupleList, i)
        
    correctIndexes = []
    for num, index in numbersTupleList:
        correctIndexes.append(index)

    return correctIndexes

if __name__ == "__main__":
    main()
