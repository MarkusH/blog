====================
Mandelbrot in Python
====================


:tags: Arch Linux, Linux, PyPy, Python
:author: Markus Holtermann
:summary: I just found a nice Python script that draws the Mandelbrot set. Have
   a look!


I just `found <http://preshing.com/20110926/high-resolution-mandelbrot-in-obfuscated-python>`_
a nice Python script that draws the `Mandelbrot set <http://en.wikipedia.org/wiki/Mandelbrot_set>`_.


.. code-block:: python

    _                                      =   (
                                            255,
                                          lambda
                                   V       ,B,c
                                 :c   and Y(V*V+B,B,  c
                                   -1)if(abs(V)&lt;6)else
                   (              2+c-4*abs(V)**-0.4)/i
                     )  ;v,      x=1500,1000;C=range(v*x
                      );import  struct;P=struct.pack;M,\
                j  ='&lt;QIIHHHH',open('M.bmp','wb').write
    for X in j('BM'+P(M,v*x*3+26,26,12,v,x,1,24))or C:
                i  ,Y=_;j(P('BBB',*(lambda T:(T*80+T**9
                      *i-950*T  **99,T*70-880*T**18+701*
                     T  **9     ,T*i**(1-T**45*2)))(sum(
                   [              Y(0,(A%3/3.+X%v+(X/v+
                                   A/3/3.-x/2)/1j)*2.5
                                 /x   -2.7,i)**2 for  \
                                   A       in C
                                          [:9]])
                                            /9)
                                           )   )


You can change the output dimension in line 8. Just make sure that the width is
dividable by 4.

I ran the script with a resolution of 3000x2000 px on my T400 with an Intel
Core2Duo P8600 @ 2.40GHz and 4GB RAM. I used Python 2.7.2-2 on Arch Linux 64bit
and it took took me half an our. And as stated in the article as well, PyPy
1.6-2 should be much faster. And I can confirm that. It only runs half the time
of the regular Python implementation:


.. code-block:: bash

    $ time python2 mandelbrot.py
    real    29m16.779s
    user    29m12.519s
    sys     0m0.977s

    $ time pypy mandelbrot.py 
    real    16m21.750s
    user    16m18.200s
    sys     0m1.320s


And here the download link. I converted the file M.bmp, which had a size of 18MB
to PNG with a size of 1.7MB:

.. gallery::
   :small: 1

   .. image:: mandelbrot.png
      :alt: KDE 4.10 RC1
