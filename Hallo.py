


class Auto:
    def __init__(self, farbe):
        self.farbe = farbe

    def hupen(self):
        print('Peep ' + self.farbe)


rote_auto = Auto('rot')
blau_auto = Auto('blau')
gelbe_auto = Auto('gelb')
autos = [rote_auto.farbe, blau_auto.farbe, gelbe_auto.farbe]

for i in autos:
    print(i)

rote_auto.hupen()

