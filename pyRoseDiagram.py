# code from http://geologyandpython.com/structural_geology.html
# python3
# MICH£LE ZUCALI OCT 2018 @Houston UH


import os
import sys
import numpy as np
#import mplstereonet
# import matplotlib.pyplot as plt ##versione py2
import matplotlib

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QToolBar, QAction, QStatusBar, QCheckBox, \
    QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt  # py3 anche py2
import pandas as pd
from tkinter import *
import tkinter as ttk
from tkinter import filedialog
from tkinter import scrolledtext
#import mplstereonet as mpl
#from windrose import plot_windrose
#from windrose import WindroseAxes
import matplotlib.cm as cm

def readStrikes(df):
    #global strike
    #global weight
    #strike, weight = getHeaders(df)
    listStrikes = df[strike.get()].tolist()
    print(listStrikes)
    print(len(listStrikes))
    peso = df[weight.get()].tolist()
    print(peso)
    return listStrikes, peso

def makeCalcForRose(strikes, peso):
    ## QUESTO FA IL CALCOLO e prepara two_halves per il PLOT
    bin_edges = np.arange(-5, 366, 10)
    number_of_strikes, bin_edges = np.histogram(strikes, bin_edges)
    number_of_strikes_w, bin_edges = np.histogram(strikes, bin_edges, weights=peso)
    number_of_strikes_wdT, bin_edges = np.histogram(strikes, bin_edges, weights=peso, density=True)

    # number_of_strikes, bin_edges = np.histogram(strikes, bin_edges)
    print("NUM OF STRIKES:\n")
    print(len(number_of_strikes.tolist()))
    print(number_of_strikes.tolist())
    number_of_strikes[0] += number_of_strikes[-1]
    number_of_strikes_w[0] += number_of_strikes_w[-1]
    number_of_strikes_wdT[0] += number_of_strikes_wdT[-1]

    half = np.sum(np.split(number_of_strikes[:-1], 2), 0)
    half_w = np.sum(np.split(number_of_strikes_w[:-1], 2), 0)
    half_wdT = np.sum(np.split(number_of_strikes_wdT[:-1], 2), 0)

    global two_halves_1
    two_halves_1 = np.concatenate([half, half])
    global two_halves_1_w
    two_halves_1_w = np.concatenate([half_w, half_w])
    global two_halves_1_wdT
    two_halves_1_wdT = np.concatenate([half_wdT, half_wdT])
    return two_halves_1,two_halves_1_w,two_halves_1_wdT

def getHeaders(data):
    root = Tk()
    root.title("Set columns for Strike and Weight")

    # Add a grid
    mainframe = Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.pack(pady=100, padx=100)
    # Create a Tkinter variable
    global strike
    strike = StringVar(root)
    global weight
    weight = StringVar(root)
    # Dictionary with options
    choices = data.columns.values.tolist()
    strike.set('?')  # set the default option
    weight.set('?')

    popupMenu = OptionMenu(mainframe, strike, *choices)
    Label(mainframe, text="Strike").grid(row=1, column=1)
    popupMenu.grid(row=2, column=1)
    popupMenu2 = OptionMenu(mainframe, weight, *choices)
    Label(mainframe, text="Weight").grid(row=1, column=2)
    popupMenu2.grid(row=2, column=2)
    # on change dropdown value
    def change_dropdown(*args):
        print(strike.get())
        print(weight.get())
    # # link function to change dropdown
    strike.trace('w',change_dropdown)
    weight.trace('w',change_dropdown)
    closebutton = Button(root, text='QUIT', command=root.destroy)
    closebutton.pack()
    root.mainloop()
    strike=strike.get()
    weight=weight.get()
    return

def plotSingleDataRoseUnW(unW):
    print('plotting')
    print(unW)
    fig = plt.figure(1, figsize=(4, 4))
    ax = fig.add_subplot(1, 1, 1, projection='polar')  # #NON RIESCO A RIDURRE LO SPAZIO
    ax.bar(np.deg2rad(np.arange(0, 360, 10)), unW,
            width=np.deg2rad(10), bottom=0.0, color='red', edgecolor='k', label='unW')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.arange(0, 360, 30), labels=np.arange(0, 360, 30))
    # ax.set_rgrids(np.arange(1, two_halves_1.max() + 1, 2), angle=0, weight= 'black')
    ax.set_title('Rose Diagram', y=1.10, fontsize=15)
    ax.grid(True)
    ax.legend()
    #ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show()
    fig.savefig("UnWeighted.png")
    fig.savefig("UnWeighted.svg", format='svg', dpi=1200)
    return

def plotSingleDataRoseW1(W1):
    fig1 = plt.figure(2, figsize=(4, 4))
    ax1 = fig1.add_subplot(1, 1, 1, projection='polar')  # #NON RIESCO A RIDURRE LO SPAZIO
    ax1.bar(np.deg2rad(np.arange(0, 360, 10)), W1,
            width=np.deg2rad(10), bottom=0.0, color='blue', edgecolor='k', label='W1')
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    ax1.set_thetagrids(np.arange(0, 360, 30), labels=np.arange(0, 360, 30))
    # ax.set_rgrids(np.arange(1, two_halves_1.max() + 1, 2), angle=0, weight= 'black')
    ax1.set_title('Rose Diagram', y=1.10, fontsize=15)
    ax1.grid(True)
    ax1.legend()
    #ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    plt.show()
    fig1.savefig("weighted1.png")
    fig1.savefig("weighted1.svg", format'svg', dpi=1200)
    return

def plotSingleDataRoseW2(W2):
    fig2 = plt.figure(3, figsize=(4, 4))
    ax2 = fig2.add_subplot(1, 1, 1, projection='polar')  # #NON RIESCO A RIDURRE LO SPAZIO
    ax2.bar(np.deg2rad(np.arange(0, 360, 10)), W2,
            width=np.deg2rad(10), bottom=0.0, color='green', edgecolor='k', label='W2')
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    ax2.set_thetagrids(np.arange(0, 360, 30), labels=np.arange(0, 360, 30))
    ax2.set_title('Rose Diagram', y=1.10, fontsize=15)
    ax2.grid(True)
    ax2.legend()
    #ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    plt.show()
    fig2.savefig("weighted2.png")
    fig2.savefig("weighted2.svg",format='svg', dpi=1200)
    return


def test(df):
    print("alura?")
    strikes, peso = readStrikes(df)
    UnW,W1,W2=makeCalcForRose(strikes,peso)
    plotSingleDataRoseUnW(UnW)
    plotSingleDataRoseW1(W1)
    plotSingleDataRoseW2(W2)
 #   plotWindRose(strikes, peso)
    #sys.exit()

def setHeaders(s,w):
    print(s,w)

def mpltest():
    return
