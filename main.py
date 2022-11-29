# Dokumentation: https://docs.python.org/3/library/tk.html
# weiterhin genutzte Dokumentation: https://www.educba.com/python-tkinter/
# https://www.python-kurs.eu/tkinter_canvas.php für grafische Elemente
# Pygame Dokumentation für Sounds: https://www.pygame.org/docs/ref/mixer.html

# Import der benötigten Libraries

import tkinter as tki
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import pygame
import time  # ggf. notwendig für api unterbrechung bei spam-requests
import geocoder
import geopy
import pgeocode
import string
import requests
import json



"""
Part 3 - Implementierung der Button - Funktionen (Frank Kovmir)
"""


# 3.1.0 Funktionen für den Haupttab
# 3.1.1 Funktion für den Beenden-Button

def ende_button():
    end_sound = pygame.mixer.Sound(r".\sounds\Shutdown.mp3")
    end_sound.play()
    response = tki.messagebox.showinfo("Goodbye", "Auf Wiedersehen!")
    tki.Label(tab1, text=response)
    root.quit()


# 3.1.2 Funktion für den Klick auf "Los". Erst werden Validierungen der Felder durchlaufen, danach Übergang in 3.2
# tki.messagebox Generiert ein Pop-Up Window (Ausgestaltung je nach Typ, infobox / errorbox / ja oder nein Box)
# In Anlehnung an https://youtu.be/YXPyB4XeYLA?t=9133

def los_button():
    if radio_var and radio_var.get() == 0:
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte ein Ausgabeformat angeben!")
    if ks and ks.get() == 'Kraftstoff wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte einen Kraftstoff angeben!")
    if r and r.get() == 'Radius wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte einen Radius angeben!")
    if adresse and adresse.get():  # Validierung der Adressdaten (PLZ)
        # im Api Aufruf muss die PLZ in lat / lng als float übergeben werden, siehe tankerkönig-api doc.
        # Ohne Verbindung zur Google API kann nominatim genutzt werden, die Funktion nimmt aber nur eine PLZ entgegen.
        # Daher erfolgt hier eine rudimentäre Validierung der Adresseingabe

        if len(adresse.get()) == 5 and all(num in string.digits for num in adresse.get()):  # checkt die Länge und ob
            # es sich um einen Zahlenstring handelt (string.digits = 0123456789)
            # Code von https://www.reddit.com/r/learnpython/comments/ljqyqr
            # /best_way_to_get_latitude_and_longitude_data_from/
            nomi = pgeocode.Nominatim('de')
            query = nomi.query_postal_code(adresse.get())
            data = {
                "lat": query["latitude"],
                "lon": query["longitude"]
            }

            if not any(np.isnan(val) for val in data.values()):  # extra Sicherheitsabfrage um die Übergabe eines NaN
                # Numpy Frames dicts und damit einen fehlerhaften Api Aufruf zu vermeiden
                return popup(data)  # Aufruf der nächsten Funktion und Übergabe der Koordinaten aus data als Parameter

            else:
                error_sound()
                tki.messagebox.showerror("Falscher Input", f"Die eingegebene Adresse '{adresse.get()}' ist keine "
                                                           f"Postleitzahl in Deutschland")
        else:
            error_sound()
            tki.messagebox.showerror("Falscher Input", f"Die eingegebene Adresse '{adresse.get()}' ist keine "
                                                       f"Postleitzahl")
    else:
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte eine Postleitzahl angeben!")


# 3.1.3 Funktion für die Kontrollfrage

def popup(data):
    info_sound()
    response = tki.messagebox.askyesno("Bitte bestätigen", "Sind Sie mit der Auswahl einverstanden?")
    tki.Label(tab1, text=response)
    print(data)
    print(data['lat'])  # Testaufruf um Übergabe der PLZ zu testen
    print(data['lon'])
    if response == 1:
        api_check(data)
    else:
        error_sound()
        response = tki.messagebox.showerror("Anfrage gestoppt", "Die Anfrage wurde abgebrochen. Bitte Daten prüfen")
        tki.Label(tab1, text=response)

# 3.1.4 Funktion für den Einstieg in die Generierungsfunktionen, baut API Verbindung auf

def api_check(data):

    """
    Part 2 - Aufruf der API
    """

    # https://creativecommons.tankerkoenig.de/
    # Dein API-Key ist c7f5f8e5-e352-81d0-7d49-996d13f53d26

    key = "c7f5f8e5-e352-81d0-7d49-996d13f53d26"
    # Code für radius von https://stackoverflow.com/questions/1450897/remove-characters-except-digits-from-string
    # -using-python. Es wandelt den Radius-Input (zB 5km) in ein Float Objekt für den Api Aufruf um, siehe Doku
    radius = float(''.join(filter(str.isdigit, r.get())))
    #print(radius)
    kraftstoff_dict = {'Diesel': 'diesel', 'Super': 'e5', 'Super E10': 'e10'} # wandelt den Kraftstoff-Input (Diesel)
    # in den vom Api unterstützen String um
    kraftstoff = kraftstoff_dict[ks.get()]
    active_flag = aktiv_checkbox()
    open_list = []
    full_list = []
    #print(kraftstoff)
    try:
        api_request = requests.get(
            f"https://creativecommons.tankerkoenig.de/json/list.php?lat={data['lat']}&lng={data['lon']}&rad={radius}&sort=dist&type={kraftstoff}&apikey={key}")
        api = json.loads(api_request.content)
    except Exception as e:
        api = f"Error..{e}"

    # API Troubleshooting falls ok == False (z.B. wenn Website down, Key tot .. )
    if api and api.get('ok') is False:
        info_sound()
        return tki.messagebox.showinfo("Fehler in der Verbindung", api.get("message"))

    print(api)

    for i in api.get("stations"):
        if active_flag:
            if not i.get("isOpen"):
                continue
            else:
                open_list.append(i)
        else:
            full_list.append(i)

    #print(open_list)
    #print(full_list)

    new_list = []
    if len(open_list) <= 0:
        new_list = full_list
    else:
        new_list = open_list


    # Einstieg in die weiteren Funktionen, hier muss noch dafür gesorgt werden, dass in Abhängigkeit vom active Flag
    # die korrekte Liste in die Funktionen übergeben wird (open, oder full)

    if radio_var.get() == 1:
        cvs_export(new_list)
    if radio_var.get() == 2:
        pdf_export(new_list)
    if radio_var.get() == 3:
        map_export(new_list)


# 3.1.5 Funktion löscht die PLZ - Eingabemaske bei Klick in das Feld 'Adresse' (überschreibt den Default Text)
# übernommen von https://www.tutorialspoint.com/how-to-clear-text-widget-content-while-clicking-on-the-entry-widget
# -itself-in -tkinter

def click(event):  # es muss ein parameter in die Funktion übergeben werden
    adresse.configure()
    adresse.delete(0, tki.END)
    adresse.unbind('<Button-1>', clicked)


# 3.1.6 Funktion für die Generierung der Streetmap in einem zweiten Fenster, falls angeklickt im radio-button

def map_export(new_list):
    # ggf. sind globale variablen notwendig um korrekt in das neue frame transportiert zu werden
    newframe = tki.Toplevel()
    newframe.title('Google Streetview')
    newframe.iconbitmap('./icon/gasstation_4334.ico')


# 3.1.7 Funktion für die Generierung des cvs Exports, falls angeklickt im radio-button

def cvs_export(new_list):
    pass


# 3.1.8 Funktion für die Generierung des pdf Exports, falls angeklickt im radio-button

def pdf_export(new_list):
    pass


# 3.1.9 Funktion, um nur aktive Tankstellen anzuzeigen. Soll je nach Checkbox Status ein True (checked)
# oder ein False returnen. Wird über die export Funktionen geprüft (if aktiv_checkbox() is True ..)

def aktiv_checkbox():
    if check_var.get() == 1:
        return True
    else:
        return False


# 3.1.9 Sound - Funktionen

def info_sound():
    info = pygame.mixer.Sound(r".\sounds\Control.mp3")
    info.play()


def error_sound():
    error = pygame.mixer.Sound(r".\sounds\Windows.mp3")
    error.play()


# 3.2.0 Funktionen für den Prognose und Historie - Tab
# 3.2.1 Funktion für den Los-Button

def los2_button():
    pass


"""
Part 1 - Erstellen des GUI und der benötigten Buttons / Tabs (Frank Kovmir)
Das Erstellen dieser Objekte mit Tkinter ist ein zweistufiger Prozess - erst wird das "Widget" definiert
(alles in Tkinter ist ein Widget) und dann in das Fenster (d.h. in den root) geplottet.
"""

# 1.1 Initiieren der Standardbefehle

root = tki.Tk()  # erstellt das Root-Fenster für alle weiteren Widgets (d.h. Buttons etc)
root.title("PKI - Fuel Guru")  # bennent das Fenster
root.geometry("550x620")  # setzt die Maße, Breite x Höhe
root.iconbitmap('./icon/gasstation_4334.ico')  # Iconanpassung

# Setzen der derzeitigen User-Postleitzahl im Adressfeld(näherungsweise)
# Code von https://stackoverflow.com/questions/24906833/how-to-access-current-location-of-any-user-using-python
# und https://gis.stackexchange.com/questions/352961/convert-lat-lon-to-zip-postal-code-using-python

geocode = geocoder.ip('me')  # holt die Koordinaten
geo_locator = geopy.Nominatim(user_agent='1234')
location = geo_locator.reverse(geocode.latlng)
zipcode = location.raw['address']['postcode']

# Hintergrundmusik

pygame.mixer.init()  # initialisiert Sounds
pygame.mixer.music.load(r".\sounds\background.mp3")
pygame.mixer.music.set_volume(0.0079)
pygame.mixer.music.play(loops=-1)  # unendlicher loop für die Hintergrundmusik

# Setzen von verschiedenen Tabs mithilfe von TTK-Widgets

notebook = ttk.Notebook(root)  # TTK Widget, ist quasi ein Array / eine Sammlung von Widgets
tab1 = tki.Frame(notebook)  # Frame für Tab 1
tab2 = tki.Frame(notebook)  # Frame für Tab 2
notebook.add(tab1, text="Hauptfunktionen")  # Füllt die Tabs in das kreierte Notebook
notebook.add(tab2, text="Historie und Prognosen")
notebook.pack(expand=True, fill="both")

# Einfügen eines Hintergrundbildes
# Canvas sind grafische html-basierte Elemente der TK Klasse

bg = ImageTk.PhotoImage(Image.open("./icon/bg.jpg"))
canvas = tki.Canvas(tab1)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

bg2 = ImageTk.PhotoImage(Image.open("./icon/graph.jpg"))
canvas2 = tki.Canvas(tab2)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, image=bg2, anchor="nw")

# 1.2 Kreieren von Hauptfunktions-Buttons
# 1.2.1 Kraftstoff - muss singlechoice Dropdown sein

kraftstoff_liste = [

    "Diesel",
    "Super",
    "Super E10"
]

ks = tki.StringVar()
ks.set("Kraftstoff wählen")
kraftstoff = tki.OptionMenu(tab1, ks, *kraftstoff_liste)

# 1.2.2 Radius - muss singlechoice Dropdown sein

radius_liste = [

    "1 km",
    "2 km",
    "5 km",
    "10 km",
    "25 km",
]

r = tki.StringVar()
r.set("Radius wählen")
radius = tki.OptionMenu(tab1, r, *radius_liste)

# 1.2.3 PLZ/Ort - muss text-input Feld sein

adresse = tki.Entry(tab1, width=25, borderwidth=3)
adresse.insert(0, zipcode)  # setzt den Default Text (aktuelle PLZ)
adresse.get()  # speichert den Input
clicked = adresse.bind('<Button-1>', click)  # ruft die click Funktion zur Löschung des Default - Textes auf

# 1.2.4 Ausgabeformat - muss singlechoice - klick ('radiobutton') sein (Wahl: CVS / PDF / Streetmap)

canvas.create_text(110, 145, text="Ausgabeformat wählen", fill="white", font='Helvetica 13 bold')

radio_var = tki.IntVar()  # die Variable wird als ein Integer definiert, um später in einer Funktion mit
# Zahlen arbeiten zu können. Alternativ wäre z.B. auch StrVar() möglich, wenn der value "1" gewählt wird

output_cvs = tki.Radiobutton(tab1, text="CVS", variable=radio_var,
                             value=1)  # Tkinter nutzt eine eigene Syntax für Variablen
output_pdf = tki.Radiobutton(tab1, text="PDF", variable=radio_var, value=2)
output_map = tki.Radiobutton(tab1, text="Streetmap", variable=radio_var, value=3)

# 1.2.5 Start und Ende - müssen 'normale' Buttons sein

los = tki.Button(tab1, text="Los", padx=80, pady=60, \
                 command=los_button)
ende = tki.Button(tab1, text='Beenden', padx=60, pady=60, command=ende_button)

# 1.2.6 nur offene Tankstellen anzeigen - Checkbox Button

check_var = tki.IntVar()
aktiv = tki.Checkbutton(tab1, width=20, text="nur geöffnete Tankstellen", variable=check_var, \
                        command=aktiv_checkbox)
check_var.get()

# 1.3 Kreieren von Historie und Prognose-Buttons
# 1.3.1 Start und Ende - müssen 'normale' Buttons sein

los2 = tki.Button(tab2, text="Los", padx=80, pady=60, \
                  command=los2_button)  # Achtung, Funktion fehlt noch
ende2 = tki.Button(tab2, text='Beenden', padx=60, pady=60, command=ende_button)

# 1.3.2 Dropdown für Historie (1 W, 1M, 1J)
#folgt

# 1.3.3 Radiobuttons für Preisprognose (Diesel, Super, Super E10) des nächsten Tages
#folgt

# Outputs für Historie jeweils als Grafik in neuem Fenster
# Outputs für Prognose jeweils als Textfeld Hinweis

# 1.4 Plotten der Hauptfunktions - Buttons in das Tab 1 GUI - Fenster
# Es wurde mit place und manuellen Koordinatenübergabe gearbeitet. Alternativ wäre auch .pack() oder .grid mit row &
# columns für die Platzierung möglich gewesen.

adresse.place(x=20, y=20)
radius.place(x=400, y=20)
kraftstoff.place(x=230, y=20)
output_cvs.place(x=20, y=190)
output_pdf.place(x=20, y=240)
output_map.place(x=20, y=290)
los.place(x=340, y=430)
ende.place(x=20, y=430)
aktiv.place(x=20, y=80)

# 1.5 Plotten der Historie und Prognose - Buttons in das Tab 2 des GUI - Fensters

los2.place(x=340, y=430)
ende2.place(x=20, y=430)

# 1.6 Mainloop

root.mainloop()  # führt eine Endlosschleife durch (startet das sichtbare GUI-Fenster)
