'''
Created on Mar 28, 2019
first stable version April 17 2019

@author: miki
'''

##SYSTEM
import os
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
##import xlsxwriter
import sys
import pandas as pd

#import PySimpleGUI as sg

##SPECIFIC
# from mincalclib import mineral_constants, dataset, conversion, plotdata
##from mincalclib.conversion import exportAX

##from mincalclib.mainMenu import Example
#import matplotlib
import matplotlib.pyplot as plt
#from matplotlib import interactive
#import seaborn as sns

plt.style.use('seaborn-whitegrid')

import pyRoseDiagram as rose

'''
https://pypi.org/project/PySimpleGUI/
https://pysimplegui.readthedocs.io/tutorial/
https://opensource.com/article/18/8/pysimplegui
'''


class pyStereoRoseGUI:
    version = '0.0'

    def __init__(self):
        self.version


def main():
    if len(sys.argv) >= 2:
        inputfile = sys.argv[1]
        # print('file exists')
        print()
        # batch_calc_from_file(inputfile)
        exit(0)  # Successful exit
    #    quit()
    else:
        # startingpoint = 'blah'
        print('start GUI')

    print("\n")
    print(os.path.dirname(os.path.realpath(sys.argv[0])))
    filewd = os.path.dirname(os.path.realpath(sys.argv[0]))

    # =======GUI========================================================
    #
    root = Tk()
    root.geometry("370x320+400+30")
    root.title("pyStereoRoseGUI beta - Michele Zucali 2021")
    label_root = Label(root, text="pyStereoRoseGUI \n\n michele.zucali@unimi.it\n\n\n "
                                  "The Vaccine Version - Jan 2021 \n\n\n\n\n\n\n")

    label_root.pack()

    output_terminal = Toplevel(root)
    output_terminal.geometry('600x200+800+30')
    label = Label(output_terminal, text="Output Terminal")
    label.pack()
    # text = Text(output_terminal)
    text = scrolledtext.ScrolledText(output_terminal)
    text.pack()
    text.insert(END, "Ready to RUN\n\n")

    root.filename = ''
    #data = ''

    def UploadAction():
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select mineral oxides input file",
                                                   filetypes=[("TXT files", "*.txt"), ("TAB files", "*.tab"),
                                                              ("CSV files", "*.csv"), ("excel files", "*.xlsx"),
                                                              ("excel files", "*.xls")])
        print('Selected1 root.filename:', root.filename)
        text.insert(END, ('Selected1 root.filename:', root.filename))
        saved = sys.stdout
        fout = open("pyMinCalc.log", 'w')
        sys.stdout = writer(sys.stdout, fout)
        print(root.filename)
        inputfile = root.filename
        print(inputfile)
        text.insert(END, ('\nthis is our input file: ', inputfile))
        global data
        data = pd.read_excel(root.filename, engine='openpyxl')
        text.insert(END, data)
        processedFile = open('pyMinCalc.log', 'r')
        text1 = processedFile.read()
        text.insert(END, "\nfinishing\n")
        text.insert(END, "\ntask completed\n")
        print("finishing")
        print("executed")
        sys.stdout = saved
        fout.close()
        print("\n")

    def doSomethingWithData():
        print("doSomethingWithData")
        print(data)
        rose.test(data)
        return

    def ReadDataHeaders():
        print("niente")
        rose.getHeaders(data)
        return



    ###############BUTTONS
    start_button = Button(root, text="1) Load the File (.xlsx)", command=UploadAction).pack()
    read_button = Button(root, text="2) Read Headers", fg='blue', activebackground='#00ff00',
                         command=ReadDataHeaders).pack()
    plot_button = Button(root, text="2) Plot Data", fg='red', activebackground='#00ff00',
                         command=doSomethingWithData).pack()

    close_button = Button(root, text="Exit", command=root.destroy).pack()







    root.mainloop()

    ##### BACK TO TERMINAL-CONSOLE

    print("system closing")
    sys.exit(0)

    '''
    TO BE implemented:
    1) cation partitioning
    2) AX export and reformat for EXCEL spreadsheets
    3) √ save each mineral
    4) SD
    5) thermobarometry?
    6) √ plot √
    7) √ remove spaces headers if any==> inoutfile.py==> line 90 in def readFILE_E_ESTRAI_DATI_MA_CONTROLLA_MINLABEL_SET_OX(file_Input_XLSX): headers.append(str(s.cell(riga,colo).value).strip())

    '''


class writer:
    def __init__(self, *writers):
        self.writers = writers

    def write(self, text):
        for w in self.writers:
            w.write(text)


# def windowsss():
#     # import PySimpleGUI as sg
#
#     layout = [[sg.Text('Persistent window')],
#               [sg.Input(do_not_clear=True)],
#               [sg.Button('Read'), sg.Exit()]]
#
#     window = sg.Window('Window that stays open', layout)
#
#     while True:
#         event, values = window.Read()
#         if event is None or event == 'Exit':
#             break
#         print(event, values)
#
#     window.Close()


if __name__ == '__main__':
    main()
