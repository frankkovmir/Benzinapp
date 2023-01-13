# Dokumentation: https://docs.python.org/3/library/tk.html
# weiterhin genutzte Dokumentation: https://www.educba.com/python-tkinter/
# https://www.python-kurs.eu/tkinter_canvas.php für grafische Elemente
# Pygame Dokumentation für Sounds: https://www.pygame.org/docs/ref/mixer.html
# Import der benötigten Libraries

import tkinter as tki
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import pygame
import geocoder
import geopy
import pgeocode
import string
import requests
import json
import tkintermapview
from fpdf import FPDF, XPos, YPos
from datetime import datetime, timedelta
import os
import subprocess
from tkinter.filedialog import askdirectory
import webbrowser
from threading import Thread
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
import time
from Tooltip import CreateToolTip

"""
Part 3 - Implementierung der Button - Funktionen
"""


# 3.1.0 Funktionen für den Haupttab
# 3.1.1 Funktion für den Beenden-Button bzw. das Beenden per Window - Manager

def on_closing():
    """Implementiert die Funktion für das Beenden per Window Manager
    Returns:
        Zerstört den Root
    """

    end_sound()
    if messagebox.askokcancel("Beenden", "Wollen Sie das Programm beenden?"):
        root.destroy()


def ende_button():
    """Implementiert die Funktion für den Beenden-Button
    Returns:
        Zerstört den Root
    """

    end_sound()
    if messagebox.askokcancel("Beenden", "Wollen Sie das Programm beenden?"):
        root.destroy()


# 3.1.2 Funktion für den Klick auf "Los". Erst werden Validierungen der Felder durchlaufen, danach Übergang in 3.2
# tki.messagebox Generiert ein Pop-Up Window (Ausgestaltung je nach Typ, infobox / errorbox / ja oder nein Box)
# In Anlehnung an https://youtu.be/YXPyB4XeYLA?t=9133

def los_button():
    """Führt Input - Validierungen durch und prüft die Vollständigkeit / Korrektheit der übergebenen Daten
        Returns:
            Führt entweder in die nachfolgende Funktion oder beendet mit einer Messagebox (Error, Hinweis)
    """

    if radio_var and radio_var.get() == 0:
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte ein Ausgabeformat angeben!")
    if ks and ks.get() == 'Kraftstoff wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte einen Kraftstoff angeben!")
    if r and r.get() == 'Radius wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte einen Radius angeben!")
    if sa and sa.get() == 'Sortierung wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte eine Sortierung angeben!")
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
                return tki.messagebox.showerror("Falscher Input",
                                                f"Die eingegebene Adresse '{adresse.get()}' ist keine "
                                                f"Postleitzahl in Deutschland")
        else:
            error_sound()
            return tki.messagebox.showerror("Falscher Input", f"Die eingegebene Adresse '{adresse.get()}' ist keine "
                                                              f"Postleitzahl")
    else:
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte eine Postleitzahl angeben!")


# 3.1.3 Funktion für die Kontrollfrage

def popup(data):
    """Initiiert eine abschließende Ja/Nein Frage, vor dem Stellen der Anfrage an die API
    Input:
        Data Numy-Dictionary mit der Longitude / Langitude aus der Funktion los_button
    Returns:
        Ruft bei Positiver Checkbox-Auswahl die api_check Funktion auf und übergibt das Data-Dict.
    """

    info_sound()
    response = tki.messagebox.askyesno("Bitte bestätigen", "Sind Sie mit der Auswahl einverstanden?")
    tki.Label(tab1, text=response)

    if response == 1:
        return api_check(data)
    else:
        error_sound()
        response = tki.messagebox.showerror("Anfrage gestoppt", "Die Anfrage wurde abgebrochen. Bitte Daten prüfen")
        return tki.Label(tab1, text=response)


# 3.1.4 Funktion für den Einstieg in die Generierungsfunktionen, baut API Verbindung auf

def api_check(data):
    """Part 2 - Aufruf der API
    Baut den API-Aufruf auf und führt diesen durch.
    Input:
        Data Numpy-Dictionary mit der Longitude / Langitude aus der Funktion popup
    Returns:
        Beendet die Funktion bei einem nicht-erfolgreichen API-Aufruf, oder verzweigt
        in eine der Output-Funktionen (mit Uebergabe des Ergebnisses aus dem API-Aufruf)
    """

    # https://creativecommons.tankerkoenig.de/
    # Dein API-Key ist c7f5f8e5-e352-81d0-7d49-996d13f53d26

    key = "c7f5f8e5-e352-81d0-7d49-996d13f53d26"
    # Code für radius von https://stackoverflow.com/questions/1450897/remove-characters-except-digits-from-string
    # -using-python. Es wandelt den Radius-Input (zB 5km) in ein Float Objekt für den Api Aufruf um, siehe Doku
    radius = float(''.join(filter(str.isdigit, r.get())))
    kraftstoff_dict = {'Diesel': 'diesel', 'Super': 'e5', 'Super E10': 'e10'}  # wandelt den Kraftstoff-Input (Diesel)
    # in den vom Api unterstützen String um
    kraftstoff = kraftstoff_dict[ks.get()]
    active_flag = aktiv_checkbox()
    # Wandelt den Input (Preis, Entfernung) in das benötigte Objekt für die API um (price, dist).
    sortierung_dict = {'Preis': 'price', 'Entfernung': 'dist'}
    sortierung = sortierung_dict[sa.get()]
    active_flag = aktiv_checkbox()

    open_list = []
    full_list = []

    try:
        api_request = requests.get(
            f"https://creativecommons.tankerkoenig.de/json/list.php?lat={data['lat']}&lng={data['lon']}&rad={radius}"
            f"&sort={sortierung}&type={kraftstoff}&apikey={key}")
        api = json.loads(api_request.content)
    except Exception as e:
        api = f"Error..{e}"

    # API Troubleshooting falls ok == False (z.B. wenn Website down, Key tot .. )
    if api and api.get('ok') is False:
        info_sound()
        return tki.messagebox.showinfo("Fehler in der Verbindung", api.get("message"))

    for i in api.get("stations"):
        if active_flag:
            if not i.get("isOpen"):
                continue
            else:
                open_list.append(i)
        else:
            full_list.append(i)

    if len(open_list) <= 0:
        new_list = full_list
    else:
        new_list = open_list

    # Einstieg in die Ausgabefunktionen

    if radio_var.get() == 1:
        return csv_export(new_list)
    if radio_var.get() == 2:
        return pdf_export(new_list)
    if radio_var.get() == 3:
        map_export(new_list, data, radius)


# 3.1.5 Funktion löscht die PLZ - Eingabemaske bei Klick in das Feld 'Adresse' (überschreibt den Default Text)
# übernommen von https://www.tutorialspoint.com/how-to-clear-text-widget-content-while-clicking-on-the-entry-widget
# -itself-in -tkinter

def click(event):  # es muss ein parameter in die Funktion übergeben werden
    """Sorgt für eine Leerung des Adress-Feldes beim initialen Klick in das Feld
    Input:
        Event-Parameter
    Returns:
        kein Return-Wert
    """

    adresse.configure()
    adresse.delete(0, tki.END)
    return adresse.unbind('<Button-1>', clicked)


# 3.1.6 Funktion für die Generierung der Streetmap in einem zweiten Fenster, falls angeklickt im radio-button
# Quelle :   https: // github.com / TomSchimansky / TkinterMapView

def map_export(new_list, data, radius):
    """Startet ein neues Fenster in TKinter für die Map-Ausgabe
    Input:
        Liste aus der api_check Funktion
    Returns:
        kein Return-Wert
    """
    # ggf. sind globale variablen notwendig um korrekt in das neue frame transportiert zu werden
    newframe = tki.Toplevel()
    newframe.title('Mapview')
    newframe.iconbitmap('./icon/gasstation_4334.ico')
    newframe.geometry("1200x800")

    karte = tkintermapview.TkinterMapView(newframe, width=1200, height=800, corner_radius=0)
    karte.place(relx=0.5, rely=0.5, anchor=tki.CENTER)

    karte.set_position(data['lat'], data['lon'])
    if radius == 1:
        karte.set_zoom(14)
    elif radius == 2:
        karte.set_zoom(13)
    elif radius == 5:
        karte.set_zoom(12)
    elif radius == 10:
        karte.set_zoom(11)
    else:
        karte.set_zoom(10)

    for gas_station in new_list:
        gas_station_text = gas_station["brand"] + "  " + str(gas_station["price"])
        karte.set_marker(gas_station["lat"], gas_station["lng"], text=gas_station_text)


# 3.1.7 Funktion für die Generierung des csv Exports, falls angeklickt im radio-button

def csv_export(new_list: list):
    """Erstellt eine Tabelle aus den Daten, die durch die API angefragt werden und speichert diese als csv.

    Args:
        new_list (list): Liste mit multiplen dicts. Je Zeile ein dict.
    """

    # erstellt dataframe aus den dicts
    df = pd.DataFrame(new_list)
    # jeder Export erhält einen datetime Stempel
    export_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # öffnet Datei Explorer damit man den Pfad aussuchen kann, wo die csv gespeichert werden soll
    dir_name = askdirectory()
    # Dateinamen mit Zeitstempel erstellen und Pfad zusammenfügen
    file_name = f'csv_export_{export_time}.csv'
    file_path = os.path.join(dir_name, file_name)
    # Dataframe als csv exportieren
    try:
        df.to_csv(file_path, index=False, encoding='utf-8')
        info_sound()
        return tki.messagebox.showinfo('CSV-Export', 'CSV erfolgreich generiert.')
    except Exception as e:
        print(e)
        return


# 3.1.8 Funktion für die Generierung des pdf Exports, falls angeklickt im radio-button

def pdf_export(new_list):
    """Funktion für die Ergebnisausgabe im PDF-Format
    Input:
        Liste aus der api_check Funktion
    Returns:
        kein Return-Wert
    """

    # Erstelle ein leeres Tuple für spätere Bildung von Tuple in Tuple
    TABLE_DATA = ()
    # Estelle eine Interims Liste mit Tuples aus der übergebenen new_list, die Zahlen (PLZ, Preis) müssen Strings sein
    interim = [(d['brand'].title(), str(d['postCode']), str(d['dist']), str(d['price'])) for d in new_list]
    # Erstelle einen Tuple of Tuples für die render Funktion
    for entry in interim:
        if entry[0] == "": continue # Aussteuern von Tankstellen ohne Brand, um Leere Felder im PDF zu verhindern
        TABLE_DATA += (entry,)
    TABLE_COL_NAMES = ("Tankstelle", "Postleitzahl", "Entfernung in km", "Preis in EUR")
    title = "Tankstellen in deiner Nähe"

    class PDF(FPDF):
        def header(self):
            # Logo
            self.image("./icon/pdf_hintergrund_bild.jfif", 10, 8, 25)
            # font
            self.set_font('helvetica', 'B', 20)
            # Calculate width of title and position
            title_w = self.get_string_width(title) + 6
            # Start Punkt für Titel definieren
            doc_w = self.w
            self.set_x((doc_w - title_w) / 2)
            # colors of frame, background, and text
            self.set_draw_color(0, 80, 180)  # border = blue
            self.set_fill_color(230, 230, 0)  # background = yellow
            self.set_text_color(50, 50, 200)  # text = blue
            # Title
            self.cell(title_w, 10, title, border=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=True)
            # Line break
            self.ln(30)

        # Page footer
        def footer(self):
            # Set position of the footer
            self.set_y(
                -15)  # dieser Wert ist negativ, weil ich 15 mm von der unterkante messen möchte, bei positivem Wert misst man von der oberkante
            # set font
            self.set_font('helvetica', 'I', 8)
            # Page number
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)
    pdf = PDF('p', 'mm', 'A4')
    # Anzahl der Seitenanzahl
    pdf.alias_nb_pages()
    # eine Seite hinzufügen
    pdf.add_page()
    pdf.cell(0, 10, 'Tankerkönig Homepage', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link="https://creativecommons.tankerkoenig.de/")
    pdf.set_font("Times", size=10)
    # pdf.set_text_color(220,0,0)
    pdf.set_auto_page_break(auto=True, margin=15)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4

    # datetime objekt enthält aktuelles Datum in Format # dd/mm/YY
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    # Anfrage über Explorer zu Speicherort
    dir_name = tki.filedialog.askdirectory()
    # definition der Zusammensetzung des output_file_names
    file_name = f"pdf_export_{day} {month} {year}.pdf"
    # kombination der pfadnamen zu einem vollständigen pfad
    file_path = os.path.join(dir_name, file_name)

    # siehe https://pyfpdf.github.io/fpdf2/Tables.html (repeat table header on each page)

    def render_table_header():
        pdf.set_font(style="B")  # enabling bold text
        for col_name in TABLE_COL_NAMES:
            pdf.cell(col_width, line_height, col_name, border=1, align='C')
        pdf.ln(line_height)
        pdf.set_font('helvetica', style="")  # disabling bold text

    render_table_header()

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header()
        for column in row:
            # fixes UnicodeEncodeError if character is not latin1
            column = column.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, line_height, column, border=1, align='C')
        pdf.ln(line_height)
    try:
        pdf.output(file_path)
        info_sound()
        return tki.messagebox.showinfo('PDF-Export', 'PDF erfolgreich generiert.')
    except Exception as e:
        print(e)
        return

# 3.1.9 Funktion, um nur aktive Tankstellen anzuzeigen. Soll je nach Checkbox Status ein True (checked)
# oder ein False returnen. Wird über die export Funktionen geprüft (if aktiv_checkbox() is True ..)

def aktiv_checkbox():
    """Funktion prüft die Checkbox "nur aktive Tankstellen anzeigen"
    Returns:
        Boolean
    """

    if check_var.get() == 1:
        return True
    else:
        return False


# 3.1.9.1 Sound - Funktionen

def info_sound():
    """Funktion für den Infosound
    Returns:
        kein Wert
    """

    info = pygame.mixer.Sound(r".\sounds\Control.mp3")
    info.play()
    return


def error_sound():
    """Funktion für den Errorsound
    Returns:
        kein Wert
    """

    error = pygame.mixer.Sound(r".\sounds\Windows.mp3")
    error.play()
    return


def end_sound():
    """Funktion für den Beendensound
    Returns:
        kein Wert
    """

    end_sound = pygame.mixer.Sound(r".\sounds\Shutdown.mp3")
    end_sound.play()
    return


def music_control():
    """Funktion für den Start/das Ende der Hintergrundmusik
    Returns:
        kein Wert
    """
    global SOUNDCHECK

    if SOUNDCHECK is True:
        SOUNDCHECK = False
        return pygame.mixer.music.stop()
    else:
        SOUNDCHECK = True
        return pygame.mixer.music.play(loops=-1)


# 3.2.0 Funktionen für den Prognose und Historie - Tab
# 3.2.1 Funktion für den Los-Button

def los2_button():
    """Funktion für den Losbutton im zweiten Tab für Historie und Prognose
    Returns:
        Einstieg in Prognose oder Historie Funktion
    """

    if ks_p and ks_p.get() == 'Kraftstoff für Zukunftsprognose wählen':
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte einen Kraftstoff wählen!")
    if prog_var and prog_var.get() == 0:
        info_sound()
        return tki.messagebox.showinfo("Fehlender Input", "Bitte die Anzahl der Datenpunkte angeben!")
    else:
        info_sound()
        return prognose_threaded()

def los3_button():
    """Funktion für den Losbutton im dritten Tab für Historie
    Returns:
        Ruft die Historien Funktion auf
    """

    return historie_threaded()

def historie_threaded():
    """Funktion zum Aufruf der Funktion History() in einem eigenen Thread, um nicht den mainloop einzufrieren
    Returns:
            s.o.
    """

    return Thread(target=historie).start()


def historie():
    """Funktion für die Historie, öffnet das Dashboard für die historischen Daten. Subprocess ist notwendig,
    damit der Kind-Prozess (das Dashboard) unabhängig vom Hauptprozess (GUI) laufen kann
    Returns: Startet die Dashboard Funktion
    """

    # subprocess code in anlehnung an https://stackoverflow.com/questions/14797236/python-howto-launch-a-full-process
    # -not-a-chil d-process-and-retrieve-the-pid
    # browser doc. https://docs.python.org/3/library/webbrowser.html

    info_sound()
    tki.messagebox.showinfo("Achtung",
                            "Dies startet ein vom GUI getrenntes Python-Skript. Zum Beenden der Verbindung zum "
                            "Dashboard "
                            "muss das Terminal geschlossen werden. Das Schließen des GUI reicht nicht aus!")
    path = Path().absolute()
    command_dir = path / 'src' / 'dashboard' / 'main.py'
    webbrowser.open('http://127.0.0.1:8050', new=1, autoraise=True)
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    ps = subprocess.Popen(['python', f'{command_dir}'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    return ps.communicate()


def prognose_threaded():
    """Funktion für die Prognose des Preises des nächsten Tages, für alle Kraftstoffe
    Returns:
        startet die Hauptfunktion für die Prognose in einem eigenen Thrad
    """

    return Thread(target=prognose).start()


def prognose():
    """Funktion für die Prognose des Preises des nächsten Tages, für alle Kraftstoffe
    Returns:
        zeigt den prognostizierten Preis für den gewählten Kraftstoff in einem Popup
    """
    # Code in Anlehnung an https://www.youtube.com/watch?v=PuZY9q-aKLw&t=1570s

    info_sound()
    tki.messagebox.showinfo("Disclaimer", "Es handelt sich hierbei um eine Schätzung, basierend auf den von "
                                          "'Tankerkoenig' für Nordrhein-Westfalen zur Verfügung gestellten "
                                          "historischen "
                                          "Daten seit 2019. Die Berechnung beginnt nach einem Klick auf 'OK'.")

    # Umwandlung des Inputs in das Column-name der Excel
    prognose_kraftstoff_dict = {'Diesel': 'diesel', 'Super': 'e5', 'Super E10': 'e10'}
    prognose_kraftstoff = prognose_kraftstoff_dict[ks_p.get()]

    # Heranziehen der historischen Daten Datei und Filterung für Preisdaten in NRW
    path = Path().absolute()
    DATA_PATH = f'{path}\data\historical_data.csv'
    dataset = pd.read_csv(DATA_PATH, sep=",", header=0)
    dataset_interim = dataset[[f"bundesland", f"{prognose_kraftstoff}"]]
    dataset_fin = dataset_interim[dataset_interim["bundesland"] == 'Nordrhein-Westfalen']
    prices = dataset_fin[prognose_kraftstoff]

    # Skaliert alle vorhandenen Daten in eine Range zwischen 0 und 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset_fin[prognose_kraftstoff].values.reshape(-1, 1))
    start = time.time()

    # wie viele Einträge aus der Vergangenheit möchte ich heranziehen, um den Preis für den nächsten Tag zu berechnen.
    # Hat großen Einfluss auf die Berechnungsgeschwindigkeit, aber auch auf die Modell-Genauigkeit. Ein Wert von
    # 1000 benötigt etwa 10 Minuten Rechenzeit

    prog_dict = {1: 60, 2: 250, 3: 1000}
    prediction_days = prog_dict[prog_var.get()]

    x_train = []
    y_train = []

    # startet beim gewählten Index und zählt hoch bis zum letzten Index

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build the Model

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # prediction of the next closing value

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    model_inputs = prices.values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    real_data = [model_inputs[len(model_inputs)-prediction_days:len(model_inputs+1), 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)

    end = time.time()
    elapsed = end - start
    print('Elapsed time is %f seconds.' % elapsed)


    tki.messagebox.showinfo("Ergebnis", f"Der Kraftstoff {ks_p.get()} hat für den {NextDay_Date_Formatted} einen "
                                        f"prognostizierten Preis von EUR {prediction[0][0]:.4f}. "
                                        f"Die Berechnung brauchte {round(elapsed, 3)} Sekunden"
                                        f" bei einer Iteration über {prediction_days} Datenpunkten.")


"""
Part 1 - Erstellen des GUI und der benötigten Buttons / Tabs
Das Erstellen dieser Objekte mit Tkinter ist ein zweistufiger Prozess - erst wird das "Widget" definiert
(alles in Tkinter ist ein Widget) und dann in das Fenster (d.h. in den root) geplottet.
"""

# 1.1 Initiieren der Startbefehle

root = tki.Tk()  # erstellt das Root-Fenster für alle weiteren Widgets (d.h. Buttons etc)
root.title("PKI - Fuel Guru")  # bennent das Fenster
root.geometry("550x620")  # setzt die Maße, Breite x Höhe
root.iconbitmap('./icon/gasstation_4334.ico')  # Iconanpassung
path = Path().absolute()  # greift das aktuelle Arbeitsverzeichnis ab
command_dir = f'{path}\src\dashboard\main.py'  # setzt den Pfad für das Historische Daten Dashboard
root.protocol("WM_DELETE_WINDOW", on_closing)  # Protokoll - Handling für (window) close event
NextDay_Date = datetime.today() + timedelta(days=1)
NextDay_Date_Formatted = NextDay_Date.strftime ('%d-%b-%Y')

# Setzen der derzeitigen User-Postleitzahl im Adressfeld(näherungsweise)
# Code von https://stackoverflow.com/questions/24906833/how-to-access-current-location-of-any-user-using-python
# und https://gis.stackexchange.com/questions/352961/convert-lat-lon-to-zip-postal-code-using-python

geocode = geocoder.ip('me')  # holt die Koordinaten des GUI Nutzers
geo_locator = geopy.Nominatim(user_agent='1234')
location = geo_locator.reverse(geocode.latlng)
zipcode = location.raw['address']['postcode']

# Hintergrundmusik

SOUNDCHECK = True
pygame.mixer.init()  # initialisiert Sounds
pygame.mixer.music.load(r".\sounds\background.mp3")
pygame.mixer.music.set_volume(0.0079)
pygame.mixer.music.play(loops=-1)

# Setzen von verschiedenen Tabs mithilfe von TTK-Widgets

notebook = ttk.Notebook(root)  # TTK Widget, ist quasi ein Array / eine Sammlung von Widgets
tab1 = tki.Frame(notebook)  # Frame für Tab 1
tab2 = tki.Frame(notebook)  # Frame für Tab 2
tab3 = tki.Frame(notebook)  # Frame für Tab 3
tab4 = tki.Frame(notebook)
notebook.add(tab1, text="Hauptfunktionen")  # Füllt die Tabs in das kreierte Notebook
notebook.add(tab2, text="Prognosen")
notebook.add(tab3, text="Historie")
notebook.add(tab4, text="Musik-Einstellungen")
notebook.pack(expand=True, fill="both")

# Einfügen von Hintergrundbildern für die Tabs
# Canvas sind grafische html-basierte Elemente der TK Klasse

bg = ImageTk.PhotoImage(Image.open("./icon/bg.jpg"))
canvas = tki.Canvas(tab1)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

bg2 = ImageTk.PhotoImage(Image.open("./icon/graph.jpg"))
canvas2 = tki.Canvas(tab2)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, image=bg2, anchor="nw")

bg3 = ImageTk.PhotoImage(Image.open("./icon/graph.jpg"))
canvas3 = tki.Canvas(tab3)
canvas3.pack(fill="both", expand=True)
canvas3.create_image(0, 0, image=bg3, anchor="nw")

bg4 = ImageTk.PhotoImage(Image.open("./icon/musik_bg.jpg"))
canvas4 = tki.Canvas(tab4)
canvas4.pack(fill="both", expand=True)
canvas4.create_image(0, 0, image=bg4, anchor="nw")

photo_music = tki.PhotoImage(file=r"./icon/speaker-2488096_1280.png")
small_image_music = photo_music.subsample(15, 15)

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

# 1.2.4 Ausgabeformat - muss singlechoice - klick ('radiobutton') sein (Wahl: CSV / PDF / Streetmap)

canvas.create_text(110, 145, text="Ausgabeformat wählen", fill="white", font='Helvetica 13 bold')

radio_var = tki.IntVar()  # die Variable wird als ein Integer definiert, um später in einer Funktion mit
# Zahlen arbeiten zu können. Alternativ wäre z.B. auch StrVar() möglich, wenn der value "1" gewählt wird

output_csv = tki.Radiobutton(tab1, text="CSV", variable=radio_var,
                             value=1, activebackground='green')  # Tkinter nutzt eine eigene Syntax für Variablen
output_pdf = tki.Radiobutton(tab1, text="PDF", variable=radio_var, value=2, activebackground='green')
output_map = tki.Radiobutton(tab1, text="Streetmap", variable=radio_var, value=3, activebackground='green')

# 1.2.5 Start und Ende - müssen 'normale' Buttons sein

los = tki.Button(tab1, text="Los", padx=80, pady=60,
                 command=los_button)
ende = tki.Button(tab1, text='Beenden', padx=60, pady=60, command=ende_button)

# 1.2.6 nur offene Tankstellen anzeigen - Checkbox Button

check_var = tki.IntVar()
aktiv = tki.Checkbutton(tab1, width=20, text="nur geöffnete Tankstellen", variable=check_var,
                        command=aktiv_checkbox)
check_var.get()

# 1.2.7 Sortierungsmoeglichkeiten als Drop-Down (Sven Simon Szczesny)

sortierung_liste = [

    "Preis",
    "Entfernung"
]

sa = tki.StringVar()
sa.set("Sortierung wählen")
sortierung = tki.OptionMenu(tab1, sa, *sortierung_liste)

# 1.2.8 Hintergrundmusik aktivieren/deaktivieren

musik_an = tki.Button(tab4, image=small_image_music, text="Musik aus/an", compound=tki.LEFT, padx=50, pady=30,
                      command=music_control)
CreateToolTip(musik_an, text='Toggle um die Hintergrundmusik zu aktivieren bzw. zu deaktivieren')

# 1.3 Kreieren von Historie-, Prognose-, und Musikbutton(s)
# 1.3.1 Start und Ende - müssen 'normale' Buttons sein

los2 = tki.Button(tab2, text="Los", padx=80, pady=60,
                  command=los2_button)
los3 = tki.Button(tab3, text="Historisches Daten Dashboard", width=72, height=7,
                  command=los3_button)
CreateToolTip(los3, text='Toggle um das Dashboard für die historischen Daten im Browser zu öffnen')
ende2 = tki.Button(tab2, text='Beenden', padx=60, pady=60, command=ende_button)
ende3 = tki.Button(tab3, text='Beenden', width=72, height=8, command=ende_button)  # der Vollständigkeit halber
ende4 = tki.Button(tab4, text='Beenden', padx=60, pady=60, command=ende_button)  # der Vollständigkeit halber

# 1.3.3 Buttons um die Prognose für einen Kraftstoff zu spezifizieren

ks_p = tki.StringVar()
ks_p.set("Kraftstoff für Zukunftsprognose wählen")
prognose_kraftstoff = tki.OptionMenu(tab2, ks_p, *kraftstoff_liste)
prognose_kraftstoff.config(width=77, height=5)

# 1.3.4 Buttons um die Stichgröße für die Prognose zu steuern

prog_var = tki.IntVar()
prognose1 = tki.Radiobutton(tab2, text="60 Datenpunkte", variable=prog_var,
                            value=1, activebackground='green', bd=10)
prognose2 = tki.Radiobutton(tab2, text="250 Datenpunkte", variable=prog_var, value=2, activebackground='green', bd=10)
prognose3 = tki.Radiobutton(tab2, text="1000 Datenpunkte", variable=prog_var, value=3, activebackground='green', bd=10)

p_l = [prognose1, prognose2, prognose3]

for element in p_l:
    CreateToolTip(element, text='Dieses Feld bestimmt die Anzahl der Datenpunkte, die das Modell für die Berechnung'
                                ' des zukünftigen Preises zugrunde legt.\n'
                                'Die Genauigkeit der Prognose steigt in der Theorie mit der Anzahl der Datenpunkte - '
                                'in jedem Fall steigt aber die Verarbeitungsdauer.\n'
                                'Bei 1000 Punkten beträgt die Rechenzeit etwa 10 Minuten.\n'
                  )

# 1.4 Plotten der Hauptfunktions - Buttons in das Tab 1 GUI - Fenster
# Es wurde mit place und manuellen Koordinatenübergabe gearbeitet. Alternativ wäre auch .pack() oder .grid mit row &
# columns für die Platzierung möglich gewesen.

adresse.place(x=20, y=20)
radius.place(x=400, y=20)
kraftstoff.place(x=230, y=20)
sortierung.place(x=230, y=80)
output_csv.place(x=20, y=190)
output_pdf.place(x=20, y=240)
output_map.place(x=20, y=290)
los.place(x=340, y=430)
ende.place(x=20, y=430)
aktiv.place(x=20, y=80)

# 1.5 Plotten der Buttons in das Tab 2 des GUI - Fensters

prognose_kraftstoff.place(x=20, y=50)
prognose1.place(x=20, y=250)
prognose2.place(x=200, y=250)
prognose3.place(x=380, y=250)
los2.place(x=340, y=430)
ende2.place(x=20, y=430)

# 1.6 Plotten der Buttons in das Tab 3 des GUI - Fensters

los3.place(x=20, y=50)
ende3.place(x=20, y=400)

# 1.7 Plotten der Buttons in das Tab 4 des GUI - Fensters

musik_an.place(x=120, y=80)
ende4.place(x=20, y=430)

# 1.8 Mainloop

root.mainloop()  # führt eine Endlosschleife durch (startet das sichtbare GUI-Fenster)
