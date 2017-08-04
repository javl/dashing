# dashing #

### About ###
Made during the [Hackers & Designers Summer Academy 2017](https://hackersanddesigners.nl/s/Summer_Academy_2017).

Amazon dash buttons are a dream for the modern consumer. Never run out of any product, buy more without any hassle.

This script combines the commercial

### Installing ###
Full instructions on installing MXNet can be found [here](http://mxnet.io/tutorials/embedded/wine_detector.html), but in short:

#### Virtualenv ####
Running the script in a virtual environment is optional, but it might be useful in keeping your machine organized:

    # Install virtualenv (using a virtual environment is optional)
    sudo apt-get install virtualenv

    # Create a virtual environment folder and load it
    virtuelenv env
    source env/bin/activate

#### MXNet ####
After installing MXNet you can download one of their models for testing

    # Use pip to install MXNet
    pip install mxnet

    # Download the model
    curl --header 'Host: data.mxnet.io' --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --header 'Referer: http://data.mxnet.io/models/imagenet/' --header 'Connection: keep-alive' 'http://data.mxnet.io/models/imagenet/inception-bn.tar.gz' -o 'inception-bn.tar.gz' -L

    # Unpack it
    tar -xvzf inception-bn.tar.gz

    # Rename the numbers in the filenames to 0000. I also had to
    # change the first '-' into a '_' (was not mentioned in above tutorial)
    mv Inception-BN-*.params Inception_BN-0000.params
    mv Inception-BN-symbol.json Inception_BN-symbol.json

For future reference: I also got a warning saying `label_shapes don't match names specified by label_names`. These were fixed using instructions from [here](https://stackoverflow.com/questions/44947104/mxnet-label-shapes-dont-match-names-specified-by-label-names) (already fixed for this repo).

    

#### Amazon API ####
I found the official Amazon API for Python hard to use, so instead I used `python-amazon-simple-product-api`

    pip install python-amazon-simple-product-api

Rename `amazon_credentials.example.py` to `amazon_credentials.example.py` and fill in your credentials.
Follow the instructions on the [Amazon Developer website](https://developer.amazon.com/) to get these.


#### Running ####
Change any variables in the code to fit your system: change `img_folder` to the right location and fill it with the images you want to use. I used [instagram-scraper](https://github.com/rarcega/instagram-scraper) to get a bunch of images from an Instagram account.

Now, making sure the Processing sketch is running on the receiving machine, run the sender script using:

    ./dashing.py
