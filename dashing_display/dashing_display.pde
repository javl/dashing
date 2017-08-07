// Receiving end of Dashing
// Quick and dirty prototype so completely inefficient

import hypermedia.net.*;

PImage img1;
PImage img2;
String keyword = "";
int counter = -1;
UDP udp;
boolean ready = false;
void setup() {
  // 6050 is the port number, this could be a different one, but needs to be > 1024
  udp = new UDP(this, 6001);
  udp.listen(true);
  fullScreen();
  noCursor();
}
void receive(byte[] data, String ip, int port) {
  String msg = new String(data);
  String[] list = split(msg, ',');
  if (list.length == 5) {
    if (int(list[1]) != counter) {
      println(int(list[1]) +" is not " + counter);
      counter = int(list[1]);
      println(msg);
      if (list[0].equals("dash")) {
        if (list[2].equals("original")) {
          img1 = null;
          img1 = loadImage(list[3]);
          ready = true;
        } else if (list[2].equals("found")) {
          fill(0, 255, 255);
          img2 = null;
          img2 = loadImage(list[3]); 
          ready = true;
        } else if (list[2].equals("clear")) {
          img1 = loadImage("/home/pi/jasper/img/white.jpg");
          img2 = loadImage("/home/pi/jasper/img/white.jpg");
          //img1 = loadImage("/home/javl/tmp/mxnet/img/white.jpg");
          //img2 = loadImage("/home/javl/tmp/mxnet/img/white.jpg");
          ready = false;
          keyword = "";
        } else if (list[2].equals("keyword")) {
          keyword = list[3];
        }
      }
    }
  }
}

void draw() {
  background(255);
  if (ready) {
    if (img1 != null) {
      try {
        if (img1.width > img1.height) {
          img1.resize(width/2, 0);
        } else {
          img1.resize(0, height);
        }
      } 
      catch (Exception e) {
      }

      fill(255);
      try {
        image(img1, 0, 0);
      } 
      catch (Exception e) {
      }
    }
    if (img2 != null) {
      try {
        if (img2.width > img2.height) {
          img2.resize(width/2, 0);
        } else {
          img2.resize(0, height);
        }
      } 
      catch (Exception e) {
      }
      fill(255);
      try {
        image(img2, width/2, 0);
      } 
      catch (Exception e) {
      }
    }
  } else {
    fill(0);
    textSize(32);
    textAlign(CENTER, CENTER);
    text("Waiting for Dash button", width/2, height/2);
  }
  if (!keyword.equals("")) {
    textSize(64);
    textAlign(CENTER, CENTER);
    fill(0);
    text(keyword, width/2, 50);
    fill(255);
    text(keyword, width/2-2, 50-2);
  }
}