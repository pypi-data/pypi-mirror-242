import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def qhtm():
    """
    Output: quos.html webpage with a list of various gates
    """
    import webbrowser
    try:
        webbrowser.open((__file__).replace('__init__.py','') + "quos.html")
    except:
        webbrowser.open("quos.html")

def qxls():
    """
    Output: quos.xlsm Excel file with a macro to create a plot of specified gates
    """
    from pathlib import Path
    import shutil
    try:
        zdst = str(os.path.join(Path.home(), "Downloads"))
    except:
        zdst = str(Path.home() / "Downloads")    
    try:
        shutil.copy((__file__).replace('__init__.py','') + "quos.xlsm", zdst + "/quos.xlsm")         
    except:
        shutil.copy("quos.xlsm",  zdst + "/quos.xlsm")

def qstr(xlsm='quos.xlsm', wsht='Gates'):
    """
    Output: String of sgqt strings concatenated by pipe ('|')
    xlsm  : Excel file with a specification of gates
    """
    import pandas as pd
    xdf = pd.read_excel(xlsm, sheet_name=wsht, header=None)
    txt = ""
    for col in range(0, xdf.shape[1]):
        for row in range(0, xdf.shape[0]):
            cel = str(xdf.iloc[row, col])
            if (cel.lower() != "nan"):
                txt = txt + cel + "," + str(row+1) + "," + str(col+1) + "|"
    if txt=="":
        txt = '1,3,0|Q 30 15,5,0|H a,1,1|Y,1,2|Z,2,2|X,3,2|Y,4,2|Z,5,2|X,6,2|S,2,3|T,4,3|V,6,3|'
        txt = txt + 'Rx 30,1,4|Ry 15,2,4|Rz 15,3,4|Rz 30,4,4|Ry 15,5,4|Rx 15,6,4|Ph 15,2,5|'
        txt = txt + 'Pp 30,4,5|O a,1,6|Cd,1,7,Ph 15,2,7|K,3,7|U 30 30 15,4,7|U 15 15 30,6,7|'
        txt = txt + 'C,1,8,X,2,9|Sw,4,8,Sw,6,8|iSw,3,9,iSw,4,9|M a,1,10|'
    print(txt)
    return txt

def qplt(ssgqt):
    """
    Output: Matplotlib plot
    ssgqt : String of sgqt strings concatenated by pipe ('|')
    sgqt  : String of g q t strings concatenated by comma
    g     : String of item-name and applicable arguments strings concatenated by space
    q     : a (for all) or Positive integer denoting qudit sequence number
    t     : Positive integer denoting opertation time sequence number
    """
    asgqt = ssgqt.split('|')
    qmx, tmx = 0, 0
    for sgqt in asgqt:
        agqt = sgqt.split(",")
        q, t = agqt[1], int(agqt[2])
        if not (q=="a"):
            if (int(q) > qmx): qmx = int(q)
        if (t > tmx): tmx = t
        if len(agqt) > 3:
            q, t = agqt[4], int(agqt[5])
            if not (q=="a"):
                if (int(q) > qmx): qmx = int(q)
            if (t > tmx): tmx = t
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.set_xlim(0, tmx+1)
    ax.set_ylim(-qmx-1, 0)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    try:
        idir = (__file__).replace('__init__.py','') + 'icons/'
    except:
        idir = 'icons/'
    for q in range(1, qmx+1):
        ax.axhline(-q, color='red', lw=1)
        ax.add_artist(AnnotationBbox(
            OffsetImage(imread(idir +'0.jpg')),
            (0, -q), frameon=False))
    for sgqt in asgqt:
        agqt = sgqt.split(",")
        g, q, t = agqt[0].split(" ")[0], agqt[1], int(agqt[2])
        if q=="a":
            r = range(1,qmx+1)
        else:
            r = [int(q)]
        if (t==0) and ((g=="1") or (g=="Q")):
            for p in r:
                ax.add_artist(AnnotationBbox(
                    OffsetImage(imread(idir + g +'.jpg')),
                    (0, -p), frameon=False))
        if (t>0) and (g in ['0','1','Q','I','H','X','Y','Z','S','T','V','Rx','Ry','Rz','Ph','Pp','U','C','Cd','Sw','iSw','M','O','K']):
            for p in r:
                ax.add_artist(AnnotationBbox(
                    OffsetImage(imread(idir + g + '.jpg')),
                    (t, -p), frameon=False))
                if len(agqt) > 3:
                    g1, q1, t1 = agqt[3].split(" ")[0], agqt[4], int(agqt[5])
                    if q1=="a":
                        r1 = range(1,qmx)
                    else:
                        r1 = [int(q1)]
                    for p1 in r1:
                        ax.add_artist(AnnotationBbox(
                            OffsetImage(imread(idir + g1 + '.jpg')),
                            (t1, -p1), frameon=False))
                        plt.plot([t,t1], [-p,-p1], 'b')
    plt.show()

def qsim(ssgqt):
    """
    Output: Matplotlib plot
    ssgqt : String of sgqt strings concatenated by pipe ('|')
    sgqt  : String of g q t strings concatenated by comma
    g     : String of item-name and applicable arguments strings concatenated by space
    q     : Positive integer denoting qudit sequence number
    t     : Positive integer denoting opertation time sequence number
    """
    print(ssgqt)

'''
qsim("This is to test qsim.")
qxls()
qhtm()
txt = '1,3,0|Q 30 15,5,0|H a,1,1|Y,1,2|Z,2,2|X,3,2|Y,4,2|Z,5,2|X,6,2|S,2,3|T,4,3|V,6,3|'
txt = txt + 'Rx 30,1,4|Ry 15,2,4|Rz 15,3,4|Rz 30,4,4|Ry 15,5,4|Rx 15,6,4|Ph 15,2,5|'
txt = txt + 'Pp 30,4,5|O a,1,6|Cd,1,7,Ph 15,2,7|K,3,7|U 30 30 15,4,7|U 15 15 30,6,7|'
txt = txt + 'C,1,8,X,2,9|Sw,4,8,Sw,6,8|iSw,3,9,iSw,4,9|M a,1,10'
qplt(txt)
'''