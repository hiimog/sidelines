from PIL import *

pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
sizes = {"l": 1000, "m": 500, "s": 250, "xs": 100}
all_width = 250 * len(pieces)
colors = ["", "black", "white"]

for piece in pieces:
    for color in colors:
        original = Image.open(f"{color}{piece}-xl.png")
        for letter, number in sizes.items():
            print(f"Working on {color}{piece}-{letter}.png")
            copy = original.resize((number, number))
            copy.save(f"{color}{piece}-{letter}.png")
for color in colors:
    im = Image.new("RGBA", (all_width, 250))
    
    for i, piece in enumerate(pieces):
        piece_img = Image.open(f"{color}{piece}-s.png")
        location = (i * 250, 0)
        im.paste(piece_img, location)
    im.save(f"all{color}.png")
