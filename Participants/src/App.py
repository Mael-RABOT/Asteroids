import Wrapper


class App:
    def __init__(self):
        self.wrapper = Wrapper.Wrapper(1920, 1080)

    def run(self):
        self.wrapper.run()
