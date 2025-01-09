from PIL import Image, ImageDraw
image_path = "project/images/14.png"
image = Image.open(image_path)
boxs = [(250, 120, 400, 180),(260,1890,540,1990),(2540,110,2670,180),(2690,220,2890,390),(3240,240,3390,380)]
draw = ImageDraw.Draw(image)
for region in boxs:
    draw.rectangle(region, outline="red", width=3)
output_path = "regions.png"
image.save(output_path)
