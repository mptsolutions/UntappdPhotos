# Untappd Photos
### This is a project for building a small screen that displays user photos from [Untappd](https://untappd.com/). It uses a [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) and the <i>pre-2021</i> version of the [HyperPixel 4 Square](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075).

## Contents
- [Necessary Hardware](#necessary-hardware)
- [Setup](#setup)
- [Very Helpful Example Code](#very-helpful-example-code)

## [Necessary Hardware](#necessary-hardware)
* [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
* [HyperPixel 4 Square](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075)
  * <i>Important Note</i>: There are two versions of the HyperPixel 4 <i>Square</i>. The version that was manufactured before 2021 is apparently different in some way that is very important but impossible to tell by looking at it. All the recent instructions for working with the screen assume you have the newer version, but if you have the older one none of those instruction will actually work. I do not have the newer one, so <u>this project has been set up using the pre-2021 hardware</u>. That is why I am using RaspberryPi OS <i>Bullseye</i>. I did not want to use Olde Worlde software, but apparently I bought [Olde Worlde hardware](https://www.pishop.ca/product/hyperpixel-4-0-square-hi-res-display-for-raspberry-pi-non-touch/?searchid=0&search_query=hyperpixel+square).
* [3D Printed stand](https://cults3d.com/en/3d-model/gadget/enclosure-base-for-hyperpixel-4-0-square-non-touch-and-raspberry-pi-zero)

## [Setup](#setup)
### Steps
- [Hardware](#hardware)
- [RaspberryPi OS](#raspberrypi-os)
- [HyperPixel Driver](#hyperpixel-driver)
- [Python Project](#python-project)

### [Hardware](#hardware)
HyperPixels are hyper-sensitive. If yours wasn't broken when you took it out of the box, it will probably be broken soon.  
Try to connect the Raspberry Pi to the screen as carefully as possible. You have to avoid pushing on the screen itself. No, that isn't a joke. Apparently you are supposed to push using magic.

### [RaspberryPi OS](#raspberrypi-os)
Setup a new SD card with RaspberryPi OS Bullseye. When I created this, Bullseye was the "legacy" option in the Raspberry Pi Imager so it was easy, but if you live in the future it might take more effort to track down.

Setup the Raspberry Pi like normal and once the OS running, do the usual updates:

```bash
$ sudo apt update -y
$ sudo apt upgrade -y
```

### [HyperPixel Driver](#hyperpixel-driver)
This is where life gets hard. Don't waste your time with the easy instructions on [the Pimoroni website](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075) - those are for the chosen ones with the newer version of the screen.  

Instead you are going to want to run the below command from somewhere convenient like the ```home``` directory:

```bash
$ curl -sSL get.pimoroni.com/hyperpixel4-legacy | bash
```

This is going to walk you through some confusing nonsense that starts with confirming that you really, truely, sincerely, do want that screen you paid for to work:

```txt
This script will install everything needed to use
HyperPixel4

Always be careful when running scripts and commands copied
from the internet. Ensure they are from a trusted source.

This script should -- only be run on a Raspberry Pi with RPi OS --
other systems and SBCs are not supported and may explode!

If you want to see what this script does before running it,
you should run: 'curl https://get.pimoroni.com/hyperpixel4'

---------------------------------------------------------
PSA: The install process has changed!
Pi 4 and Pi 3B+ users should read this before continuing:
https://github.com/pimoroni/hyperpixel4/issues/177
---------------------------------------------------------

Do you wish to continue? [y/N]
```
Next you need to choose one of the below options. Even though you are not using the "Pi 4 / Pi 400", you should enter "```1```" anyway. If you got this far and only just clued-in that this project uses the square screen, stop now - none of this nonsense isn't need for the rectangle version.

```
Pick your HyperPixel 4 and Raspberry Pi combo below:

Pi 4 / Pi 400
 0 : Rectangular
 1 : Weirdly Square

Pi 3B+ or older
 2 : Rectangular
 3 : Weirdly Square

Press Ctrl+C to cancel.

If you have problems with your install
let us know: https://github.com/pimoroni/hyperpixel4

Enter an option [0-4]:
```

The next question is a trick. It doesn't matter when you <i>purchased</i> your screen - I bought mine in 2025. Enter "```1```" again to select the Olde Worlde version.
```
When did you purchase your HyperPixel Square?
 0: 2021 or later
 1: 2020 or earlier
Press Ctrl+C to cancel.

If you're unsure, don't worry, you can change your /boot/config.txt later.

Enter an option [0-1]:
```

And finally, confirm that you were paying attention the whole time.
```txt
Installing Weirdly Square for Pi 4 / Pi 400
for HP manufactured 2020 or earlier.
Is this correct? [y/N]
```

The script will run, install some files, and update some configs. If it outputs any error messages then all bets are off and you are on your own from here. 

On the other hand, if it pretends like all is well, continue on...

The script lies - it doesn't update everything it needs to. It <i>could</i> if they wanted it to, but it just doesn't. If you were to reboot now, you would experience the delight of seeing the Raspberry Pi OS splash screen pop up in all its glory - only to be replaced by a blank screen that never goes away.

To fix this, you need to manually edit one more line in ```/boot/config.txt```. Open the file in ```nano```.

```bash
$ sudo nano /boot/config.txt
```

Then make sure that the ```dtoverlay``` line shown below is commented out. There might multiple lines that start with ```dtoverlay``` but you only want to mess with the one that actually looks like below.

```txt
# Enable DRM VC4 V3D driver
# dtoverlay=vc4-kms-v3d
```

Now you can reboot and your Raspberry Pi should start up normally with a nice tiny screen!

Maybe. At least it worked for me. Good luck.

#### Links I Found ~~Frustrating~~ Useful

I read all of this madness. Some of it was helpful and it's a good place to start if you you got this far and your screen still doesn't display.

* https://github.com/pimoroni/hyperpixel4
* https://github.com/pimoroni/hyperpixel4/issues/223
* https://github.com/pimoroni/hyperpixel4/issues/177
* https://github.com/pimoroni/hyperpixel4/issues/177#issuecomment-1786957639
* https://github.com/pimoroni/hyperpixel4/issues/177#issuecomment-1675723130
* https://github.com/pimoroni/hyperpixel4/tree/square
* https://forums.pimoroni.com/t/hyperpixel-4-0-square-touch-splash-screen-but-no-desktop/18491
* https://forums.pimoroni.com/t/hyperpixel-4-square-and-pi-zero-2-issue/18188/6
* https://github.com/pimoroni/hyperpixel4/issues/155

### [Python Project](#python-project)

Find a convenient place to clone this repository, like in the ```home``` directory.

```bash
$ cd ~/
$ git clone https://github.com/mptsolutions/UntappdPhotos.git
```

If you are happy to have your photos live in ```./media/photos/```, and for them to rotate every 10 seconds, then you probably don't need to adjust anything. But you can verify all the configurable settings in ```configs.py```.
```bash
$ nano config.py
```



## [Very Helpful Example Code](#very-helpful-example-code)
* [Lupin3000/HyperPixel-4.0-Square](https://github.com/Lupin3000/HyperPixel-4.0-Square)

