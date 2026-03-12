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
from tkinter import Tk, filedialog


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


# Fenêtre de sélection du fichier image
root = Tk()
root.withdraw()
root.attributes("-topmost", True)

image_file = filedialog.askopenfilename(
    title="Sélectionner une image",
    filetypes=[
        ("Images", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
        ("Tous les fichiers", "*.*")
    ]
)

root.destroy()

if not image_file:
    print("Aucune image sélectionnée. Fin du programme.")
    raise SystemExit

# Chemin de l'image sélectionnée
image_path = Path(image_file)

# Fichier de sortie : même nom, même dossier, extension .txt
output_path = image_path.with_suffix(".txt")

# Vider le fichier au démarrage
output_path.write_text("", encoding="utf-8")

fig, ax = subplots()
p = io.imread(str(image_path))
ax.imshow(p)

cursor = Cursor(ax, p.shape, str(output_path))
connect('button_press_event', cursor.mouseclick)

show()