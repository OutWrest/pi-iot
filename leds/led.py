import time
from rpi_ws281x import *

class LEDStrip:
    def __init__(self, LED_COUNT: int, LED_PIN: int = 18, LED_FREQ_HZ: int = 800000, LED_DMA: int = 10, LED_INVERT: bool = False, LED_CHANNEL: int = 0) -> None:
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, 255, LED_CHANNEL)
        self.strip.begin()
        self.rgb_offset = 0

    def changeBrightness(self, brightness: int) -> None:
        self.strip.setBrightness(brightness)

    def show(self) -> None:
        self.strip.show()

    def colorWipe(self, color, wait_ms=25):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChase(self, color, wait_ms=25, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def setColor(self, color, wait_ms=50) -> None:
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        time.sleep(wait_ms/1000.0)

    @staticmethod
    def getColor(r: int = 0, g: int = 0, b: int = 0) -> Color:
        return Color(r, g, b)

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def transition(self, r1, g1, b1, r2, g2, b2, wait_ms=15):
        max_diff = max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))

        for j in range(max_diff + 1):
            for i in range(self.strip.numPixels()):
                # set all the pixels to the transition of the colors
                self.strip.setPixelColor(i, Color(r1 + (r2 - r1) * j // max_diff, g1 + (g2 - g1) * j // max_diff, b1 + (b2 - b1) * j // max_diff))
                self.strip.show()
                time.sleep(wait_ms/1000.0)


    def rainbow(self, wait_ms=30, iterations=1):
        self.transition(255, 0, 0, 0, 255, 0, wait_ms)
        self.transition(0, 255, 0, 0, 0, 255, wait_ms)
        self.transition(0, 0, 255, 0, 0, 255, wait_ms)
        self.transition(255, 0, 255, 0, 0, 255, wait_ms)
        self.transition(255, 255, 0, 255, 255, 0, wait_ms)
        

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms=25):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

