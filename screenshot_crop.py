from PIL import Image
import PIL.ImageOps
import os


def crop_many_screenshots():
    path = "screenshots"
    for(dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            img = Image.open(os.path.join(dirpath, file))
            width, height = img.size
            pixels_to_crop = []
            with open("resolutions.txt", "r") as resolutions:
                line = resolutions.readline().strip()
                while line:
                    parts = line.split(':')
                    if str(width) + ',' + str(height) == parts[0]:
                        pixels_to_crop = parts[1].split(',')
                        pixels_to_crop = [int(pixel) for pixel in pixels_to_crop]
                    line = resolutions.readline().strip()
                cropped_img = img.crop(pixels_to_crop)

            f, e = os.path.splitext(file)
            cropped_img.save("cropped" + os.sep + f + "_cropped.png", "PNG", quality=100)


def crop_screenshot(file):
    img = Image.open(file)
    width, height = img.size
    pixels_to_crop = []
    with open("resolutions.txt", "r") as resolutions:
        line = resolutions.readline().strip()
        while line:
            parts = line.split(':')
            if str(width) + ',' + str(height) == parts[0]:
                if os.path.splitext(file)[1].lower() == '.png':
                    img = img.convert('RGB')

                pixels_to_crop = parts[1].split(',')
                pixels_to_crop = [int(pixel) for pixel in pixels_to_crop]
                cropped_img = img.crop(pixels_to_crop)

            line = resolutions.readline().strip()

        if len(pixels_to_crop) == 0:
            print("Resolution", width, height, "of your screenshot not found in resolutions text for screenshot", file,
                  "Please add your dimensions into resolutions.txt as detailed on https://github.com/BradfordBach/NMSLocator")

    try:
        os.makedirs("cropped")
    except FileExistsError:
        pass

    invert_cropped_img = PIL.ImageOps.invert(cropped_img)
    invert_cropped_img.save("cropped" + os.sep + os.path.splitext(os.path.basename(file))[0] + "_cropped.png", "PNG", quality=100)
    return "cropped" + os.sep + os.path.splitext(os.path.basename(file))[0] + "_cropped.png"
