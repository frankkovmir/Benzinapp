# Allgemein

Benzinapp für das Gruppenprojekt in PKI. 
Teilnehmer: Sam Barjesteh, Hicham Ben Ayoub, Frank Kovmir, Sven Simon Szczesny

Das Programm kann entweder über die FuelGuru.exe im Archiv ausgeführt, oder über einen Python Interpreter
mittels Kompilierung der main.py im Hauptordner gestartet werden. (Entweder durch Import des gesamten Ordners in eine IDE, oder per Shell-Aufruf).
In beiden Fällen ist es notwendig, dass sich der Icon-, der Sound-, und der historical_data Ordner im selben Verzeichnis befindet, wie die main.py bzw. FuelGuru.exe Datei.

# Ausführen per Terminal

  1.) Start des Terminals aus dem Download-Ordner des entpackten Archivs (cmd im Pfad des Fensters eingeben), oder Navigation per cd
  
![grafik](https://user-images.githubusercontent.com/114833933/210898763-18ee6d49-f694-4f78-bd5a-357f041bf93b.png)


2.) Ausführen des Befehls python main.py

![grafik](https://user-images.githubusercontent.com/114833933/210898866-850e875c-3b5a-4988-a616-73f1e6f24414.png)


# Troubleshoot

Das Programm ist unter Windows entwickelt und getestet worden.
Sollten bei dem Aufruf der main.py importierte Module fehlen, so sind diese per pip install 'modulname' in die genutzte Umgebung zu installieren.

Teilweise kommt es Problemen bei dem Pygame Modul in Kombination mit AnaConda (o.ä.) aufgrund von einer fehlenden .dll Datei (libmpg123-0.dll). Diese sollten nur entstehen, wenn die main.py per IDE oder Terminal gestartet wird, nicht jedoch bei der .exe Datei.
Ein möglicher Workaround ist der manuelle Download einer passenden .whl (wheel) Datei. 

Die Installation sollte wie folgt erfolgen:

  1.) Aufruf https://www.lfd.uci.edu/~gohlke/pythonlibs/

![grafik](https://user-images.githubusercontent.com/114833933/210898649-ac85cb73-1968-44ff-8a67-8ff14a8b07f3.png)

2.) STRG+F und Suche nach "Pygame" (ohne Anführungsstriche)

3.) Ausführen des Terminals (CMD)

4.) Auführen des Befehls "pip debug --verbose" (ohne Anführungsstriche)

![grafik](https://user-images.githubusercontent.com/114833933/210898493-277714d3-47cf-4404-99a6-54396ed6492a.png)

5.) Download einer unterstützen Pygame .whl Datei (siehe Sektion "Compatible tags" im Terminal)

6.) Start des Terminals aus dem Download-Ordner der Datei, oder Navigation zum Download-Ordner per cd

7.) Auführen des Befehls pip install "vollständiger heruntergeladener Dateiname"

![grafik](https://user-images.githubusercontent.com/114833933/210898983-b4b586c3-f87f-4f18-8854-58289eaa00e6.png)

8.) Nach Erfolgreicher Installation Neustart des Rechners und der IDE

