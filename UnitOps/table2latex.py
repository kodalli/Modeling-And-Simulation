# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:29:18 2019

@author: Ryan Arnold
edited by Surya T. Kodali 2/1/20
"""

"""
HOW TO USE:
    keep this .py file in a working directory with 2 text files:
        -input_latex_table.txt
        -output_latex_table.txt
    -in the function arguement, change the number of columns to the proper number
    -change dblLine to false if you do not want double underlines in the table header
    -make sure .txt files are in the same directory as the python program
    - copy and paste data copied from a spreadsheet to input_latex_table.txt
    - output is stored in output_latex_table.txt in the same directory,
    the text file contains a properly formatted table
    -if using double line, include usepackage{hhline}
"""


def table2Latex(fileName='input_latex_table.txt', fileOut='output_latex_table.txt', dblLine=False):
    newLines = []
    fline = open(fileName, 'r').readline()
    numCols = len(fline.split('\t'))

    file = open(fileName, 'r')
    firstLine = False

    for line in file:
        if line == fline:
            firstLine = True
        else:
            firstLine = False

        if "&" in str(line):
            line = str(line).replace("&", "\\&")

        newLine = str(line).replace("	", "&")
        newLine = newLine.strip()

        if firstLine and dblLine:

            dblUnderline = ""
            for _ in range(numCols):
                dblUnderline = dblUnderline + '|='
            dblUnderline = dblUnderline + '|'

            newLine = newLine + '\\\\ \\hhline{' + dblUnderline + '}'
            firstLine = False

        else:
            newLine = newLine + ' \\\\ \\hline'

        if len(line) == 1:
            break
        newLines.append(newLine)

    file.close()

    newFile = open(fileOut, "w")

    newFile.write('\\begin{table}[htbp]\n')
    newFile.write('\\centering\n')
    newFile.write('\\caption{insert caption here}\n')
    newFile.write('\\label{insert label here}\n')

    colProp = ""
    for _ in range(numCols):
        colProp = colProp + '|c'
    colProp = colProp + '|'

    newFile.write('\\begin{tabular}'+'{' + colProp + '}\n')

    newFile.write('\\hline\n')

    for lineItem in newLines:
        newFile.write(lineItem)
        newFile.write('\n')

    newFile.write('\\end{tabular}\n')
    newFile.write('\\end{table}\n')

    newFile.close()


if __name__ == '__main__':
    table2Latex(fileName=r'input_latex_table.txt',
                fileOut=r'output_latex_table.txt')
