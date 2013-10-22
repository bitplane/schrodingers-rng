Schrödinger's RNG
=================

So you don't trust your operating system's random number generator and you have
blisters on your hands from flipping coins to create bitcoin private keys. 
All your dice have worn out at the corners and every deck of cards you own is 
severely dog-eared.

Whether you need a quantum-tinfoil hat to protect you from malignant hidden 
non-local variables, or you want a slow but steady stream of truly random bits 
generated on your Raspberry Pi then you may and may not need a hardware random 
number generator.

Disclaimer
----------

This is a toy project and should not be taken seriously. I am not a cryptographer 
and although I have tried to make the minimum number of assumptions, a dice
rolling or coin flipping machine would have less complexities and potential attack 
vectors.

While feeding this into /dev/random is considered safe, you should exercise caution
if you choose to use the raw values themselves. From what I understand the safest 
way to use this tool is to consider each row a single bit of information, select a
column and compare its direction from the observed average to decide whether it 
represents a 0 or a 1. 

 * Don't mess with the device while it is recording, it may skew the output.
 * Consider each row of output to only have one bit of entropy. A value on the same
   row is part of the same event and may share information; a frame number declares 
   that the X and Y values are not off the screen; the angle of the radiation 
   source may mean that the brightness of an event may leak information about its 
   position, or a given X position may make a Y position more likely. 
 * Don't generate random numbers on a machine that has been or will be connected
   to the Internet and do not keep them for longer than is necessary.

Ingredients
-----------

You will need...

1. 1 machine running Linux.
2. The cheapest Linux-compatible webcam money can buy.
3. 1 ionization smoke detector containing americium-241.
4. Any screwdriver except the sexist pink one that you're not allowed to use.
5. A glue gun.
6. Tin / aluminium foil.
7. Insulation / gaffer / BDSM tape.

Instructions
------------

Unscrew the webcam and remove the lens from the sensor. Open the smoke detector,
remove the housing around the radiation source and then the source itself. This
is a thin sheet of film with americium-241 embedded in it and is facing at the
ion detector. **Do not inhale, burn or otherwise let this get into your body, 
it's not good for you**. Affix the radiation source to the webcam sensor and 
glue it in place. Cover the rest of the electronics in glue to prevent shorts and 
then wrap the thing in several layers of foil (probably not necessary but I'm 
paranoid) and then tape it up. Easy-peasy.

Assuming video4linux works with your webcam it should show up as /dev/video0
or /dev/video1 if you already have a webcam. Install uvcview 
(`apt-get install guvcview`) or some other webcam viewer and you should observe a 
black screen with a pixel flashing in a random location every 10-20 seconds.

Run `./configure` to check for dependencies and create the FIFO queue (needed 
because "streamer" actually lacks streaming output support). You should only need
to `apt-get install streamer python`, but `pypy` or `jython` are recommended for 
speed/power use (the fastest available interpreter will be selected by `./configure`)

Finally, run `./capture` to dump the data out to CSV. This can be used to feed
into your system's random pool, just `./capture > /dev/random`. 

to-do
-----

Todo list and bugs are being held on the project's Github issue tracker:

    https://github.com/bitplane/schrodingers-rng/issues

License
-------
Copyright (c) 2013 Gaz Davidson <gaz@bitplane.net>

Licensed under the [WTFPL](http://en.wikipedia.org/wiki/WTFPL) with one
additional clause:

   1. Don't blame me.

