# Dokumentation: https://docs.python.org/3/library/tk.html
# weiterhin genutzte Dokumentation: https://www.educba.com/python-tkinter/
# Import der benötigten Libraries

import tkinter as tki
from tkinter import ttk
from tkinter.messagebox import showinfo
import numpy
import matplotlib

"""
Part 1 - Erstellen des GUI und der benötigten Buttons / Tabs (Frank Kovmir)
Das Erstellen dieser Objekte mit Tkinter ist ein zweistufiger Prozess - erst wird das "Widget" definiert
(alles in Tkinter ist ein Widget) und dann in das Fenster (d.h. in den root) geplottet.
"""

class App(tki.Tk): # Vererbung der Tkinter Tk Klasse
  def __init__(self):
    super().__init__() # import der geerbten init Funktion

    # Anpassen geerbter Parameter
    self.title("PKI - Benzinpreisapp") # benennt das Fenster
    self.geometry('500x800') # Auflösung des Fensters

    # Kreieren von Labels
    #self.label = ttk.Label(self, text='Hello, Tkinter!')
    #self.label.pack()

    # Kreieren von Buttons
    self.Kraftstoff = ttk.Button(self, text='Click Me')
    self.Kraftstoff['command'] = self.button_clicked

    # Plotten der Buttons
    self.Kraftstoff.pack()

  # Funktionen der Buttons

  def button_clicked(self):
    showinfo(title='Information', message='Hello, Tkinter!')

# Einstiegsfunktion, mainloop
if __name__ == "__main__":
  root = App() #erstellt das Root-Fenster für alle weiteren Widgets (d.h. Buttons etc)
  root.mainloop()