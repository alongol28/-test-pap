import random
from dataclasses import dataclass, field
from typing import List
from .card import Card

@dataclass
class Pile:
    cards: List[Card] = field(default_factory=list)

    def push(self, card: Card):
        self.cards.append(card)

    def pop(self):
        return self.cards.pop() if self.cards else None

    def top(self):
        return self.cards[-1] if self.cards else None

    def is_empty(self):
        return not self.cards

    def __len__(self):
        return len(self.cards)

class Klondike:
    def __init__(self):
        self.stock = Pile()
        self.waste = Pile()
        self.foundations = [Pile() for _ in range(4)]
        self.tableau = [Pile() for _ in range(7)]
        self._setup()

    def _create_deck(self):
        deck = [Card(suit, rank, face_up=False)
                for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(deck)
        return deck

    def _setup(self):
        deck = self._create_deck()
        # deal tableau
        for i in range(7):
            for j in range(i + 1):
                card = deck.pop()
                if j == i:
                    card.face_up = True
                self.tableau[i].push(card)
        # remaining cards to stock
        for card in deck:
            self.stock.push(card)

    def draw(self):
        if self.stock.is_empty():
            # reset from waste
            while not self.waste.is_empty():
                card = self.waste.pop()
                card.face_up = False
                self.stock.push(card)
        if not self.stock.is_empty():
            card = self.stock.pop()
            card.face_up = True
            self.waste.push(card)

    def move(self, source: str, dest: str, count: int = 1):
        src_pile = self._get_pile(source)
        dst_pile = self._get_pile(dest)
        if src_pile is None or dst_pile is None:
            print("Invalid pile name")
            return False
        if len(src_pile) < count:
            print("Not enough cards in source pile")
            return False
        moving = src_pile.cards[-count:]
        # Basic validation: allow single card move if allowed by suit/rank
        if dest.startswith('f'):
            if count != 1:
                print("Can only move one card to foundation")
                return False
            card = moving[0]
            foundation_index = int(dest[1]) - 1
            foundation = self.foundations[foundation_index]
            if foundation.is_empty():
                if card.rank != '1':
                    print("Foundation must start with Ace")
                    return False
            else:
                top_card = foundation.top()
                # ranks are strings '1'..'10','J','Q','K'
                rank_order = Card.RANKS
                if card.suit != top_card.suit or rank_order.index(card.rank) != rank_order.index(top_card.rank) + 1:
                    print("Invalid foundation move")
                    return False
            for _ in range(count):
                src_pile.pop()
            dst_pile.push(card)
            if not src_pile.is_empty() and not src_pile.top().face_up:
                src_pile.top().flip()
            return True
        elif dest.startswith('t'):
            card = moving[0]
            tableau_index = int(dest[1]) - 1
            tableau = self.tableau[tableau_index]
            # simplified check: if tableau empty, must be King
            if tableau.is_empty():
                if card.rank != 'K':
                    print("Empty tableau must be filled with King")
                    return False
            else:
                top_card = tableau.top()
                rank_order = Card.RANKS
                if top_card.face_up:
                    if rank_order.index(card.rank) + 1 != rank_order.index(top_card.rank):
                        print("Rank mismatch")
                        return False
                    if (Card.SUITS.index(card.suit) % 2) == (Card.SUITS.index(top_card.suit) % 2):
                        print("Color must alternate")
                        return False
                else:
                    print("Cannot place on a face-down card")
                    return False
            for _ in range(count):
                src_pile.pop()
            for c in moving:
                dst_pile.push(c)
            if not src_pile.is_empty() and not src_pile.top().face_up:
                src_pile.top().flip()
            return True
        else:
            print("Invalid destination")
            return False

    def _get_pile(self, name: str):
        name = name.lower()
        if name == 'waste':
            return self.waste
        if name == 'stock':
            return self.stock
        if name.startswith('f') and name[1:].isdigit():
            idx = int(name[1:]) - 1
            if 0 <= idx < 4:
                return self.foundations[idx]
        if name.startswith('t') and name[1:].isdigit():
            idx = int(name[1:]) - 1
            if 0 <= idx < 7:
                return self.tableau[idx]
        return None

    def display(self):
        print("Stock:", len(self.stock.cards))
        print("Waste:", ' '.join(map(str, self.waste.cards)))
        for i, f in enumerate(self.foundations, 1):
            print(f"F{i}:", ' '.join(map(str, f.cards)))
        for i, t in enumerate(self.tableau, 1):
            show = []
            for card in t.cards:
                if card.face_up:
                    show.append(str(card))
                else:
                    show.append("[]")
            print(f"T{i}:", ' '.join(show))


