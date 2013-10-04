Schrödinger's RNG
=================

So you don't trust your operating system's random number generator, but you have
blisters on your hands from flipping coins to create bitcoin private keys. 
All your dice have worn out at the corners and every deck of cards you own is 
severely dog-eared.

Whether you need a quantum-tinfoil hat to protect you from malignant hidden local 
variables, or you want a slow but steady stream of truly random bits generated on 
your Raspberry Pi then you might want a Schrödinger's random number generator.

Disclaimer
----------

This is a toy project and should not be taken seriously. I am not a cryptographer 
and although I have tried to make the minimum number of assumptions, a dice
rolling or coin flipping machine would have less complexities and potential attack 
vectors.

Test with diehard before generating private keys with this method.

Ingredients
-----------

You will need...

1. 1 machine running Linux.
2. The cheapest Linux-compatible webcam money can buy.
3. 1 ionization smoke detector containing americium-241.
4. Any screwdriver except the sexist pink one that you're not allowed to use.
5. A glue gun
6. Tin / aluminium foil
7. Insulation / gaffer / BDSM tape

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

Run `./configure.sh` to check for dependencies and create the FIFO queue (needed 
because "streamer" actually lacks streaming output support). You should only need
to `apt-get install streamer python dieharder`.

Finally, run `./capture.sh` to dump the data out to CSV. This can be used to feed
into your system's random pool, just `./capture.sh > /dev/random`. 

to-do
-----

Need to take the CSV and convert it into a bit-stream, then test with dieharder.

License
-------
Copyright (c) 2013 Gaz Davidson <gaz@bitplane.net>,

Licensed under the [WTFPL](http://en.wikipedia.org/wiki/WTFPL) with one
additional clause:

   1. Don't blame me.

