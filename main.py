# five-card-draw Poker.
import random

class Card:
    value_to_rank = {
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace"
    }

    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit
        self.rank = self._determine_rank(value)

    @staticmethod
    def _determine_rank(value: int) -> str:
        return Card.value_to_rank.get(value, "Unknown")

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class Deck:
    number_to_suit = {
        1: "Diamonds",
        2: "Hearts",
        3: "Spades",
        4: "Clubs"
    }

    def __init__(self):
        self.deck = self.generate_deck()
        self.deck = self.shuffle_deck()

    @staticmethod
    def generate_deck():
        generated_deck = []
        for i in range(1, 5):  # Loop from 1 to 4, representing suit.
            for j in range(2, 15):  # Loop from 1 to 15, representing value of the card
                card = Card(j, Deck.number_to_suit[i])
                generated_deck.append(card)
        return generated_deck

    def shuffle_deck(self):
        # return random.shuffle(self.deck) Can use random.shuffle for pre-made method.
        # Decided to implement my own for experience.

        shuffled_deck = []

        for i in range(len(self.deck)):
            n = len(self.deck)
            random_num = random.randint(0, n - 1)
            shuffled_deck.append(self.deck.pop(random_num))

        return shuffled_deck

    def draw_card(self):
        if self.deck:
            card = self.deck.pop(0)
            return card
        else:
            print("No more cards left in the deck.")
            return None


class Table:
    pass


class Hand:
    def __init__(self):
        self.cards_in_hand = []

    def add_card(self, card):
        self.cards_in_hand.append(card)

    def discard_at_index(self, index):
        if 0 <= index < len(self.cards_in_hand):
            self.cards_in_hand.pop(index)

    def check_value(self):
        if full_house := self._check_full_house():
            msg = f"{Card.value_to_rank[full_house[0]]}s full of {Card.value_to_rank[full_house[1]]}s"
            return msg
        elif flush := self._check_flush():
            msg = f"Flush of {flush}"
            return msg
        elif straight := self._check_straight():
            msg = f"{Card.value_to_rank[straight]} high straight!"
            return msg
        elif three_of_a_kind_value := self._check_three_of_a_kind():
            three_of_a_kind = Card.value_to_rank[three_of_a_kind_value]
            msg = f"Three of a kind {three_of_a_kind}s"
            return msg
        elif two_pair := self._check_two_pair():
            low_pair = Card.value_to_rank[two_pair[0]]
            high_pair = Card.value_to_rank[two_pair[1]]
            msg = f"Two Pair, {high_pair}s and {low_pair}s."
            return msg
        elif pair_value := self._check_pair():
            pair = Card.value_to_rank[pair_value]
            msg = f"Pair of {pair}"
            return msg
        else:
            high_card = self._check_high_card()
            high_card_rank = Card.value_to_rank[high_card.value]
            high_card_suit = high_card.get_suit()
            msg = f"Highcard, {high_card_rank} of {high_card_suit}"
            return msg

    def _check_full_house(self):
        self.cards_in_hand.sort()

        if self.cards_in_hand[0] == self.cards_in_hand[2]:
            if self.cards_in_hand[3] == self.cards_in_hand[4]:
                return self.cards_in_hand[0].value, self.cards_in_hand[3].value
        if self.cards_in_hand[2] == self.cards_in_hand[4]:
            if self.cards_in_hand[0] == self.cards_in_hand[1]:
                return self.cards_in_hand[2].value, self.cards_in_hand[0].value

        return None

    def _check_flush(self):
        check_suit = []
        card = self.cards_in_hand[0]
        card_suit = card.get_suit()
        check_suit.append(card_suit)

        for i in range(1, len(self.cards_in_hand)):
            card = self.cards_in_hand[i]
            card_suit = card.get_suit()

            if card_suit not in check_suit:
                return False
        suit = card.get_suit()
        return suit

    def _check_straight(self):
        self.cards_in_hand.sort()

        # if five-high straight
        values = []
        for i in range(len(self.cards_in_hand)):
            values.insert(0, self.cards_in_hand[i].value)
        if values == [14, 5, 4, 3, 2]:
            return self.cards_in_hand[3].value

        # for rest straights
        for i in range(len(self.cards_in_hand) - 1):
            if self.cards_in_hand[i + 1].value - self.cards_in_hand[i].value != 1:
                return False
        else:
            return self.cards_in_hand[4].value

    def _check_three_of_a_kind(self):
        self.cards_in_hand.sort()
        if self.cards_in_hand[0] == self.cards_in_hand[2]:
            return self.cards_in_hand[0].value
        elif self.cards_in_hand[1] == self.cards_in_hand[3]:
            return self.cards_in_hand[1].value
        elif self.cards_in_hand[2] == self.cards_in_hand[4]:
            return self.cards_in_hand[2].value
        return False

    def _check_two_pair(self):
        card_values = {}
        for i in range(len(self.cards_in_hand)):
            if self.cards_in_hand[i].value not in card_values:
                card_values[self.cards_in_hand[i].value] = 1
            else:
                card_values[self.cards_in_hand[i].value] += 1

        print(card_values)
        pairs = []
        for key, value in card_values.items():
            if value == 2:
                pairs.append(key)
        pairs.sort()
        print(pairs)
        if len(pairs) == 2:
            return pairs[0], pairs[1]
        else:
            return False

    def _check_pair(self):
        values = set()
        for i in range(len(self.cards_in_hand)):
            card = self.cards_in_hand[i]
            card_value = card.get_value()
            if card_value not in values:
                values.add(card_value)
                continue
            else:
                return card.value

        return False

    def _check_high_card(self):

        highest_card = self.cards_in_hand[0]
        for card in self.cards_in_hand:
            if card.value > highest_card.value:
                highest_card = card
        # suit = highest_card.get_suit()
        return highest_card

    def __str__(self):
        result = ""
        for i, card in enumerate(self.cards_in_hand):
            result += f"{i + 1}: {card}, "

        return result[:-2]


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.exchanged_cards = False

    def receive_starting_hand(self, deck):
        for i in range(1, 6):
            card = deck.draw_card()
            self.hand.add_card(card)

    def exchange_card(self, deck):
        if self.exchanged_cards:
            return "Sorry, you can exchange cards only once per game"
        else:
            current_hand = self.hand
            cards_to_change = input(
                f"{current_hand}\nWhich cards would you like to exchange? (Input as xxx, eq. 123 for cards 1, 2 and 3) or 1 for card 1\n: ")

            # Get the indexes to remove
            indexes_to_remove = set()
            for char in cards_to_change:
                if char.isdigit():
                    index = int(char) - 1
                    indexes_to_remove.add(index)

            # Remove cards from highest index to lowest
            sorted_indexes = sorted(indexes_to_remove, reverse=True)
            for i in sorted_indexes:
                self.hand.discard_at_index(i)

            # draw until 5 cards back in hand
            while len(self.hand.cards_in_hand) < 5:
                new_card = deck.draw_card()
                self.hand.add_card(new_card)

            self.exchanged_cards = True

            return f"The new hand is \n{self.hand}"

    def print_hand(self):
        for card in self.hand.cards_in_hand:
            print(card)

    def check_hand(self):
        result = self.hand.check_value()
        print(result)


deck = Deck()
p1 = Player("John")

print("=" * 125)

# sami.receive_starting_hand(deck)
card1 = Card(8, "Hearts")
card2 = Card(8, "Clubs")
card3 = Card(7, "Spades")
card4 = Card(7, "Hearts")
card5 = Card(6, "Diamonds")

p1.hand.cards_in_hand = [card1, card2, card3, card4, card5]
# sami.print_hand()
p1.check_hand()
