======================
Dominator 1.0 released
======================


:tags: Arch, C/C++, Debian, Eclipse, Git, KDE, Linux, Studium, Ubuntu, Windows
:author: Markus Holtermann


As a result of my fourth semester at the university, my team and I created the
`DOMINATOR <{filename}/Development/2011-05-26__de__neues-vom-studium.rst>`_
(de) program, an `OpenGL 2.1 <http://en.wikipedia.org/wiki/OpenGL#OpenGL_2.1>`_
based 3D domino simulation. You can find a demo video at `YouTube
<http://www.youtube.com/watch?v=H2vHt1vh1Sg>`_.

.. gallery::
   :small: 1

   .. image:: dominator-1.0-screenshot.png
      :alt: Dominator 1.0 Screenshot

In round about 13,000 lines of C++ code we solved this exercise. As a UI
framework we decided to make use of the `Qt framework
<http://en.wikipedia.org/wiki/Qt_(framework)>`_ which has perfect OpenGL
integration. The `lib3ds <https://code.google.com/p/lib3ds/>`_ and the `Newton
Game Dynamics <http://newtondynamics.com/>`_ are used to import 3DS models and
calculate the physical environment. Several `3rd-party libraries
<https://github.com/MarkusH/dominator/wiki/Third-Party-Libraries>`_ finalize
the set of external software that we use for our project.

DOMINATOR 1.0 officially supports Microsoft Windows 7 and Ubuntu 10.04 (Lucid
Lynx) and 10.10 (Maverick Meerkat). I tested it on Arch Linux as well and even
developed it on my Arch Linux systems. But there is no install script for Arch
right now, sorry for that, but you can easily compile it from source. See the
links below and have a brief look at the `development installation docs
<https://github.com/MarkusH/dominator/wiki/Installation>`_. In theory Mac OSX
should be supported as well, but we couldn't get Newton Game Dynamics compiled.

And here's `the code on Github <http://github.com/MarkusH/dominator>`_.

Markus

