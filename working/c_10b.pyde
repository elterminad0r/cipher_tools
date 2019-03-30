WIN_SIZE = 972

with open("key.txt", "r") as keyfile:
    key_tab = [line.split() for line in keyfile]

def setup():
    size(WIN_SIZE * 7 / 26, WIN_SIZE)

def draw_grid():
    background(0)
    scale(width / 7.0, height / 26.0)
    colorMode(HSB, 255, 255, 255)
    textMode(CENTER)
    noStroke()
    for y, line in enumerate(key_tab):
        for x, n in enumerate(line):
            if n.isdigit():
                fc = color(int(n) * 255.0 * 5.0 / 6.0 / 26.0, 255, 255)
                fill(fc)
                rect(x, y, 1, 1)
                if 255.0 * 1.0 / 12.0 < hue(fc) < 255.0 * 7.0 / 12.0:
                    fill(0)
                else:
                    fill(255)
                pushMatrix()
                translate(x + 0.5, y + 0.5)
                scale(7.0 / width, 26.0 / height)
                text(n, -textWidth(n) * 0.5, textAscent() * 0.5)
                popMatrix()

def draw():
    draw_grid()

def keyPressed():
    if keyCode == ord("Q"):
        exit()
