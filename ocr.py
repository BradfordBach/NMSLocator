import pytesseract
from PIL import Image
import PIL.ImageOps
import os


def ocr_many():
    for(dirpath, dirnames, filenames) in os.walk("cropped"):
        for file in filenames:
            print(os.path.join(dirpath, file))

            screenshot_text = pytesseract.image_to_string(Image.open(os.path.join(dirpath, file)))
            screenshot_lines = screenshot_text.split('\n')
            for line in screenshot_lines:
                if "System" in line:
                    line_split = line.split('System')
                    if '-l' in line_split:
                        line_split = line_split.replace('-l', '-I')
                    if '|' in line_split:
                        line_split = line_split.replace('|', 'I')
                    print(line_split[0].strip())
                if "REGION" in line:
                    print(line.split(':')[1].strip())
                if "Sell:" in line:
                    print(line.split('//')[-1].strip())


def ocr_screenshot(file, tesseract):
    pytesseract.pytesseract.tesseract_cmd = tesseract
    screenshot_text = pytesseract.image_to_string(Image.open(file))
    filename = os.path.splitext(os.path.basename(file))[0]
    with open("cropped" + os.sep + filename + '.log', "w") as ocr_log:
        ocr_log.write(screenshot_text)
    if screenshot_text:
        screenshot_lines = screenshot_text.split('\n')
        system_info = {'system': None, 'region': None, 'econ': None, 'life': None}
        for line in screenshot_lines:
            if "System" in line:
                line_split = line.split('System')
                system_info['system'] = fix_common_ocr_issues(line_split[0].strip())
            if "REGION" in line:
                system_info['region'] = fix_common_ocr_issues(line.split(':')[1].strip())
            if "Sell:" in line:
                econ_values = ["Declining", "Destitute", "Failing", "Fledgling", "Low Supply", "Struggling", "Unpromising", "Unsuccessful",
                               "Adequate", "Balanced", "Comfortable", "Developing", "Medium Supply", "Promising", "Satisfactory", "Sustainable",
                               "Advanced", "Affluent", "Booming", "Flourishing", "High Supply", "Opulent", "Prosperous", "Wealthy"]
                #print(line.split('//')[-1].strip())
                if line.split('//')[-1].strip() in econ_values:
                    system_info['econ'] = line.split('//')[-1].strip()
                elif "Med" in line.split('//')[-1].strip():
                    system_info['econ'] = 'Medium Supply'
            if "Gek" in line:
                system_info['life'] = "Gek"
            if "Korvax" in line:
                system_info['life'] = "Korvax"
            if "Vy'keen" in line:
                system_info['life'] = "Vy'keen"

        if not system_info['system'] or not system_info['region']:
            print('Skipping latest screenshot, no system or region info found.')
            return None
        else:
            return system_info
    else:
        print('Skipping latest screenshot, no system or region info found.')
        return None


def fix_common_ocr_issues(text):
    if '-l' in text:
        text = text.replace('-l', '-I')
    if '|' in text:
        text = text.replace('|', 'I')
    if text[:1] == 'l':
        text = list(text)
        text[0] = 'I'
        text = ''.join(text)
    if ' l ' in text:
        text = text.replace(' l ', ' I ')
    if ' Ill' in text:
        text = text.replace(' Ill', ' III')
    if ' lV' in text:
        text = text.replace(' lV', ' IV')
    if ' XVIll' in text:
        text = text.replace(' XVIll', ' XVIII')

    return text
