# war_game.py
from collections import deque
from deck import Deck, Card

def card_value(card: Card):
    return Deck.rank_values[card.rank]

class WarGame:
    def __init__(self, shuffle: bool = True, round_limit: int = 10000):
        deck = Deck(shuffle=shuffle)
        self.p1, self.p2 = deck.deal()  # p1 is human, p2 is computer
        self.round_limit = round_limit
        self.round = 0
        self.pile = deque()  # central pile for war resolution

    def _draw_card(self, player_deck: deque):
        return player_deck.popleft() if player_deck else None

    def _collect_pile_for_winner(self, winner_deck: deque):
        # Winner takes all cards in pile (in order they were placed)
        while self.pile:
            winner_deck.append(self.pile.popleft())

    def _simple_round(self):
        """Play one basic round (no recursive war). Returns winner str or 'tie'."""
        c1 = self._draw_card(self.p1)
        c2 = self._draw_card(self.p2)

        if c1 is None:
            return "p2"
        if c2 is None:
            return "p1"

        # place both cards in the pile in the order played
        self.pile.append(c1)
        self.pile.append(c2)

        v1 = card_value(c1)
        v2 = card_value(c2)

        if v1 > v2:
            self._collect_pile_for_winner(self.p1)
            return "p1"
        elif v2 > v1:
            self._collect_pile_for_winner(self.p2)
            return "p2"
        else:
            return "tie"

    def _war(self):
        """Resolve a war: each player places up to 3 face-down cards and then one face-up.
           If a player runs out of cards at any point they lose (or give what's left)."""
        print("=== WAR! Each player places 3 face-down cards (or as many as they can) and 1 face-up ===")
        # Each player places 3 face-down (or fewer if they don't have enough)
        for i in range(3):
            if self.p1:
                self.pile.append(self._draw_card(self.p1))
            if self.p2:
                self.pile.append(self._draw_card(self.p2))

        # Now play the deciding face-up card (if possible)
        c1 = self._draw_card(self.p1)
        c2 = self._draw_card(self.p2)

        if c1:
            self.pile.append(c1)
        if c2:
            self.pile.append(c2)

        # If one player couldn't draw a deciding card, the other wins automatically
        if c1 is None and c2 is None:
            return None  # both out — tie (rare)
        if c1 is None:
            self._collect_pile_for_winner(self.p2)
            return "p2"
        if c2 is None:
            self._collect_pile_for_winner(self.p1)
            return "p1"

        v1 = card_value(c1)
        v2 = card_value(c2)

        print(f"War face-off: Player plays {c1.rank} of {c1.suit} vs Computer plays {c2.rank} of {c2.suit}")

        if v1 > v2:
            self._collect_pile_for_winner(self.p1)
            return "p1"
        elif v2 > v1:
            self._collect_pile_for_winner(self.p2)
            return "p2"
        else:
            # War continues recursively
            return "tie"

    def play_one_round(self):
        """Play one interactive round, showing both cards."""
        self.round += 1
        if self.round > self.round_limit:
            print("Round limit reached.")
            return "limit"

        print(f"\n--- Round {self.round} ---")
        print(f"Your cards: {len(self.p1)} | Computer cards: {len(self.p2)}")

        c1 = self._draw_card(self.p1)
        c2 = self._draw_card(self.p2)

        if c1 is None:
            print("You are out of cards — computer wins the game.")
            return "p2"
        if c2 is None:
            print("Computer is out of cards — you win the game!")
            return "p1"

        # Add cards to central pile
        self.pile.append(c1)
        self.pile.append(c2)

        print(f"You play:      {c1.rank} of {c1.suit}")
        print(f"Computer plays:{c2.rank} of {c2.suit}")

        v1, v2 = card_value(c1), card_value(c2)

        # Determine outcome or trigger war
        if v1 > v2:
            print("You win this round!")
            self._collect_pile_for_winner(self.p1)
            return "p1"

        elif v2 > v1:
            print("Computer wins this round.")
            self._collect_pile_for_winner(self.p2)
            return "p2"

        else:
            print("War! Same value — drawing extra cards...")
            result = "tie"

            # Handle potential chained wars
            while result == "tie":
                result = self._war()

                if result == "p1":
                    print("You win the war and take the pile!")
                    return "p1"
                elif result == "p2":
                    print("Computer wins the war and takes the pile.")
                    return "p2"
                elif result is None:
                    print("Both players ran out of cards — draw.")
                    return "draw"
                else:
                    print("Another tie! Continuing WAR...")

    def is_game_over(self):
        if not self.p1:
            return "p2"
        if not self.p2:
            return "p1"
        return None

    def play_interactive(self):
        print("Welcome to War! You are Player 1. Commands: [enter] play next round, 's' show counts, 'q' quit")
        while True:
            over = self.is_game_over()
            if over:
                if over == "p1":
                    print("\n*** You collected all the cards. YOU WIN! ***")
                else:
                    print("\n*** Computer collected all the cards. YOU LOSE. ***")
                break

            cmd = input("\nPress Enter to play next round, 's' to show deck sizes, 'q' to quit: ").strip().lower()
            if cmd == "q":
                print("Quitting game — final card counts:")
                print(f"You: {len(self.p1)} | Computer: {len(self.p2)}")
                break
            if cmd == "s":
                print(f"You: {len(self.p1)} cards | Computer: {len(self.p2)} cards")
                continue

            # Play one round
            round_result = self.play_one_round()
            if round_result == "limit":
                print("Reached round limit — ending game.")
                break
            if round_result == "draw":
                print("Game ended in a draw.")
                break

if __name__ == "__main__":
    g = WarGame()
    g.play_interactive()
