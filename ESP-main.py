import machine
import time
import os
from machine import Pin, SoftI2C, ADC, PWM, UART
from ssd1306 import SSD1306_I2C


ANALOG_SENSOR_PIN = 35
DIGITAL_SENSOR_PIN = 25
BUZZER_PIN = 26
BUTTON_PIN = 27
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

TIME_UNTIL_WARMUP = 5

analog_sensor = ADC(Pin(ANALOG_SENSOR_PIN))
analog_sensor.atten(ADC.ATTN_11DB)
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(2000)
buzzer.duty(0)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

i2c = SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
display = SSD1306_I2C(128, 64, i2c, addr=0x3c)

UART_NUM = 0
BAUD_RATE = 115200

uart = UART(UART_NUM, baudrate=BAUD_RATE)


def setup():
    display.fill(0)
    display.show()
    
def center_text(text, y, font_width=8):
    screen_width = 128
    text_width = len(text) * font_width
    x = (screen_width - text_width) // 2
    display.text(text, x, y)

def print_title():
    display.fill(0)
    display.text("Breath Analyzer", 4, 0)
    display.show()

def print_warming():
    display.fill(0)
    print_title()
    center_text("Warming up...", 30)
    display.show()

def print_loading_bar(elapsed_time, total_time):
    mapped_time = int((elapsed_time / total_time) * 110)
    display.rect(10, 50, 110, 10, 1)
    display.fill_rect(10, 50, mapped_time, 10, 1)

def print_ready():
    display.fill(0)
    print_title()
    center_text("Ready for Test", 30)
    display.show()

def send_uart(value):
    uart.write(str(value) + '\n')

def analog_read(pin):
    adc = ADC(Pin(pin))
    val = adc.read()
    return val

def read_alcohol():
    val1 = analog_read(ANALOG_SENSOR_PIN)
    time.sleep_ms(10)
    val2 = analog_read(ANALOG_SENSOR_PIN)
    time.sleep_ms(10)
    val3 = analog_read(ANALOG_SENSOR_PIN)
    val = (val1 + val2 + val3) // 3
    return val

def beep(duration):
    buzzer.duty(52)
    time.sleep(duration)
    buzzer.duty(0)

def print_test_begun():
    display.fill(0)
    print_title()
    center_text("Test has begun", 30)
    display.show()
    time.sleep(2)

def print_test_ended():
    display.fill(0)
    print_title()
    center_text("Test has ended", 30)
    display.show()


def main():
    setup()
    start_time = time.ticks_ms()
    warming_up = True
    test_active = False
    start_test_time = 0

    while True:
        time.sleep(0.1)
        elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)

        if warming_up:
            if elapsed_time <= TIME_UNTIL_WARMUP * 1000:
                display.fill(0)
                print_warming()
                print_loading_bar(elapsed_time, TIME_UNTIL_WARMUP * 1000)
                display.show()
            else:
                warming_up = False
                print_ready()
                print("Sensor warmed up.")
        
        elif not warming_up and button.value() == 0 and not test_active:
            test_active = True
            start_test_time = time.ticks_ms()
            time.sleep(0.1)

        if test_active:
            start_test_time = time.ticks_ms()
            for i in range(10, 0, -1):
                current_time = time.ticks_ms()
                val = read_alcohol()
                send_uart(val)
                print(val)
                display.fill(0)
                print_title()
                center_text("Blow steady", 25)
                center_text(f"for {i} seconds", 40)
                display.show()
                while time.ticks_diff(time.ticks_ms(), current_time) < 1000:
                    pass

            beep(0.5)
            print_test_ended()
            time.sleep(2)
            print_ready()
            test_active = False

        time.sleep(0.1)

if __name__ == "__main__":
    main()