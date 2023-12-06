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
bpm = 120
bpm_ms = 0
active_bank = 0
sequence_position = 0
sound_banks = [[0 for _ in range(9)] for _ in range(3)]
sequences = [[[0 for _ in range(16)] for _ in range(9)] for seq in range(3)]

pygame.init()
pygame.mixer.init()

# Créez des objets pygame.mixer.Sound pour chaque son
kick_sound = pygame.mixer.Sound("sounds/banks/0/0.mp3")
hihat_sound = pygame.mixer.Sound("sounds/banks/1/0.mp3")
snare_sound = pygame.mixer.Sound("sounds/banks/2/0.mp3")

class Button:
    def __init__(self, x, y, size, button_id, text=None, sound=None):
        self.x = x
        self.y = y
        self.size = size
        self.button_id = button_id
        self.text = text
        #self.sound = pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')
        self.sound = sound
        self.clicked = False

    def draw(self, surface):
        color = (255, 0, 0) if self.clicked \
            else (255, 255, 255)

        pygame.draw.rect(surface, color, (self.x, self.y, self.size, self.size))

        if self.text:
            font = pygame.font.Font(None, 18)
            text = font.render(self.text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            surface.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        return (self.x < mouse_pos[0] < self.x + self.size and
                self.y < mouse_pos[1] < self.y + self.size)

    def play_sound(self):
        self.sound.play()
class Track:
    def __init__(self, x, y, width, height, track_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.track_id = track_id
        self.buttons_pressed = []

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height))

        button_height = self.height // 9

        for i in range(9):
            button_x = self.x + 50  # Ajustement de la position en x
            button_y = self.y + i * button_height
            pygame.draw.rect(surface, (255, 0, 0), (button_x, button_y, self.width, button_height), 2)

            # Draw pressed buttons
            for button_id in self.buttons_pressed:
                if button_id == i:
                    pygame.draw.rect(surface, (0, 0, 0), (button_x, button_y, self.width, button_height))
class UIBoard:
    global button
    window = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    run = True

    buttons = [
        Button(100, 700, 80, 1, "Track 1", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(200, 700, 80, 2, "Track 2", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(300, 700, 80, 3, "Track 3", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(500, 700, 50, 4, "Stop", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(600, 700, 50, 5, "Play/Record", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(800, 650, 50, 6, "Select 1", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(900, 650, 50, 7, "Select 2", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(1000, 650, 50, 8, "Select 3", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(800, 700, 50, 9, "Select 4", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(900, 700, 50, 10, "Select 5", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(1000, 700, 50, 11, "Select 6", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(800, 750, 50, 12, "Select 7", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(900, 750, 50, 13, "Select 8", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
        Button(1000, 750, 50, 14, "Select 9", pygame.mixer.Sound(f'mixkit-fast-small-sweep-transition-166.wav')),
    ]

    tracks = [
        Track(100, 100, 900, 150, 1),
        Track(100, 300, 900, 150, 2),
        Track(100, 500, 900, 150, 3),
    ]

    current_track = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     for button in buttons:
            #         if button.is_clicked(mouse_pos):
            #             button.clicked = not button.clicked
            #             if button.clicked:
            #                 current_track = button.button_id
            #                 button.play_sound()

                # for track in tracks:
                    # track_rect = pygame.Rect(track.x, track.y, track.width, track.height)
                    # if track_rect.collidepoint(mouse_pos):
                        # current_track = track
                        # current_track.sound.play()
                        # current_track.buttons_pressed.append(button.button_id)

        pygame.display.update()
        clock.tick(40)
        window.fill((225, 225, 225))

        # Draw tracks
        for track in tracks:
            track.draw(window)

        # Draw buttons
        for button in buttons:
            button.draw(window)

def initialize():
    global sound_banks, bpm, bpm_ms

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
            path = "sounds/banks/"+str(b)+"/"+str(s)+".mp3"
            sound_banks[b][s] = pygame.mixer.Sound(path)

    bpm_ms = bpm_bar_to_ms(bpm)

def bpm_bar_to_ms(bpm):
    return 60000 / (bpm * 4)

def play_sound(sound):
    sound.play()

def record_sound(sound_index):
    global recording, sequences, active_bank, sequence_position
    if recording:
        sequences[active_bank][sound_index][sequence_position] = 1

def play_sequence_bar():
    global sequence_position
    for bank_index, bank in enumerate(sound_banks):
        for sound_index, sound in enumerate(bank):
            if (sound[sequence_position] == 1):
                play_sound(sound_banks[bank_index][sound_index])
    if sequence_position < 15:
        sequence_position += 1
    else:
        sequence_position = 0

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
    global recording, playing
    recording = not recording
    if recording & playing == False:
        playing = True


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
        record_sound(0)
        play_sound(sound_banks[active_bank][0])

def x1y2_event(pin):
    global active_bank, x1y2
    if x1y2:
        button_delay(x1y2)
        record_sound(1)
        play_sound(sound_banks[active_bank][1])

def x1y3_event(pin):
    global active_bank, x1y3
    if x1y3:
        button_delay(x1y3)
        record_sound(2)
        play_sound(sound_banks[active_bank][2])

def x2y1_event(pin):
    global active_bank, x2y1
    if x2y1:
        button_delay(x2y1)
        record_sound(3)
        play_sound(sound_banks[active_bank][3])

def x2y2_event(pin):
    global active_bank, x2y2
    if x2y2:
        button_delay(x2y2)
        record_sound(4)
        play_sound(sound_banks[active_bank][4])

def x2y3_event(pin):
    global active_bank, x2y3
    if x2y3:
        button_delay(x2y3)
        record_sound(5)
        play_sound(sound_banks[active_bank][5])

def x3y1_event(pin):
    global active_bank, x3y1
    if x3y1:
        button_delay(x3y1)
        record_sound(6)
        play_sound(sound_banks[active_bank][6])

def x3y2_event(pin):
    global active_bank, x3y2
    if x3y2:
        button_delay(x3y2)
        record_sound(7)
        play_sound(sound_banks[active_bank][7])

def x3y3_event(pin):
    global active_bank, x3y3
    if x3y3:
        button_delay(x3y3)
        record_sound(8)
        play_sound(sound_banks[active_bank][8])


initialize()


try:
    while True:
        if playing:
            play_sequence_bar()
            time.sleep(bpm_ms)
except:
    GPIO.cleanup()
