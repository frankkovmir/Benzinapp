# Allgemein

Der aktuelle Stand des aggregierten historischen Datensatzes beinhaltet Daten bis zum 12.01.2023 und ist dem Projekt beigefügt.
Die historical_data.py ermöglicht es, einen aggregierten Datensatz herzustellen, falls noch keiner vorhanden ist oder den bereits vorhanden mit neuen Daten zu füllen,
wenn bereits neue Daten vorhanden sind. Diese Datei kann allerdings nur ausgeführt werden wenn folgende Bedingungen erfüllt sind.

## Verbindung zum Tankerkönig Repository herstellen

Da das Skript die historischen Daten des Tankerkoenig Repos verwendet muss dieses zunächst geklont werden.
Auch das aktualisieren der Daten geschieht über einen git Befehl innerhalb des Skripts.

## Klonen des Tankerkönig Repositorys

Das Tankerkönig Repository muss in den data Ordner des Stammverzeichnisses geklont werden.
Folgende Befehle vom Stammverzeichnis des Projekts ausführen.

```shell
cd data
```
Das Klonen kann über HTTPS oder SSH stattfinden.

Klonen per HTTPS
```shell
git clone https://tankerkoenig@dev.azure.com/tankerkoenig/tankerkoenig-data/_git/tankerkoenig-data
```
Klonen per SSH
```shell
git clone git@ssh.dev.azure.com:v3/tankerkoenig/tankerkoenig-data/tankerkoenig-data
```

Dieser Vorgang kann einige Zeit dauern, da sehr viele Daten runtergeladen werden.
Aus demselben Grund war es nicht möglich, das Tankerkönig Repository direkt ins Projekt zu integrieren.

## Ausführen der historical_data.py

Sobald das Repository erfolgreich geklont wurde und sich in dem Verzeichnis 'Benzinapp/data' des Projekts befindet,
ist es möglich das Skript auszuführen. Da bereits ein aggregierter Datensatz mitgeliefert wird, wird dieser durch das Programm aktualisiert.
Möchte man die initiale Erstellung des Datensatzes testen, kann die 'historical_data.csv' im selben Ordner 'Benzinapp/data' gelöscht werden.
Es ist anzuraten, vorher eine Sicherheitskopie anzulegen, falls doch Probleme auftreten sollten, kann die Sicherheitskopie wieder in den Ordner eingefügt werden.
Ohne diese CSV ist die Ausgabe des Dashboards nicht möglich.
Es ist weiterhin zu erwähnen, dass die initiale Erstellung des aggregierten Datensatzes ca. eine Stunde Zeit in Anspruch nimmt.