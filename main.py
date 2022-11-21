# Dokumentation: https://docs.python.org/3/library/tk.html
# weiterhin genutzte Dokumentation: https://www.educba.com/python-tkinter/
# https://www.python-kurs.eu/tkinter_canvas.php für grafische Elemente
# Pygame Dokumentation für Sounds: https://www.pygame.org/docs/ref/mixer.html
# Import der benötigten Libraries

import tkinter as tki
from PIL import ImageTk, Image
from tkinter import messagebox
import numpy as np
import matplotlib
import pygame
import time  # ggf. notwendig für api unterbrechung bei spam

"""
Part 3 - Implementierung der Button - Funktionen
"""


# Generiert ein Pop-Up Window mit Kontrollfrage (1 = Ja, 0 = Nein), in Anlehnung an https://youtu.be/YXPyB4XeYLA?t=9133
# showerror ggf. für Fehlerhandling

# 3.1 Funktion für den Klick auf "Los". Erst werden Validierungen der Felder durchlaufen, danach Übergang in 3.1

def los_button():
    # prüfen, dass radius und kraftstoff gewählt sind
    # prüfen, dass adresse eine PLZ oder Ort + Straße ist
    # AdressLabel = tki.Label(root, text=adresse.get())  # ruft den gespeicherten Input auf
    popup()


def ende_button():
    end_sound = pygame.mixer.Sound(".\sounds\Shutdown.mp3")
    end_sound.play()
    response = tki.messagebox.showinfo("Goodbye", "Auf Wiedersehen!")
    tki.Label(root, text=response)
    root.quit()


# 3.2 Funktion für die Kontrollfrage und Einstieg in die Output - Funktionen

def popup():
    popup_sound = pygame.mixer.Sound(".\sounds\Control.mp3")
    popup_sound.play()
    response = tki.messagebox.askyesno("Bitte bestätigen", "Sind Sie mit der Auswahl einverstanden?")
    tki.Label(root, text=response)
    if response == 1:
        if radio_var.get() == 1:
            cvs_export()
        if radio_var.get() == 2:
            pdf_export()
        if radio_var.get() == 3:
            map_export()
    else:
        error_sound = pygame.mixer.Sound(".\sounds\Windows.mp3")
        error_sound.play()
        response = tki.messagebox.showerror("Anfrage gestoppt", "Die Anfrage wurde abgebrochen. Bitte Daten prüfen")
        tki.Label(root, text=response)


# 3.3 Funktion löscht die PLZ - Eingabemaske bei Klick in das Feld Adresse (überschreibt den Default Text) übernommen
# von https://www.tutorialspoint.com/how-to-clear-text-widget-content-while-clicking-on-the-entry-widget-itself-in
# -tkinter

def click(event):  # es muss ein parameter in die Funktion übergeben werden
    adresse.configure()
    adresse.delete(0, tki.END)
    adresse.unbind('<Button-1>', clicked)


# 3.4 Funktion für die Generierung der Streetmap in einem zweiten Fenster

def map_export():
    # ggf. sind global variablen notwendig
    newframe = tki.Toplevel()
    newframe.title('Google Streetview')
    root.iconbitmap('./icon/gasstation_4334.ico')


# 3.5 Funktion für die Generierung des cvs Exports falls gewählt

def cvs_export():
    pass


# 3.6 Funktion für die Generierung des pdf Exports falls gewählt

def pdf_export():
    pass


# 3.7 Funktion um nur aktive Tankstellen anzuzeigen. Soll je nach Checkbox Status ein True (checked)
# oder ein False returnen. Wird über die export Funktionen geprüft (if aktiv_checkbox() and aktiv_checkbox() == ..)

def aktiv_checkbox():
    if check_var.get() == 1:
        return True
    else:
        return False


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

# Hintergrundmusik

pygame.mixer.init()  # initialisiert Sounds
pygame.mixer.music.load(r".\sounds\background.mp3")
pygame.mixer.music.set_volume(0.0079)
pygame.mixer.music.play(loops=-1)  # unendlicher loop für die Hintergrundmusik

# Einfügen eines Hintergrundbildes
# Canvas sind grafische html-basierte Elemente
bg = ImageTk.PhotoImage(Image.open("./icon/bg.jpg"))
canvas = tki.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

# 1.2 Kreieren von Buttons

# Kraftstoff - muss singlechoice Dropdown sein

kraftstoff_liste = [

    "Diesel",
    "Super",
    "Super E10"
]

ks = tki.StringVar()
ks.set("Kraftstoff wählen")
kraftstoff = tki.OptionMenu(root, ks, *kraftstoff_liste)
ks.get()

# Radius - muss singlechoice Dropdown sein

radius_liste = [

    "1 km",
    "2 km",
    "5 km",
    "10 km",
    "25 km",
]

r = tki.StringVar()
r.set("Radius wählen")
radius = tki.OptionMenu(root, r, *radius_liste)
r.get()

# PLZ/Ort - muss text-input Feld sein

adresse = tki.Entry(root, width=25, borderwidth=3)
adresse.insert(0, "Hier bitte die PLZ eingeben")
adresse.get()  # speichert den Input
clicked = adresse.bind('<Button-1>', click)

# Ausgabeformat - muss singlechoice - klick ('radiobutton') sein (Wahl: CVS / PDF / Streetmap)
canvas.create_text(110, 145, text="Ausgabeformat wählen", fill="white", font='Helvetica 13 bold')

radio_var = tki.IntVar()  # die Variable wird als ein Integer definiert, um später in einer Funktion mit
# Zahlen arbeiten zu können. Alternativ wäre z.B. auch StrVar() möglich, wenn der value "1" gewählt wird

output_cvs = tki.Radiobutton(root, text="CVS", variable=radio_var,
                             value=1)  # Tkinter nutzt eine eigene Syntax für Variablen
output_pdf = tki.Radiobutton(root, text="PDF", variable=radio_var, value=2)
output_map = tki.Radiobutton(root, text="Streetmap", variable=radio_var, value=3)
radio_var.get()

# Start und Ende - muss normaler Button sein
los = tki.Button(root, text="Los", padx=60, pady=60,\
                 command=los_button)  # Achtung, Funktion fehlt noch
ende = tki.Button(root, text='Beenden', padx=60, pady=60, command=ende_button)

# nur offene Tankstellen anzeigen - Checkbox Button
check_var = tki.IntVar()
aktiv = tki.Checkbutton(root, width=20, text="nur geöffnete Tankstellen", variable=check_var,\
                        command=aktiv_checkbox)
check_var.get()

# 1.3 Plotten der Buttons in das root GUI - Fenster

adresse.place(x=20, y=20)
radius.place(x=400, y=20)
kraftstoff.place(x=230, y=20)
output_cvs.place(x=20, y=190)
output_pdf.place(x=20, y=240)
output_map.place(x=20, y=290)
los.place(x=380, y=430)
ende.place(x=20, y=430)
aktiv.place(x=20, y=80)

root.mainloop()  # führt eine Endlosschleife durch (startet das sichtbare GUI-Fenster)
