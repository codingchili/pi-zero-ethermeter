from blinkt import set_clear_on_exit, set_pixel, show, set_brightness, clear
import asyncio
import colorsys

class CoinDisplay:
    """ a class to represent the value of ether on a RPI zero BLINKT """
    animation_task = None   # animation task saved so it may be cancelled.
    percent_change = 0.0
    loop = None

    def __init__(self, loop):
        self.loop = loop
        set_brightness(0.1)
        set_clear_on_exit()
    
    def start(self, loop, animation):
        self.cancel()
        self.animation_task = self.loop.create_task(animation())

    def cancel(self):
        if (self.animation_task != None):
            self.animation_task.cancel()
            clear()
            show()

    def on_load(self):
        """ called before the exchange api is called to indicate loading """
        self.start(self.loop, self.loading_animation)

    def on_error(self):
        """ called when an api error has occured """
        self.start(self.loop, self.error_animation)

    def on_data(self, percent_change):
        """ called with the results from the exchange api as a dict """
        self.percent_change = percent_change
        self.start(self.loop, self.value_animation)

    @asyncio.coroutine
    def error_animation(self):
        while (1):
            clear()
            for index in range(0, 8):
                set_pixel(index, 255, 0, 32)
                show()
                yield from asyncio.sleep(0.1)
            for index in range(0, 8):
                set_pixel(index, 0, 0, 0)
                show()
                yield from asyncio.sleep(0.05)

    @asyncio.coroutine
    def loading_animation(self):
        sleep = 0.05
        time = 0
        while (1):
            hue = int(time * 200) % 360
            for index in range(3, 5):
                h = ((hue - 60 * index) % 360) / 360.0
                r, g, b = [int(color * 255) for color in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                set_pixel(index, r, g, b)
            show()
            yield from asyncio.sleep(sleep)
            time += sleep

    @asyncio.coroutine
    def value_animation(self):
        # default to green for +%
        color = [118, 255, 3]

        # set color to red if -%
        if self.percent_change < 0:
            color = [242, 8, 0]

        # for each 1% light an additional led, max +/- 8%.
        self.update_pixels(0, min(round(abs(self.percent_change)), 8), color)
        yield from asyncio.sleep(0)

    def update_pixels(self, pixel_from, pixel_to, color):
        """ updates the given pixels to the given color after clearing. """
        clear()
        for index in range(pixel_from, pixel_to):
            set_pixel(index, color[0], color[1], color[2])
        show()
