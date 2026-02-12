from old_code.Modes.DefaultMode import DefaultMode


class ScooterMode(DefaultMode):
    def __init__(self, file):
        super().__init__(file=file)
        self.tags = [('highway', 'primary'), ('highway', 'secondary'), ('highway', 'tertiary'),
                     ('highway', 'residential'),
                     ('highway', 'pedestrian'), ('highway', 'service')]

    # обязательно переопределить метод добавления тегов для самокатика - брать только подходящую скорость
    # можно задать переменную с максимальной допустимой скоростью
