#!/usr/bin/env python
# -*- noplot -*-

"""
This example shows how to use matplotlib to provide a data cursor.  It
uses matplotlib to draw the cursor and may be a slow since this
requires redrawing the figure with every mouse move.

Faster cursoring is possible using native GUI drawing, as in
wxcursor_demo.py
"""

from __future__ import print_function
from pylab import *
from skimage import io
from pathlib import Path


class Cursor:
    def __init__(self, ax, s, output_file):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # fichier de sortie
        self.f = output_file
        self.count = 1
        self.s = s

    def mouseclick(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        print(x, y)

        with open(self.f, 'a', encoding='utf-8') as h:
            h.write("\t{}\t{}\n".format(x, y))

        self.ax.text(x + 4, y - 4, str(self.count), fontsize=14, color='r')
        self.ax.plot(x, y, '.r')
        self.count += 1
        draw()


# Dossier où se trouve ce script : .../code
script_dir = Path(__file__).resolve().parent

# Racine du projet : un niveau au-dessus de /code
project_root = script_dir.parent

# Dossier contenant l'image et le fichier de sortie
data_dir = project_root / "data" / "dataInput"

# Image à charger
image_path = data_dir / "Portrait.png"

# Fichier de sortie dans le même dossier que l'image
output_path = data_dir / "points.txt"

# Vider le fichier au démarrage
output_path.write_text("", encoding="utf-8")

fig, ax = subplots()
p = io.imread(str(image_path))
ax.imshow(p)

cursor = Cursor(ax, p.shape, str(output_path))
connect('button_press_event', cursor.mouseclick)

show()