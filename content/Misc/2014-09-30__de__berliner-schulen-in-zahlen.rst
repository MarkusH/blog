==========================
Berliner Schulen in Zahlen
==========================

:tags: Berlin, Projekte, Studium
:authors: Alexander Grießer, Markus Holtermann


Berlin. 2014. 1093 Bildungseinrichtungen. 835 Zeilen Javascript Code. 573
Zeilen HTML Code. 347 Zeilen Python Code. 31 Schularten. 29 Schulzweige. 19
Ausstattungskriterien. 15 Sprachen. 12 Stadtteile. 2 Möglichkeiten das selbe zu
sagen. 1 Seminar: Ini 2.0.

Wie soll man nun bei den ganzen Zahlen den Überblick bewahren? Das war die
Fragestellung mit wir uns im Seminar "Data Science -- Hacking Society" der Ini
2.0 im Sommersemester 2014 an der TU Berlin auseinandergesetzt haben. Aber
zunächst zurück zum Anfang des Projektes.

Im Wintersemester 13/14 fragten wir bei der Stadt Berlin Daten zu den
Bildungseinrichtungen im Stadtgebiet an. Dass die Stadt Berlin sehr
detaillierte Daten zu allen Bildungseinrichtungen erfasst, konnten wir anhand
der schon existierenden `Recherche Webseite`_ erahnen. Die Usability dieser
Webseite ist allerdings nicht die allerbeste, außerdem wollten wir auch die zu
Grunde liegenden Daten auswerten.

Bis die Anfrage nach den Daten befriedigend beantwortet wurde verging leider
recht viel Zeit, daher war im Wintersemester 2013/2014 nur noch Zeit zum ersten
Sichten und Aufräumen der Datensätze vorhanden. Uns wurde eine Reihe von
Excel-Dokumenten zur Verfügung gestellt, welche glücklicherweise sehr
ordentlich waren. Einen ersten Prototyp einer besseren Rechercheanwendung
konnten wir zwar beginnen, leider aber nicht fertig stellen.

Das gab den nachfolgenden Studenten im Sommersemester 2014 aber die Möglichkeit
mit einem schon vorhandenen Datensatz sehr schnell arbeiten zu können. Das Ziel
waren weitere Auswertungen der Daten, erneute Überprüfung der Datenqualität und
natürlich das Erstellen einer Webseite, welche die Recherche im Datensatz sehr
angenehm macht.


Datenqualität
=============

Trotz recht aktuellen Daten waren diese an vielen Stellen nicht 100% korrekt.
Das mitunter größte Fehlerpotential boten Links zu den Webseiten der
Bildungseinrichtungen. Etwa 10% aller Links waren fehlerhaft und verwiesen auf
nicht mehr existierende Seiten.

Obwohl die Daten zentral gesammelt werden, scheint die Erfassung nicht auf
elektronischem Wege, sondern nach wie vor mit Papierfragebogen und Stift
abzulaufen. Anders lassen sich inkonsistente Daten wie "Computerraum" und
"Computerräume" oder "Werkstatt" und "Werkstätten" nicht wirklich erklären.


Webanwendung
============

Bilder sagen mehr als tausend Worte, daher hier ein paar Eindrücke der
Webseite:

.. gallery::
   :small: 1
   :medium: 2

   .. image:: /images/berlin-school-data/school1tb.jpg
      :alt: Startseite
      :target: /images/berlin-school-data/school1.png

   .. image:: /images/berlin-school-data/school1tb.jpg
      :alt: Ein paar angewendete Filter
      :target: /images/berlin-school-data/school2.png

   .. image:: /images/berlin-school-data/school3tb.jpg
      :alt: Detailansicht einer Schule
      :target: /images/berlin-school-data/school3.png

   .. image:: /images/berlin-school-data/school4tb.jpg
      :alt: Heatmap Betreuungsschlüssel
      :target: /images/berlin-school-data/school4.png

   .. image:: /images/berlin-school-data/school5tb.jpg
      :alt: Impressum
      :target: /images/berlin-school-data/school5.png

Bis jetzt sind wir ohne technische Details ausgekommen, aber so ganz kommen wir
in diesem Abschnitt nicht drum herum. Die Webseite ist als sogenannte
`Single-Page-App`_ umgesetzt, so dass bei Benutzung des Filters oder bei der
Navigation immer nur Teile der Seite neu geladen werden. Designtechnisch haben
wir uns auf `Zurb's Foundation`_ verlassen und das Standardtheme praktisch
nicht angepasst, daher sieht das auch so gut aus ;) 

Für die dynamische Programmierung haben wir `AngularJS`_ verwendet, eine
Javascript Bibliothek welche wir anhand dieses Projekts kennen gelernt haben.
Die Daten der App lagern am Ende in einer `Elasticsearch Instanz`_ und können
über `AJAX`_ Zugriffe abgefragt werden.

Wer sich für den Code interessiert, diesen findet man in einem `öffentlichen
Github Projekt`_.

Ein Artikel zu den technischen Details wurde von Alex und Markus
`veröffentlicht`_.


Ausblick
========

Wir haben viel darüber gelernt wie aufwendig es ist solche Daten bei der
öffentlichen Verwaltung anzufragen. Ein Mitglied aus unserem Team ist auch
motiviert weiter zu machen, allerdings ist in Baden-Württemberg, trotz
Bestandteils des Koalitionsvertrags, noch kein Informationsfreiheitsgesetz in
Aussicht. Erwartungsgemäß ist die erste Anfrage nach einem ähnlich
umfangreichen Datensatz auch nicht zufriedenstellend beantwortet worden: einen
zentralen Datensatz gibt es nicht. Noch dazu soll für eine Auflistung aller
Adressen über 100 EUR gezahlt werden. Der nächste Schritt ist dort also mal auf
entsprechende Landtagsabgeordnete zuzugehen und sie an gewisse Inhalte ihres
Koalitionsvertrags zu erinnern.


.. _Recherche Webseite:
   http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/
.. _Single-Page-App: http://en.wikipedia.org/wiki/Single-page_application
.. _Zurb's Foundation: http://foundation.zurb.com/
.. _AngularJS: https://angularjs.org/
.. _Elasticsearch Instanz: http://www.elasticsearch.org/
.. _AJAX: http://de.wikipedia.org/wiki/Ajax_%28Programmierung%29
.. _öffentlichen Github Projekt:
   https://github.com/Markush2010/berlin-school-data
.. _veröffentlicht:
   {filename}/Development/2014-08-10__en__using-elasicsearch-as-relational-data-storage.rst
