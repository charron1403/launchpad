import RPi.GPIO as GPIO
import time
import pygame

playing = False
recording = False
x1y1 = True
x1y2 = True
x1y3 = True
x2y1 = True
x2y2 = True
x2y3 = True
x3y1 = True
x3y2 = True
x3y3 = True

delay = 0.1
active_bank = 0
sound_banks = [[0]*9 for i in range(3)]
sequences = [[0]*9 for seq in range(3)]

pygame.mixer.init()

# Créez des objets pygame.mixer.Sound pour chaque son
kick_sound = pygame.mixer.Sound("sounds/banks/0/0.mp3")
hihat_sound = pygame.mixer.Sound("sounds/banks/1/0.mp3")
snare_sound = pygame.mixer.Sound("sounds/banks/2/0.mp3")

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Record
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Play/Stop
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Banque1
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Banque2
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Banque3
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x1y1
    GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #x1y2
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #x1y3
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x2y1
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x2y2
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x2y3
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x3y1
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x3y2
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #x3y3

    GPIO.add_event_detect(4, GPIO.RISING, callback=switch_recording, bouncetime=200)
    GPIO.add_event_detect(17, GPIO.RISING, callback=play_stop, bouncetime=200)
    GPIO.add_event_detect(27, GPIO.RISING, callback=switch_bank, bouncetime=200)
    GPIO.add_event_detect(22, GPIO.RISING, callback=switch_bank, bouncetime=200)
    GPIO.add_event_detect(10, GPIO.RISING, callback=switch_bank, bouncetime=200)
    GPIO.add_event_detect(11, GPIO.RISING, callback=x1y1_event, bouncetime=200)
    GPIO.add_event_detect(0, GPIO.RISING, callback=x1y2_event, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.RISING, callback=x1y3_event, bouncetime=200)
    GPIO.add_event_detect(13, GPIO.RISING, callback=x2y1_event, bouncetime=200)
    GPIO.add_event_detect(19, GPIO.RISING, callback=x2y2_event, bouncetime=200)
    GPIO.add_event_detect(26, GPIO.RISING, callback=x2y3_event, bouncetime=200)
    GPIO.add_event_detect(16, GPIO.RISING, callback=x3y1_event, bouncetime=200)
    GPIO.add_event_detect(20, GPIO.RISING, callback=x3y2_event, bouncetime=200)
    GPIO.add_event_detect(21, GPIO.RISING, callback=x3y3_event, bouncetime=200)

    for b in range(3):
        for s in range(9):
            path = "~/PycharmProjects/launchpad/sounds/banks/"+str(b)+"/"+str(s)+".mp3"
            sound_banks[b][s] = pygame.mixer.Sound(path)

def play_sound(sound):
    sound.play()

def button_delay(button):
    global delay
    button = False
    time.sleep(delay)
    button = True


def play_stop(pin):
    global playing
    playing = not playing
    print(playing)


def switch_recording(pin):
    global recording
    recording = not recording


def switch_bank(pin):
    global active_bank
    if pin == 27:
        active_bank = 0
    elif pin == 22:
        active_bank = 1
    elif pin == 10:
        active_bank = 2


def x1y1_event(pin):
    global active_bank, x1y1
    if x1y1:
        button_delay(x1y1)
        play_sound(sound_banks[active_bank][0])

def x1y2_event(pin):
    global active_bank, x1y2
    if x1y2:
        button_delay(x1y2)
        play_sound(sound_banks[active_bank][1])

def x1y3_event(pin):
    global active_bank, x1y3
    if x1y3:
        button_delay(x1y3)
        play_sound(sound_banks[active_bank][2])

def x2y1_event(pin):
    global active_bank, x2y1
    if x2y1:
        button_delay(x2y1)
        play_sound(sound_banks[active_bank][3])

def x2y2_event(pin):
    global active_bank, x2y2
    if x2y2:
        button_delay(x2y2)
        play_sound(sound_banks[active_bank][4])

def x2y3_event(pin):
    global active_bank, x2y3
    if x2y3:
        button_delay(x2y3)
        play_sound(sound_banks[active_bank][5])

def x3y1_event(pin):
    global active_bank, x3y1
    if x3y1:
        button_delay(x3y1)
        play_sound(sound_banks[active_bank][6])

def x3y2_event(pin):
    global active_bank, x3y2
    if x3y2:
        button_delay(x3y2)
        play_sound(sound_banks[active_bank][7])

def x3y3_event(pin):
    global active_bank, x3y3
    if x3y3:
        button_delay(x3y3)
        play_sound(sound_banks[active_bank][8])


initialize()


try:
    while True:
        pass
except:
    GPIO.cleanup()
