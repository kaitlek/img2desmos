import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class _Utils:
    @staticmethod
    def RGBToHex(rgb):
        return '%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
            
    @staticmethod
    def ConvertToExpression(rgb, x, y):
        expression = "Calc.setExpression({color: '#" + _Utils.RGBToHex(rgb) + "', id: '" + str(x) + ":" +  str(y) + "', lineOpacity:'1', lineWidth: '1', latex:" + _Utils.CoordToLatex(x, y) + ", pointOpacity: '', fillOpacity: '1'});\n"
        return str(expression)
        
    @staticmethod
    def CoordToLatex(x, y):
        points = [
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0),
        ]
        
        points = [(x + p[0], y + p[1]) for p in points]
        points = points[::-1]
        latex = r"'\\operatorname{polygon}\\left(\\left[ " + ",".join(
            map(str, points)) + r"\\right]\\right)'"
        return latex


class img2desmos:
    def __init__(self, binaryLocation=None, width=800, height=800) -> None:
        seleniumOptions = Options()

        if binaryLocation:
            seleniumOptions.binary_location = binaryLocation

        
        self.driver = webdriver.Chrome(options=seleniumOptions)
        self.driver.set_window_size(width, height)
        self.driver.get(r'https://www.desmos.com/calculator')
        self.driver.execute_script('Calc.updateSettings({"expressions": false});')

            
    def DrawImage(self, imgPath, quality):
        inputImage = cv2.imread(imgPath)
        inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
        inputImage = cv2.flip(inputImage, 0)
        height, width = inputImage.shape[:2]
        
        outputString = ""

        aspectRatio = width / height

        if width > height:
            w = quality
            h = int(w / aspectRatio)
        else:
            h = quality
            w = int(h * aspectRatio)

        temp = cv2.resize(inputImage, (w, h), interpolation=cv2.INTER_LINEAR)

        for y in range(h):
            for x in range(w):
                outputString += _Utils.ConvertToExpression(temp[y][x], x, y)
                
        print(f"Finished processing! Executing {len(outputString.splitlines())} lines of code")

        
        zoom_func = f"""
            const currentRect = document.querySelector("#graph-container > div > div > div > div.dcg-grapher.dcg-grapher-2d > div:nth-child(3) > div").getBoundingClientRect();
            const width_current = currentRect.width;
            const height_current = currentRect.height;
            const aspect_ratio_current = width_current / height_current;
            const width_new = {quality} * 4; 
            const height_new = width_new / aspect_ratio_current;
            const midX = width_new / 4 
            const midY = width_new / 4

            const newXMin = midX - width_new / 2;
            const newXMax = midX + width_new / 2;
            const newYMin = midY - height_new / 2;
            const newYMax = midY + height_new / 2;

            Calc.setViewport([newXMin, newXMax, newYMin, newYMax]);

        """
        start = time.time()
        self.driver.execute_script(zoom_func)
        scriptLines = outputString.strip().split('\n')
        linesPerChunk = (x + 1)

        for i in range(0, len(scriptLines), linesPerChunk):
            chunk = '\n'.join(scriptLines[i:i + linesPerChunk])
            self.driver.execute_script(chunk)


        end = time.time()
        timeTaken = end - start
        print(f"Took {timeTaken:.2f} seconds")
        input("Press enter to close everything...")
        self.driver.quit()