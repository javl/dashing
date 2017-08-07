# Dashing #

1. [About](#about)
2. [Examples](#examples)
    1. [Rihanna](#rihanna)
    2. [Kylie Jenner](#kylie-jenner)
    3. [Rita Ora](#rita-ora)
3. [Dashing button](#dashing-button)
4. [Installing](#installing)
5. [Running](#running)

## About ##
Made during the [Hackers & Designers Summer Academy 2017](https://hackersanddesigners.nl/s/Summer_Academy_2017).

Amazon Dash buttons are a dream for the modern consumer. Never run out of any product, buy more without any hassle. But what if you don't only want to buy the products you can get a Dash button for, but want to be able to buy everything your favourite Instagram celebrities promote?

An unbranded, home-made Dash button triggers a script that takes an image from Instagram and, using computer vision, figures out what is shown in the picture*. This results in a keyword which it then uses to find a matching product on Amazon, so you can have what they're having, all with the push of a button!

\* your milage may vary

___

## Examples ##
Click the images to visit the original Instagram or Amazon pages.

### Rihanna ###

[![Rihanna example source](https://raw.githubusercontent.com/javl/dashing/master/img/results/rihanna_source_descr.png?raw=true)](https://www.instagram.com/p/BXBVgyplxTB/?taken-by=badgalriri)

#### Cressi SUPERNOVA DRY, Adult Diving Dry Snorkel - Cressi: Quality Since 1946  ####

[![Rihanna example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/rihanna_result.png?raw=true)](https://www.amazon.com/Cressi-Supernova-Dry-black-red/dp/B00AQRBO16/ref=sr_1_1?ie=UTF8&qid=1501922519&sr=8-1&keywords=B00AQRBO16)

___

### Kylie Jenner ###
[![Kyliejenner example source](https://github.com/javl/dashing/blob/master/img/results/kyliejenner_source_descr.png?raw=true)](https://www.instagram.com/p/BW8Llwjl6ml/?taken-by=kyliejenner)

### Nestlé® Pure Life® Bottled Purified Water, 16.9 oz. Bottles, 24/Case  ###
[![Kyliejenner example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/kyliejenner_result.png?raw=true)](https://www.amazon.com/Nestl%C3%A9-Life-Bottled-Purified-Bottles/dp/B00LLKWVL4/ref=sr_1_1?ie=UTF8&qid=1501922824&sr=8-1&keywords=B00LLKWVL4)

___

### Rita Ora ###
[![Rita Ora example source](https://raw.githubusercontent.com/javl/dashing/master/img/results/ritaora_source_descr.png?raw=true)](https://www.instagram.com/p/BXNxVqMnb1l/?taken-by=ritaora)

###  Fiesta Fun Party Maracas (2/Pkg) ###
[![Rita Ora example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/ritaora_result.png?raw=true)](https://www.amazon.com/Fiesta-Fun-Party-Maracas-Pkg/dp/B000R4OHCG/ref=sr_1_1?ie=UTF8&qid=1501923376&sr=8-1&keywords=B000R4OHCG)

___

## Dashing Button ##
The Dashing button was made in [OpenScad](http://www.openscad.org/) which is a free and open CAD tool. You can find both the source file and the .stl printable files in [the repo](https://github.com/javl/dashing/tree/master/dash_3d_model). The bottom part of the button has space for a regular breadboard-size button with 9mm tall actuator. The other two parts snap together to create a pressable button.

There are many ways to connect a button to your PC; I used an [I-PAC](https://www.ultimarc.com/ipac1.html) to emulate the return key of a keyboard. 

[![Dashing button](https://github.com/javl/dashing/blob/master/img/dashing_button.jpeg?raw=true)](https://github.com/javl/dashing/blob/master/img/dashing_button.jpeg?raw=true)
[![Dashing button inside](https://github.com/javl/dashing/blob/master/img/dashing_button_inside.jpeg?raw=true)](https://github.com/javl/dashing/blob/master/img/dashing_button_inside.jpeg?raw=true)
[![Dashing button render](https://github.com/javl/dashing/blob/master/img/dashing_button_render.png?raw=true)](https://github.com/javl/dashing/blob/master/img/dashing_button_render.png?raw=true)


## Installing ##

### pip and virtualenv ###
Commands in this readme use pip to install the necessary python modules.  
Running the script in a virtual environment is optional, but it might be useful in keeping your machine organised:

    # Install virtualenv (using a virtual environment is optional)
    sudo apt-get install virtualenv

    # Create a virtual environment folder and load it
    virtuelenv env
    source env/bin/activate

### MXNet ###
Full instructions on installing MXNet can be found [here](http://mxnet.io/tutorials/embedded/wine_detector.html), but the summarised steps below should work. First, install the opencv and mxnet python modules

    pip install opencv-python mxnet

After installing MXNet you'll need to download a model to use.

    # Download the model
    curl --header 'Host: data.mxnet.io' --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header 'Referer: http://data.mxnet.io/models/imagenet/' --header 'Connection: keep-alive' 'http://data.mxnet.io/models/imagenet/inception-bn.tar.gz' -o 'inception-bn.tar.gz' -L

    # Unpack it
    tar -xvzf inception-bn.tar.gz

    # Rename the numbers in the filenames to 0000. I also had to
    # change the first '-' into a '_' (was not mentioned in above tutorial)
    mv Inception-BN-*.params Inception_BN-0000.params
    mv Inception-BN-symbol.json Inception_BN-symbol.json

For future reference: I also got a warning saying `label_shapes don't match names specified by label_names`. These were fixed using instructions from [here](https://stackoverflow.com/questions/44947104/mxnet-label-shapes-dont-match-names-specified-by-label-names) (already fixed for this repo).

    

### Amazon API ###
I found the official Amazon API for Python hard to use, so instead I used `python-amazon-simple-product-api`

    pip install python-amazon-simple-product-api

Rename `amazon_credentials.example.py` to `amazon_credentials.example.py` and fill in your credentials.
Follow the instructions on the [Amazon Developer website](https://developer.amazon.com/) to get these.


### Running ###
`dashing.py` runs on your computer and handles all the logic. It sends UDP messages to the receiving (display) device which can then display them for you. With the current setup, the source images need to be present on both devices.
The display device runs the Processing script that will receive the UDP messages and then displays the right image and keyword.

Change any variables in the code to fit your system, change `img_folder` to the right location for instance, and fill it with the images you want to use. I used [instagram-scraper](https://github.com/rarcega/instagram-scraper) to quickly get a bunch of images from Instagram accounts.

Now, making sure the Processing sketch is running on the receiving machine, run the sender script using:

    ./dashing.py
