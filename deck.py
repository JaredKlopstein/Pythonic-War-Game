# deck.py
from collections import namedtuple, deque
import random

Card = namedtuple("Card", ["rank", "suit"])

class Deck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()
    rank_values = {str(i): i for i in range(2, 11)}
    rank_values.update(dict(J=11, Q=12, K=13, A=14))

    def __init__(self, shuffle: bool = True):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        if shuffle:
            random.shuffle(self._cards)

    def deal(self):
        """Return two deques (half the deck each)."""
        half = len(self._cards) // 2
        p1 = deque(self._cards[:half])
        p2 = deque(self._cards[half:])
        return p1, p2

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return f"Deck({len(self)} cards)"

