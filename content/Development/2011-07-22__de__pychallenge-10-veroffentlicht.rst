==============================
pyChallenge 1.0 veröffentlicht
==============================


:tags: Django, Python, SQLite, Studium
:author: Markus Holtermann


Wie in meinem Artikel vom 26.05.2011 `angekündigt
<{filename}/Development/2011-05-26__de__neues-vom-studium.rst>`_, habe ich mit
einigen Kommilitonen in der Datenbankvorlesung das Projekt `pyChallenge
<https://github.com/MarkusH/pyChallenge>`_ entwickelt mit dem die Spielstärken
von Schach- oder Tennisspielern berechnet werden können. Dies geschieht anhand
der Algorithmen `ELO <http://de.wikipedia.org/wiki/Elo-Zahl>`_ und `Glicko
<http://de.wikipedia.org/wiki/Glicko-System>`_.

Weiterhin lassen sich mit `pyChallenge
<https://github.com/MarkusH/pyChallenge>`_ auch die Besten- und Schlechtesten-
Listen eines Spiels ausgeben, und die bestmöglichen Paarungen für einen jeden
Spieler errechnen.

Kern der gesamten Entwicklung lag aber auf dem `ORM
<http://de.wikipedia.org/wiki/Objektrelationale_Abbildung>`_, welches wir für
unsere Zwecke selber entwickelt haben. Das ORM nimmt uns nun folgende
Funktionen ab wodurch die Anwendungslogik sehr gut von der Datenrepräsentation
abgetrennt wird:

* ``INSERT INTO``
* ``SELECT FROM``
* ``UPDATE WHERE``
* ``DELETE FROM``
* ``CREATE TABLE``
* ``TRUNCATE TABLE``
* ``DROP TABLE``

Ein kurzes Beispiel, wie das ORM genutzt wird, ist `dort <https://github.com/Ma
rkusH/pyChallenge/blob/master/pychallenge/db/models.py#L17-L63>`_ zu sehen.

Dann bleibt uns nur noch Danke für das Testen und Nutzen zu sagen.

Ein Artikel zu dem Projekt *Dominator* aus der Software-Engineering Vorlesung,
folgt demnächst.


* Folge uns auf `github.com <https://github.com/MarkusH/pyChallenge/>`_
