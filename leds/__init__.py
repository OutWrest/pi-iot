from leds.led import LEDStrip

def new_strip(num_leds, pin, freq_hz=800000, dma=10, invert=False, channel=0):
    # LED_COUNT: int, LED_PIN: int = 18, LED_FREQ_HZ: int = 800000, LED_DMA: int = 10, LED_INVERT: bool = False, LED_CHANNEL: int = 0
    return LEDStrip(num_leds, pin, freq_hz, dma, invert, channel)