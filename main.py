import pygame, random, time

pygame.init()
window = pygame.display.set_mode((900, 605))
pygame.display.set_caption("Typing Challenge")
font = pygame.font.SysFont('Comic Sans', 30)
starttime = None
words = [
    "apple", "orange", "banana", "grape", "peach", "pear", "plum", "mango", "lemon", "lime",
    "bread", "butter", "cheese", "milk", "cream", "sugar", "salt", "pepper", "honey", "cereal",
    "table", "chair", "couch", "desk", "shelf", "door", "window", "floor", "ceiling", "wall",
    "river", "ocean", "lake", "stream", "pond", "beach", "island", "mountain", "valley", "forest",
    "cloud", "rain", "snow", "wind", "storm", "thunder", "lightning", "sunshine", "shadow", "rainbow",
    "book", "paper", "pencil", "eraser", "notebook", "folder", "binder", "marker", "ruler", "calculator",
    "computer", "screen", "keyboard", "mouse", "speaker", "camera", "phone", "tablet", "charger", "battery",
    "car", "truck", "bicycle", "scooter", "train", "airplane", "boat", "ship", "subway", "highway",
    "music", "rhythm", "melody", "harmony", "tempo", "lyric", "chorus", "verse", "note", "scale",
]
chosen = [random.choice(words) for _ in range(35)]
print(chosen)


def write(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont('Helvetica', size)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))


class Letter:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y

        self.highlightrect = pygame.rect.Rect(x - 2, y + 5, 25, 30)
        self.highlighton = 0

    def draw(self, color=(0, 0, 0)):
        if self.highlighton == 1:
            pygame.draw.rect(window, (144, 238, 144), self.highlightrect)
        if self.highlighton == -1:
            pygame.draw.rect(window, (255, 204, 203), self.highlightrect)
        text_surface = font.render(self.letter, True, color)
        window.blit(text_surface, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, function, text, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.show = True
        self.text = text
        self.color = color
        self.toggle = False

    def draw(self):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.width, self.height])
        write(self.text, 20, self.x + self.width / 6, self.y + self.height / 6, (0, 0, 0))

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if (self.x < self.mouse[0] < self.x + self.width and
                self.y < self.mouse[1] < self.y + self.height and
                mouse_buttons[0]):
            self.function()


letters = []
done = []
stepy = 1
lettery = 0
x, y = 20, 75
for word in chosen:
    for char in word:
        letters.append(Letter(char, x, y))
        x += 23
    space = Letter(" ", x, y)
    letters.append(space)
    x += 20
    if x > 700:
        x = 20
        y += 50


def draw_words():
    for letter in letters:
        letter.draw()


index = 0

letters2 = []
x, y = 20, 200
for word in chosen:
    for char in word:
        letters2.append(Letter(char, x, y))
        x += 23
    space = Letter(" ", x, y)
    letters2.append(space)
    x += 20
    if x > 700:
        x = 20
        y += 50


def draw_box():
    pygame.draw.rect(window, (255, 255, 255), (10, 200, 875, 390))


iterate = False


def showcaseon():
    global iterate
    iterate = True


def goodScreen():
    running = True
    print(done)
    correct = []
    for i in done:
        if i:
            correct.append(i)
    accuracy = (len(correct) / len(done)) * 100
    wpm = int(len(correct) / 5) / ((time.time() - starttime) / 60)
    iteration = 0
    clock = pygame.time.Clock()
    buttons = []
    play = Button(50, 150, 85, 35, showcaseon, "Replay")

    buttons.append(play)
    while running:
        window.fill((25, 25, 112))
        draw_box()
        write(f"Accuracy: ", 30, 50, 75)
        write(f"{accuracy:.2f}%", 50, 200, 60)
        write(f"WPM: ", 30, 500, 75)
        write(f"{int(wpm)}", 50, 675, 60)
        for button in buttons:
            button.update()
            button.draw()
        if iterate:
            if iteration > len(done) - 1:
                iteration = 0
            if done[iteration] == True:
                letters2[iteration].highlighton = 1
            else:
                letters2[iteration].highlighton = -1
            iteration += 1

        for letter in letters2:
            letter.draw()

        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        pygame.display.update()


safe = False


def updates(event):
    global index, safe, starttime
    if index == 1:
        starttime = time.time()
    if event.type == pygame.KEYDOWN and index < len(letters):
        key = event.unicode
        if key == letters[index].letter:
            done.append(True)
            letters[index].highlighton = 1
        else:
            done.append(False)
            letters[index].highlighton = -1
        index += 1
        safe = True
    for e, i in enumerate(letters):
        if i.highlighton == 0:
            break
        if e == len(letters) - 1:
            goodScreen()


running = True

while running:
    window.fill((255, 255, 255))
    draw_words()
    correct = []
    for i in done:
        if i:
            correct.append(i)
    if safe:
        accuracy = (len(correct) / len(done)) * 100
        write(f"Accuracy: {accuracy:.2f}%", 25, 50, 500, (0, 0, 0))
        wpm = int(len(correct) / 5) / ((time.time() - starttime) / 60)
        write(f"WPM: {int(wpm)}", 25, 50, 550, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        updates(event)
    pygame.display.update()
