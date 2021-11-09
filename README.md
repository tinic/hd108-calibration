# hd108-calibration

The batch of HD108-5050 LEDs I have does not have a linear response on green and blue. This is fairly visible when fading to black as they shift towards green and blue. With a RaspberryPI and a TSL2591 board we can measure the response curve and determine an approximate correction. The result looks as follows:

![](hd108response.png?raw=true "Title" | width=200)

