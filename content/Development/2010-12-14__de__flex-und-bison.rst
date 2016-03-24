======================================
Binärtaschenrechner mit Flex und Bison
======================================


:tags: Bison, Flex
:author: Markus Holtermann


Einen Taschenrechner für Binärzahlen kann man mit `Flex
<http://flex.sourceforge.net/>`_ und `Bison
<http://www.gnu.org/software/bison/>`_ recht schnell erstellen. Zunächst
erstellen wir eine Datei *calc_binary.l*. Diese ist der sogenannte Lexer:

.. code-block:: c

    %{
    #include "calc_binary.y.h"
    %}
    %%
    \+ { return PLUS;}
    -  { return MINUS;}
    \* { return MAL;}
    0  { return NU;}
    1  { return EINS;}
    \( { return AUF; }
    \) { return ZU; }
    \n { return AUS; }
    [ ]+ ;
    .  { printf("what?");}

Diese Datei übersetzen wir dann mit::

    $ flex -o calc_binary.c calc_binary.l

Nun folgt der Parser, ein Bison-File, mit dem Namen *calc_binary.y*:

.. code-block:: c

    %{
    #include <stdio.h>
    #include <math.h>
    void yyerror(char *message);
    %}

    %start S

    %token AUS
    %token PLUS MINUS
    %token MAL
    %token NU EINS
    %token AUF ZU

    %left PLUS MINUS
    %left MAL

    %%
    S : E AUS {printf("= %d\n ", $1); }
      | S E AUS {printf("=%d\n ", $2);};

    E : B {$$ = $1;}
      | E PLUS E {$$ = $1 + $3;}
      | E MINUS E {$$ = $1 - $3;}
      | E MAL E {$$ = $1 * $3;}
      | AUF E ZU {$$ = $2;}
      | MINUS E {$$ = - $2;};

    B : NU {$$ = 0;}
      | EINS {$$ = 1;}
      | B NU {$$ = $1 * 2;}
      | B EINS {$$ = $1 * 2 + 1;};

    %%

    int main(int argc, char **argv) {
            yyparse();
            return 0;
    }

    void yyerror(char *message) {
            printf("Good bye\n");
    }

Auch diesen müssen wir übersetzen::

    $ bison -d -b y -o calc_binary.y.c calc_binary.y

Nun können wir mit GCC eine ausführbare Datei erstellen können::

    $ gcc calc_binary.c calc_binary.y.c -lfl -lm -o calc_binary

Wenn wir diese mit::

    $ ./calc_binary

aufrufen, können wir Binärzahlen addieren, subtrahieren und multiplizieren.
