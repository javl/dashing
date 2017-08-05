# Dashing #

## About ##
Made during the [Hackers & Designers Summer Academy 2017](https://hackersanddesigners.nl/s/Summer_Academy_2017).

Amazon dash buttons are a dream for the modern consumer. Never run out of any product, buy more without any hassle. But what if you don't only want to buy the products you can get a button for, but want to be able to buy everything your favourite Instagram celebrities promote?

Dashing takes an image from Instagram and, using computer vision, figures out what is shown in the picture*. This results in a keyword which it then uses to find a matching product on Amazon, so you can have what they're having, all with the push of a button!

* your milage may vary

## Examples ##
Click images to visit their original page.

### Rihanna ###

[![Rihanna example source](https://raw.githubusercontent.com/javl/dashing/master/img/results/rihanna_source_descr.png?raw=true)](https://www.instagram.com/p/BXBVgyplxTB/?taken-by=badgalriri)

#### Cressi SUPERNOVA DRY, Adult Diving Dry Snorkel - Cressi: Quality Since 1946  ####

[![Rihanna example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/rihanna_result.png?raw=true)](https://www.amazon.com/Cressi-Supernova-Dry-black-red/dp/B00AQRBO16/ref=sr_1_1?ie=UTF8&qid=1501922519&sr=8-1&keywords=B00AQRBO16)

### Kylie Jenner ###
[![Kyliejenner example source](https://github.com/javl/dashing/blob/master/img/results/kyliejenner_source_descr.png?raw=true)](https://www.instagram.com/p/BW8Llwjl6ml/?taken-by=kyliejenner)

### Nestlé® Pure Life® Bottled Purified Water, 16.9 oz. Bottles, 24/Case  ###
[![Kyliejenner example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/kyliejenner_result.png?raw=true)](https://www.amazon.com/Nestl%C3%A9-Life-Bottled-Purified-Bottles/dp/B00LLKWVL4/ref=sr_1_1?ie=UTF8&qid=1501922824&sr=8-1&keywords=B00LLKWVL4)

### Rita Ora ###
[![Rita Ora example source](https://raw.githubusercontent.com/javl/dashing/master/img/results/ritaora_source_descr.png?raw=true)](https://www.instagram.com/p/BXNxVqMnb1l/?taken-by=ritaora)

###  Fiesta Fun Party Maracas (2/Pkg) ###
[![Rita Ora example result](https://raw.githubusercontent.com/javl/dashing/master/img/results/ritaora_result.png?raw=true)](https://www.amazon.com/Fiesta-Fun-Party-Maracas-Pkg/dp/B000R4OHCG/ref=sr_1_1?ie=UTF8&qid=1501923376&sr=8-1&keywords=B000R4OHCG)

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
Change any variables in the code to fit your system: change `img_folder` to the right location and fill it with the images you want to use. I used [instagram-scraper](https://github.com/rarcega/instagram-scraper) to get a bunch of images from an Instagram account.

Now, making sure the Processing sketch is running on the receiving machine, run the sender script using:

    ./dashing.py
