Hue Alert
=========

## Introduction

My wife constantly has trouble getting my attention when I am either working or
playing video games due to me perpetually wearing noise cancelling headphones to focus
on work. Texts and calls may even fail since iOS often doesn't show texts when my Mac
computer is on Do Not Disturb. It has become a dyer issue.

She often gets angry with me even if I dont think its my fault because since I am the
husband, I'm obviously wrong. Obviously.

In order to combat this, I've created, **Hue Alert**. This will blink my desk lamp
different colors when my wife requires my attention. Either a nice white blink for
normal usage or if I did something wrong, red and quick blinks to know when shes mad
and I have to stop what I'm doing to take my bitter medicine.

## Usage

This is a web app which will sit on an active server listening on port 80.

The main page will display the two options: Standard Alert and Angry Alert

Clicking with the **Standard Alert** will:
    - Turn my lamp on for one second
    - Turn my lamp off for one second
    - Repeat three times

Clicking with the **Angry Alert** will:
    - Turn on my lamp for a half second
    - Turn it off for a half second
    - Repeat 5 times
    - Keep it turned on red, so I know that I screwed up

## Installation

1) `git clone https://github.com/srz2/hue_alert.git`
2) cd into hue_alert
3) Execute `python3 config.py`
4) Initially run the app `flask run`
5) Click the hue bridge button
6) Navigate to `http://<ip_address>/authorize`. Get the code given and copy it as the 
   `uuid` inside the config.ini file
7) Restart the app and now navigate to `http://<ip_address>/lights`. Locate the light
   number you want to control and copy it also into the config.ini file as the
   `light_id`
8) Restart the app one last time, and the app should be working now from the homepage


## Technologies

- Ubuntu Server
- Multithreaded Python with Flask
- HTML/CSS
- JSON
- Hue API

## Libraries

- [PyInquirer](https://github.com/CITGuru/PyInquirer)
- [Requests](https://github.com/psf/requests)