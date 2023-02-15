from sprite import *


class SetTime:
    def __init__(self):
        self.time = Actor('time1', pos=(WIDTH - 132, 0), anchor=(0, 0))
        self.time.images = get_sprites(24, 'time')
        self.time.scale = 2.5

        self.date = Actor('date1', pos=(WIDTH - 153, 45), anchor=(0, 0))
        self.date.images = get_sprites(7, 'date')
        self.date_day = 1
        self.date.scale = 2.5

        self.time_start = time.time()
        self.time_now = None
        self.time_oclock = 1

    def draw(self):
        self.date.draw()
        self.time.draw()

    def load_save(self, timeoclock, dateday):

        def change(ob, x):
            for i in range(x):
                ob.next_image()

        diff_time = 24 - self.time_oclock
        diff_date = 7 - self.date_day
        change(self.time, diff_time)
        change(self.date, diff_date)
        change(self.time, timeoclock)
        change(self.date, dateday)
        self.time_oclock = timeoclock
        self.date_day = dateday

    def update(self):

        self.time_now = time.time()
        if self.time_start + 5 < self.time_now:  # SET TIME PERIOD
            self.time.next_image()
            self.time_start = time.time()
            self.time_oclock += 1
            if self.time_oclock == 25:
                self.date.next_image()
                self.date_day += 1
                self.time_oclock = 1
                if self.date_day > 7:
                    self.date_day = 1
                