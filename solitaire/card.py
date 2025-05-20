class Card:
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = [str(n) for n in range(1, 11)] + ['J', 'Q', 'K']

    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

    def flip(self):
        self.face_up = not self.face_up

    def __repr__(self):
        return f"{self.rank}{self.suit}" if self.face_up else "XX"
