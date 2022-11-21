# Dokumentation: https://docs.python.org/3/library/tk.html
# weiterhin genutzte Dokumentation: https://www.educba.com/python-tkinter/
# Import der benötigten Libraries

import tkinter as tki
from PIL import ImageTk, Image
from tkinter import messagebox
import numpy as np
import matplotlib

"""
Part 3 - Implementierung der Button - Funktionen
"""

# Generiert ein Pop-Up Window mit Kontrollfrage (1 = Ja, 0 = Nein), in Anlehnung an https://youtu.be/YXPyB4XeYLA?t=9133
# showerror ggf. für Fehlerhandling

# 3.1 Funktion für den Klick auf "Los". Erst werden Validierungen der Felder durchlaufen, danach Übergang in 3.1

def los_button():
    # prüfen, dass radius und kraftstoff gewählt sind
    # prüfen, dass adresse eine PLZ oder Ort + Straße ist
    #AdressLabel = tki.Label(root, text=adresse.get())  # ruft den gespeicherten Input auf
    popup()

# 3.2 Funktion für die Kontrollfrage und Einstieg in die Output - Funktionen

def popup():
    response = tki.messagebox.askyesno("Bitte bestätigen", "Sind Sie mit der Auswahl einverstanden?")
    tki.Label(root, text=response)
    if response == 1:
        pass
        # if cvs is checked -> weiter in cvs Funktion
            # cvs_export()
        # if pdf is checked -> weiter in pdf Funktion
            # pdf_export()
        # if streetmap is checked:
            # map_export()
    else:
        response = tki.messagebox.showerror("Anfrage gestoppt", "Die Anfrage wurde abgebrochen. Bitte Daten prüfen")
        tki.Label(root, text=response)

def ausgabeformat_button():
    pass

# 3.3 Funktion löscht die PLZ - Eingabemaske bei Klick in das Feld Adresse (überschreibt den Default Text)
# übernommen von https://www.tutorialspoint.com/how-to-clear-text-widget-content-while-clicking-on-the-entry-widget-itself-in-tkinter

def click(event):  # es muss ein parameter in die Funktion übergeben werden
    adresse.configure()
    adresse.delete(0, tki.END)
    adresse.unbind('<Button-1>', clicked)

# 3.4 Funktion für die Generierung der Streetmap in einem zweiten Fenster

def map_export():
    newframe = tki.Toplevel()
    newframe.title('Google Streetview')
    root.iconbitmap('./icon/gasstation_4334.ico')

# 3.4 Funktion für die Generierung der Streetmap in einem zweiten Fenster

def cvs_export():
    newframe = tki.Toplevel()
    newframe.title('Google Streetview')
    root.iconbitmap('./icon/gasstation_4334.ico')

# 3.4 Funktion für die Generierung der Streetmap in einem zweiten Fenster

def pdf_export():
    newframe = tki.Toplevel()
    newframe.title('Google Streetview')
    root.iconbitmap('./icon/gasstation_4334.ico')

"""
Part 1 - Erstellen des GUI und der benötigten Buttons / Tabs (Frank Kovmir)
Das Erstellen dieser Objekte mit Tkinter ist ein zweistufiger Prozess - erst wird das "Widget" definiert
(alles in Tkinter ist ein Widget) und dann in das Fenster (d.h. in den root) geplottet.
"""

# 1.1 Initiieren der Standardbefehle

root = tki.Tk()  # erstellt das Root-Fenster für alle weiteren Widgets (d.h. Buttons etc)
root.title("PKI - Benzinpreisapp")  # bennent das Fenster
root.geometry("550x600")  # setzt die Maße, Breite x Höhe
root.iconbitmap('./icon/gasstation_4334.ico')  # Iconanpassung

# Einfügen eines Hintergrundbildes
bg = ImageTk.PhotoImage(Image.open("./icon/bg.jpg"))
canvas = tki.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

# 1.2 Kreieren von Buttons

# Kraftstoff - muss singlechoice dropdown sein, Vorbefüllung auf SuperE10
kraftstoff = tki.Button(root, text="Kraftstoff", padx=30)

# Radius - muss singlechoice dropdown sein, Vorbefüllung auf 5km
radius = tki.Button(root, text="Radius", padx=30)

# PLZ/Ort - muss text-input Feld sein

adresse = tki.Entry(root, width=25, borderwidth=3)
adresse.insert(0, "Hier bitte die PLZ eingeben")
adresse.get()  # speichert den Input
clicked = adresse.bind('<Button-1>', click)

# Ausgabeformat - muss singlechoice - klick ('radiobutton') sein (Wahl: CVS / PDF / Streetmap)
canvas.create_text(110, 145, text="Ausgabeformat wählen", fill="white", font=('Helvetica 13 bold'))

r = tki.IntVar()  # die Variable wird als ein Integer definiert, um später in einer Funktion mit
# Zahlen arbeiten zu können. Alternativ wäre z.B. auch StrVar() möglich, wenn der value "1" gewählt wird
r.get()

output_cvs = tki.Radiobutton(root, text="CVS", variable=r, value=1)  # Tkinter nutzt eine eigene Syntax für Variablen
output_pdf = tki.Radiobutton(root, text="PDF", variable=r, value=2)
output_map = tki.Radiobutton(root, text="Streetmap", variable=r, value=3)

# Start und Ende - muss normaler Button sein
los = tki.Button(root, text="Los", padx=60, pady=60,
                 command=los_button)  # Achtung, Funktion fehlt noch
ende = tki.Button(root, text='Beenden', padx=60, pady=60, command=root.quit)


# 1.3 Plotten der Buttons in das root GUI - Fenster

adresse.place(x=20, y=20)
radius.place(x=400, y=20)
kraftstoff.place(x=230, y=20)
output_cvs.place(x=20, y=190)
output_pdf.place(x=20, y=240)
output_map.place(x=20, y=290)
los.place(x=380, y=430)
ende.place(x=20, y=430)
root.mainloop()  # führt eine Endlosschleife durch (startet das sichtbare GUI-Fenster)
