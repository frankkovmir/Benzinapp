Benzinapp für das Gruppenprojekt in PKI. 
Teilnehmer: Sam Barjesteh, Hicham Ben Ayoub, Frank Kovmir, Sven Simon Szczesny

# Allgemein

Das Programm kann entweder über die FuelGuru.exe im Archiv ausgeführt, oder über einen Python Interpreter
mittels Kompilierung der main.py im Hauptordner gestartet werden. (Entweder durch Import des gesamten Ordners in eine IDE, oder per Shell-Aufruf).
In beiden Fällen ist es notwendig, dass sich der Icon-, der Sound-, und der historical_data Ordner im selben Verzeichnis befindet, wie die main.py bzw. FuelGuru.exe Datei.

# Ausführen per Terminal

  1.) Start des Terminals aus dem Download-Ordner des entpackten Archivs (cmd im Pfad des Fensters eingeben), oder Navigation per cd

2.) Auführen des Befehls python main.py

# Troubleshoot

Das Programm ist unter Windows entwickelt und getestet worden.
Sollten bei dem Aufruf der main.py importierte Module fehlen, so sind diese per pip install 'modulname' in die genutzte Umgebung zu installieren.

Teilweise kommt es Problemen bei dem Pygame Modul in Kombination mit AnaConda (o.ä.) aufgrund von einer fehlenden .dll Datei (libmpg123-0.dll). Diese sollten nur entstehen, wenn die main.py per IDE oder Terminal gestartet wird, nicht jedoch bei der .exe Datei.
Ein möglicher Workaround ist der manuelle Download einer passenden .whl (wheel) Datei. 

Die Installation sollte wie folgt erfolgen:

  1.) Aufruf https://www.lfd.uci.edu/~gohlke/pythonlibs/

2.) STRG+R und Suche nach "Pygame" (ohne Anführungsstriche)

3.) Ausführen des Terminals (CMD)

4.) Auführen des Befehls "pip debug --verbose" (ohne Anführungsstriche)

5.) Download einer unterstützen Pygame .whl Datei (siehe Sektion "Compatible tags" im Terminal)

6.) Start des Terminals aus dem Download-Ordner der Datei, oder Navigation zum Download-Ordner per cd

7.) Auführen des Befehls pip install "vollständiger heruntergeladener Dateiname"

8.) Nach Erfolgreicher Installation Neustart des Rechners und der IDE

