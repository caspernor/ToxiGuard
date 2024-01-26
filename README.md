ToxiGuard

**Project Overview:**

This GitHub repository contains the code and scripts for a breath analyzer device that involves an ESP32 microcontroller, two Raspberry Pi 4's, one inside the device and another acting as a local server, and lastly a Ubuntu VM that collects, processes, and displays the sensor readings.

Components:
1. ESP32 (ESP-main.py):
The ESP32 is responsible for collecting sensor readings from an MQ3 sensor. It provides instructions on an OLED screen and transmits the data over UART to the Raspberry Pi 4.

2. Raspberry Pi 4 (Pi-main.py):
The Raspberry Pi 4 receives the sensor data from the ESP32, formats it, and saves it in a CSV file. Additionally, it captures an image using a Pi Camera Module 3. The CSV file and the image are then transferred via SFTP to a local server.

3. Local Server (local-server-script.sh):
The local server, hosted on another Raspberry Pi 4, executes the local-server-script.sh. This script backs up the received CSV and image files and forwards them through a Cisco router and multi-layer switch to a Ubuntu VM.

4. Ubuntu VM (index.html):
The Ubuntu VM runs an index.html file, which displays the CSV data and the image on a website. This website serves as a platform for doctors to access and analyze the test results.


**Usage:**

ESP32 Setup:

Connect the ESP32 to an MQ3 sensor, an ssd1306 OLED screen, a tactile push button and a buzzer.
Upload and run ESP-main.py on the ESP32.

Raspberry Pi 4 Setup:

Connect the ESP32 to the Raspberry Pi 4 via UART, our setup uses a USB cable.
Upload and run Pi-main.py on the Raspberry Pi 4.

Local Server Setup:

Execute local-server-script.sh on the local server.

Ubuntu VM Setup:

Run an HTTP server hosting index.html on the Ubuntu VM.


**File Descriptions:**

Pi-main.py: Main script for Raspberry Pi 4.

ESP-main.py: Main script for ESP32.

local-server-script.sh: Script for the local server.

index.html: HTML file for displaying results on the Ubuntu VM.
