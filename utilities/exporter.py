import os
import time
from PIL import Image, ImageDraw

def save_payload_as_png(payload, output_dir="noteimg"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    width = payload.get("width", 800)
    height = payload.get("height", 600)

    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)

    lines = payload.get("lines", [])
    for line in lines:
        color = line.get("color", "#000000")
        points = line.get("points", [])

        coord_tuples = [(pt["x"], pt["y"]) for pt in points]

        if len(coord_tuples) >= 2:
            draw.line(coord_tuples, fill=color, width=3, joint="round")
        elif len(coord_tuples) == 1:
            x, y = coord_tuples[0]
            draw.ellipse([x-2, y-2, x+2, y+2], fill=color)

#make timestamps to ovoid overwriting files
    timestamp = int(time.time())
    filename = f"note_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    image.save(filepath, "PNG")
    print(f"[SUCCESS] Exported vector plot to disk: {filepath}")
    return filepath