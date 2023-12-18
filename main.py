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

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Record
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Play/Stop
#GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Banque1
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Banque2
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Banque3
#GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x1y1
#GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x1y2
#GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x1y3
#GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x2y1
#GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x2y2
#GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x2y3
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x3y1
#GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x3y2
#GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # x3y3

#GPIO.add_event_detect(4, GPIO.RISING, callback=switch_recording, bouncetime=200)
#GPIO.add_event_detect(17, GPIO.RISING, callback=play_stop, bouncetime=200)
#GPIO.add_event_detect(27, GPIO.RISING, callback=switch_bank, bouncetime=200)
#GPIO.add_event_detect(22, GPIO.RISING, callback=switch_bank, bouncetime=200)
#GPIO.add_event_detect(10, GPIO.RISING, callback=switch_bank, bouncetime=200)
#GPIO.add_event_detect(11, GPIO.RISING, callback=x1y1_event, bouncetime=200)
#GPIO.add_event_detect(0, GPIO.RISING, callback=x1y2_event, bouncetime=200)
#GPIO.add_event_detect(6, GPIO.RISING, callback=x1y3_event, bouncetime=200)
#GPIO.add_event_detect(13, GPIO.RISING, callback=x2y1_event, bouncetime=200)
#GPIO.add_event_detect(19, GPIO.RISING, callback=x2y2_event, bouncetime=200)
#GPIO.add_event_detect(26, GPIO.RISING, callback=x2y3_event, bouncetime=200)
#GPIO.add_event_detect(16, GPIO.RISING, callback=x3y1_event, bouncetime=200)
#GPIO.add_event_detect(20, GPIO.RISING, callback=x3y2_event, bouncetime=200)
#GPIO.add_event_detect(21, GPIO.RISING, callback=x3y3_event, bouncetime=200)

class Button:
    def __init__(self, x, y, size, button_id, text=None):
        self.x = x
        self.y = y
        self.size = size
        self.button_id = button_id
        self.text = text
        self.sound = None
        self.clicked = False
        self.last_click_time = 0

        if text and text.startswith("Select"):
            band_index = 0
            if 0 <= button_id <= 8:
                sound_path = f'sounds/banks/{band_index}/{button_id}.mp3'
                print(f"Assigning sound to button {button_id}: {sound_path}")
                self.sound = pygame.mixer.Sound(sound_path)

    def draw(self, surface):
        color = (255, 0, 0) if self.clicked else (255, 255, 255)
        pygame.draw.rect(surface, color, (self.x, self.y, self.size, self.size))

        if self.text:
            font = pygame.font.Font(None, 18)
            text = font.render(self.text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            surface.blit(text, text_rect)

    def click(self):
        self.clicked = True
        self.last_click_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_click = current_time - self.last_click_time

        if self.clicked and time_since_click >= 800:
            self.clicked = False

    def is_clicked(self, mouse_pos):
        return (self.x < mouse_pos[0] < self.x + self.size and
                self.y < mouse_pos[1] < self.y + self.size)

    def play_sound(self):
        print(f"Playing sound for button {self.button_id}")
        self.sound.play()

class Track:
    def __init__(self, x, y, width, height, track_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.track_id = track_id
        self.buttons_pressed = []
        self.recording = False
        self.recorded_sequence = []
        self.next_action = "record"

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height))

        button_height = self.height // 9

        for i in range(9):
            button_x = self.x + 50
            button_y = self.y + i * button_height
            pygame.draw.rect(surface, (255, 0, 0), (button_x, button_y, self.width, button_height), 2)

            for button_id in self.buttons_pressed:
                if button_id == i:
                    pygame.draw.rect(surface, (0, 0, 0), (button_x, button_y, self.width, button_height))

        font = pygame.font.Font(None, 18)
        text = font.render("Recorded: " + " ".join(map(str, self.recorded_sequence)), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height + 20))
        surface.blit(text, text_rect)

    def handle_button_click(self, button_id):
        if self.recording:
            self.buttons_pressed.append(button_id)
            self.recorded_sequence.append(button_id)

    def toggle_recording(self):
        self.recording = not self.recording
        if not self.recording:
            print(f"Recording stopped. Sequence: {self.recorded_sequence}")
            self.next_action = "play"

    def add_recorded_sequence(self, sequence):
        self.recorded_sequence = sequence

    def play_recorded_sequence(self):
        for button_id in self.recorded_sequence:
            self.handle_button_click(button_id)
            pygame.time.wait(100)

class UIBoard:
    window = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    run = True

    buttons = [
        Button(800, 650, 50, 0, "Select 1"),
        Button(900, 650, 50, 1, "Select 2"),
        Button(1000, 650, 50, 2, "Select 3"),
        Button(800, 700, 50, 3, "Select 4"),
        Button(900, 700, 50, 4, "Select 5"),
        Button(1000, 700, 50, 5, "Select 6"),
        Button(800, 750, 50, 6, "Select 7"),
        Button(900, 750, 50, 7, "Select 8"),
        Button(900, 750, 50, 8, "Select 9"),
        Button(100, 700, 80, 10, "Track 1"),
        Button(200, 700, 80, 20, "Track 2"),
        Button(300, 700, 80, 30, "Track 3"),
        Button(500, 700, 50, 40, "Stop"),
        Button(600, 700, 50, 50, "Play/Record"),

        Button(1100, 650, 50, 150, "Bank 1"),
        Button(1100, 700, 50, 160, "Bank 2"),
        Button(1100, 750, 50, 170, "Bank 3"),
    ]

    tracks = [
        Track(100, 100, 900, 140, 15),
        Track(100, 300, 900, 140, 25),
        Track(100, 500, 900, 140, 35),
    ]

    def __init__(self):
        global active_bank
        active_bank = 0
        self.current_track = None

        for track in self.tracks:
            track.next_action = "record"

    def update_select_buttons(self):
        global active_bank
        for button in self.buttons:
            if button.text.startswith("Select"):
                button_id = button.button_id
                if 0 <= button_id <= 8:
                    sound_path = f'sounds/banks/{active_bank}/{button_id}.mp3'
                    print(f"Assigning sound to button {button_id}: {sound_path}")
                    button.sound = pygame.mixer.Sound(sound_path)

    def switch_bank(self, button):
        global active_bank
        if button.button_id == 150:
            active_bank = 0
        elif button.button_id == 160:
            active_bank = 1
        elif button.button_id == 170:
            active_bank = 2
        print(f"Switching to bank {active_bank}")
        self.update_select_buttons()

    def handle_play_record_button_click(self):
        if self.current_track is not None and isinstance(self.current_track, Track):
            if self.current_track.next_action == "record":
                self.current_track.toggle_recording()
                if not self.current_track.recording:
                    self.current_track.add_recorded_sequence(self.current_track.recorded_sequence)
                    self.current_track.recorded_sequence = []
                    self.current_track.next_action = "play"
            elif self.current_track.next_action == "play":
                self.current_track.play_recorded_sequence()

ui_board = UIBoard()

while ui_board.run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in ui_board.buttons:
                if button.is_clicked(mouse_pos):
                    button.click()
                    if button.button_id in [150, 160, 170]:
                        ui_board.switch_bank(button)
                    elif button.button_id in [10, 20, 30]:
                        ui_board.current_track = ui_board.tracks[button.button_id // 10 - 1]
                    elif button.button_id == 50:
                        ui_board.handle_play_record_button_click()
                    else:
                        button.play_sound()
                        if ui_board.current_track is not None and isinstance(ui_board.current_track, Track):
                            ui_board.current_track.handle_button_click(button.button_id)

    pygame.display.update()
    ui_board.clock.tick(40)
    ui_board.window.fill((225, 225, 225))

    for button in ui_board.buttons:
        button.update()

    for track in ui_board.tracks:
        track.draw(ui_board.window)

    for button in ui_board.buttons:
        button.draw(ui_board.window)

def initialize():
    global sound_banks, bpm, bpm_ms

    for b in range(3):
        for s in range(9):
            path = "sounds/banks/"+str(b)+"/"+str(s)+".mp3"
            sound_banks[b][s] = pygame.mixer.Sound(path)

    bpm_ms = bpm_bar_to_ms(bpm)

def bpm_bar_to_ms(bpm):
    return 60000 / (bpm * 4)

def play_sound(sound):
    print(f"Playing sound from bank {sound}")
    sound.play()

def record_sound(sound_index):
    global recording, sequences, active_bank, sequence_position
    if recording:
        sequences[active_bank][sound_index][sequence_position] = 1

def play_sequence_bar():
    global sequence_position, active_bank
    for bank_index, bank in enumerate(sound_banks[active_bank]):
        for sound_index, sound in enumerate(bank):
            if sound[sequence_position] == 1:
                play_sound(sound_banks[active_bank][sound_index])
    if sequence_position < 15:
        sequence_position += 1
    else:
        sequence_position = 0
    print(f"Playing sequence bar at position {sequence_position}")

def button_delay(button):
    global delay
    button = False
    time.sleep(delay)
    button = True

def play_stop(pin):
    global playing
    playing = not playing
    print(f"Playing status: {playing}")

def switch_recording(pin):
    global recording, playing
    recording = not recording
    if recording & playing == False:
        playing = True
    print(f"Recording status: {recording}, Playing status: {playing}")

import time
import pygame

playing = False
recording = False
active_track = None
bpm = 120
bpm_ms = 0
sound_banks = [[0 for _ in range(9)] for _ in range(3)]

pygame.init()
pygame.mixer.init()

class Button:
    def __init__(self, x, y, size, button_id, text=None):
        self.x = x
        self.y = y
        self.size = size
        self.button_id = button_id
        self.text = text
        self.sound = None
        self.clicked = False
        self.last_click_time = 0

        if text and text.startswith("Select"):
            band_index = 0
            if 0 <= button_id <= 8:
                sound_path = f'sounds/banks/{band_index}/{button_id}.mp3'
                print(f"Assigning sound to button {button_id}: {sound_path}")
                self.sound = pygame.mixer.Sound(sound_path)

    def draw(self, surface):
        color = (255, 0, 0) if self.clicked else (255, 255, 255)
        pygame.draw.rect(surface, color, (self.x, self.y, self.size, self.size))

        if self.text:
            font = pygame.font.Font(None, 18)
            text = font.render(self.text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            surface.blit(text, text_rect)

    def click(self):
        self.clicked = True
        self.last_click_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_click = current_time - self.last_click_time

        if self.clicked and time_since_click >= 800:
            self.clicked = False

    def is_clicked(self, mouse_pos):
        return (self.x < mouse_pos[0] < self.x + self.size and
                self.y < mouse_pos[1] < self.y + self.size)

    def play_sound(self):
        print(f"Playing sound for button {self.button_id}")
        self.sound.play()

class Track:
    def __init__(self, x, y, width, height, track_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.track_id = track_id
        self.buttons_pressed = []
        self.recording = False
        self.recorded_sequence = []

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height))

        button_height = self.height // 9

        for i in range(9):
            button_x = self.x + 50
            button_y = self.y + i * button_height
            pygame.draw.rect(surface, (255, 0, 0), (button_x, button_y, self.width, button_height), 2)

            for button_id in self.buttons_pressed:
                if button_id == i:
                    pygame.draw.rect(surface, (0, 0, 0), (button_x, button_y, self.width, button_height))

        font = pygame.font.Font(None, 18)
        text = font.render("Recorded: " + " ".join(map(str, self.recorded_sequence)), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height + 20))
        surface.blit(text, text_rect)

    def handle_button_click(self, button_id):
        if self.recording:
            self.buttons_pressed.append(button_id)
            self.recorded_sequence.append(button_id)

    def toggle_recording(self):
        self.recording = not self.recording
        if not self.recording:
            print(f"Recording stopped. Sequence: {self.recorded_sequence}")

    def add_recorded_sequence(self, sequence):
        self.recorded_sequence = sequence

    def play_recorded_sequence(self):
        for button_id in self.recorded_sequence:
            self.handle_button_click(button_id)
            pygame.time.wait(100)

class UIBoard:
    window = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    run = True

    buttons = [
        Button(800, 650, 50, 0, "Select 1"),
        Button(900, 650, 50, 1, "Select 2"),
        Button(1000, 650, 50, 2, "Select 3"),
        Button(800, 700, 50, 3, "Select 4"),
        Button(900, 700, 50, 4, "Select 5"),
        Button(1000, 700, 50, 5, "Select 6"),
        Button(800, 750, 50, 6, "Select 7"),
        Button(900, 750, 50, 7, "Select 8"),
        Button(1000, 750, 50, 8, "Select 9"),
        Button(100, 700, 80, 10, "Track 1"),
        Button(200, 700, 80, 20, "Track 2"),
        Button(300, 700, 80, 30, "Track 3"),
        Button(500, 700, 50, 40, "Stop"),
        Button(600, 700, 50, 50, "Play/Record"),

        Button(1100, 650, 50, 150, "Bank 1"),
        Button(1100, 700, 50, 160, "Bank 2"),
        Button(1100, 750, 50, 170, "Bank 3"),
    ]

    tracks = [
        Track(100, 100, 900, 140, 15),
        Track(100, 300, 900, 140, 25),
        Track(100, 500, 900, 140, 35),
    ]

    def __init__(self):
        global active_track
        active_track = None

    def update_select_buttons(self):
        global active_track
        for button in self.buttons:
            if button.text.startswith("Select"):
                button_id = button.button_id
                if 0 <= button_id <= 8:
                    sound_path = f'sounds/banks/{active_track}/{button_id}.mp3'
                    print(f"Assigning sound to button {button_id}: {sound_path}")
                    button.sound = pygame.mixer.Sound(sound_path)

    def handle_play_record_button_click(self):
        global active_track
        if active_track is not None and isinstance(active_track, Track):
            if active_track.recording:
                active_track.toggle_recording()
                active_track.add_recorded_sequence(active_track.recorded_sequence)
                active_track.recorded_sequence = []
            active_track.play_recorded_sequence()
            active_track.toggle_recording()

ui_board = UIBoard()

while ui_board.run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in ui_board.buttons:
                if button.is_clicked(mouse_pos):
                    button.click()
                    if button.button_id in [150, 160, 170]:
                        active_track = int((button.button_id - 150) / 10) + 1
                        ui_board.update_select_buttons()
                    elif button.button_id in [10, 20, 30]:
                        active_track = int(button.button_id / 10) + 1
                    elif button.button_id == 40:
                        if active_track is not None:
                            active_track = None
                            ui_board.update_select_buttons()
                    elif button.button_id == 50:
                        ui_board.handle_play_record_button_click()
                    else:
                        button.play_sound()
                        if active_track is not None and isinstance(active_track, Track):
                            active_track.handle_button_click(button.button_id)

    pygame.display.update()
    ui_board.clock.tick(40)
    ui_board.window.fill((225, 225, 225))

    for button in ui_board.buttons:
        button.update()

    for track in ui_board.tracks:
        track.draw(ui_board.window)

    for button in ui_board.buttons:
        button.draw(ui_board.window)

def initialize():
    global sound_banks, bpm, bpm_ms

    for b in range(3):
        for s in range(9):
            path = "sounds/banks/"+str(b)+"/"+str(s)+".mp3"
            sound_banks[b][s] = pygame.mixer.Sound(path)

    bpm_ms = bpm_bar_to_ms(bpm)

def bpm_bar_to_ms(bpm):
    return 60000 / (bpm * 4)

def play_sound(sound):
    print(f"Playing sound from bank {sound}")
    sound.play()

def record_sound(sound_index):
    global recording, sequences, active_track
    if recording and active_track is not None:
        sequences[active_track][sound_index][sequence_position] = 1

def play_sequence_bar():
    global sequence_position, active_track
    for track_index, track in enumerate(sound_banks[active_track]):
        for sound_index, sound in enumerate(track):
            if sound[sequence_position] == 1:
                play_sound(sound_banks[active_track][sound_index])
    if sequence_position < 15:
        sequence_position += 1
    else:
        sequence_position = 0
    print(f"Playing sequence bar at position {sequence_position}")

def button_delay(button):
    global delay
    button = False
    time.sleep(delay)
    button = True

def play_stop(pin):
    global playing
    playing = not playing
    print(f"Playing status: {playing}")

def switch_recording(pin):
    global recording, playing
    recording = not recording
    if recording and not playing:
        playing = True
    print(f"Recording status: {recording}, Playing status: {playing}")

def x1y1_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x1y1)
        record_sound(0)
        play_sound(sound_banks[active_track][0])
    print(f"x1y1 event: active_track={active_track}")

def x1y2_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x1y2)
        record_sound(1)
        play_sound(sound_banks[active_track][1])
    print(f"x1y2 event: active_track={active_track}")

def x1y3_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x1y3)
        record_sound(2)
        play_sound(sound_banks[active_track][2])
    print(f"x1y3 event: active_track={active_track}")

def x2y1_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x2y1)
        record_sound(3)
        play_sound(sound_banks[active_track][3])
    print(f"x2y1 event: active_track={active_track}")

def x2y2_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x2y2)
        record_sound(4)
        play_sound(sound_banks[active_track][4])
    print(f"x2y2 event: active_track={active_track}")

def x2y3_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x2y3)

def x3y1_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x3y1)
        record_sound(6)
        play_sound(sound_banks[active_track][6])
    print(f"x3y1 event: active_track={active_track}")

def x3y2_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x3y2)
        record_sound(7)
        play_sound(sound_banks[active_track][7])
    print(f"x3y2 event: active_track={active_track}")

def x3y3_event(pin):
    global active_track
    if active_track is not None:
        button_delay(x3y3)
        record_sound(8)
        play_sound(sound_banks[active_track][8])
    print(f"x3y3 event: active_track={active_track}")

initialize()

try:
    while True:
        if playing:
            play_sequence_bar()
            time.sleep(bpm_ms)
except:
    a = 1+1


initialize()

try:
    while True:
        if playing:
            play_sequence_bar()
            time.sleep(bpm_ms)
except:
    a = 1+1
