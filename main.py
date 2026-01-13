# five-card-draw Poker.
import random
import time
from collections import Counter


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
        for suit_num in Deck.number_to_suit:
            for value_num in Card.value_to_rank:
                card = Card(value_num, Deck.number_to_suit[suit_num])
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

    def get_hand_key_values(self):
        card_values = {}
        for i in range(len(self.cards_in_hand)):
            if self.cards_in_hand[i].value not in card_values:
                card_values[self.cards_in_hand[i].value] = 1
            else:
                card_values[self.cards_in_hand[i].value] += 1
        return card_values

    def check_value(self):
        cards = [card for card in self.cards_in_hand]
        cards.sort()

        if royal_flush := self._check_royal_flush(cards):
            msg = f"Royal flush! {Card.value_to_rank[royal_flush[1]]}-high royal flush, {royal_flush[0]}"
            return msg

        elif straight_flush := self._check_straight_flush(cards):
            msg = f"Straight flush! {Card.value_to_rank[straight_flush[1]]}-high straight flush, {straight_flush[0]}"
            return msg

        elif four_of_a_kind := self._check_four_of_a_kind(cards):
            msg = f"Four of a kind! {Card.value_to_rank[four_of_a_kind]}s"
            return msg

        elif full_house := self._check_full_house(cards):
            msg = f"Full House. {Card.value_to_rank[full_house[0]]}s full of {Card.value_to_rank[full_house[1]]}s"
            return msg

        elif flush := self._check_flush(cards):
            msg = f"Flush of {flush}"
            return msg

        elif straight := self._check_straight(cards):
            msg = f"{straight} high straight"
            return msg

        elif three_of_a_kind := self._check_three_of_a_kind(cards):
            msg = f"Three of kind, {Card.value_to_rank[three_of_a_kind]}'s"
            return msg

        elif two_pair := self._check_two_pair(cards):
            msg = f"Two pairs, {Card.value_to_rank[two_pair[1]]}'s and {Card.value_to_rank[two_pair[0]]}'s"
            return msg

        elif pair := self._check_pair(cards):
            msg = f"Pair of {Card.value_to_rank[pair]}s"
            return msg
        else:
            high_card = self._check_high_card(cards)
            high_card_rank = Card.value_to_rank[high_card.value]
            high_card_suit = high_card.get_suit()
            msg = f"High card, {high_card_rank} of {high_card_suit}"
            return msg

    @staticmethod
    def _check_royal_flush(cards):

        values = [c.value for c in cards]
        if values != [10,11,12,13,14]:
            return False
        flush_suit = Hand._check_flush(cards)

        if flush_suit:
            return flush_suit, values[-1]

        return False

    @staticmethod
    def _check_straight_flush(cards):
        flush_suit = Hand._check_flush(cards)
        straight_high_card = Hand._check_straight(cards)
        if flush_suit and straight_high_card:
            return flush_suit, straight_high_card

        return False


    @staticmethod
    def _check_four_of_a_kind(cards):
        values = [card.value for card in cards]
        value_count = Counter(values)

        if 4 in value_count.values():
            four_cards = max(value_count, key=value_count.get)
            return four_cards
        return False

    @staticmethod
    def _check_full_house(cards):
        values = [card.value for card in cards]
        value_count = Counter(values)

        if sorted(value_count.values()) == [2, 3]:
            three = max(value_count, key=value_count.get)
            pair = min(value_count, key=value_count.get)
            return three, pair
        return False

    @staticmethod
    def _check_flush(cards):
        check_suit = []
        card = cards[0]
        card_suit = card.get_suit()
        check_suit.append(card_suit)

        for i in range(1, len(cards)):
            card = cards[i]
            card_suit = card.get_suit()

            if card_suit not in check_suit:
                return False
        suit = card.get_suit()
        return suit

    @staticmethod
    def _check_straight(cards):

        # For 5 high straights
        values = [c.value for c in cards]
        if values == [2,3,4,5,14]:
            return 5

        # for rest straights
        for i in range(len(cards) - 1):
            if cards[i + 1].value - cards[i].value != 1:
                return False
        else:
            return cards[4].value

    @staticmethod
    def _check_three_of_a_kind(cards):
        values = [card.value for card in cards]
        value_count = Counter(values)

        if 3 in value_count.values():
            three_cards = max(value_count, key=value_count.get)
            return three_cards
        return False

    @staticmethod
    def _check_two_pair(cards):
        values = [card.value for card in cards]
        value_count = Counter(values)

        pairs = []
        for key, value in value_count.items():
            if value == 2:
                pairs.append(key)
        pairs.sort()
        if len(pairs) == 2:
            pairs.sort()
            return pairs[0], pairs[1]
        else:
            return False

    @staticmethod
    def _check_pair(cards):
        values = set()
        for i in range(len(cards)):
            card = cards[i]
            card_value = card.get_value()
            if card_value not in values:
                values.add(card_value)
                continue
            else:
                return card.value
        return False

    @staticmethod
    def _check_high_card(cards):
        return cards[-1]

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
            print("Drawing card....")
            time.sleep(0.5)
            print(f"Card drawn {card}")
            self.hand.add_card(card)

        starting_hand = self.get_hand()
        hand_string = ", ".join(map(str, starting_hand))

        print(f"You starting hand is \n{hand_string}")

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
            print(card, end=", ")

    def get_hand(self):
        hand = []
        for card in self.hand.cards_in_hand:
            hand.append(card)

        return hand

    def check_hand(self):
        result = self.hand.check_value()
        return result


deck = Deck()
p1 = Player("John")

print("=" * 125)

#p1.receive_starting_hand(deck)
card1 = Card(14, "Hearts")
card2 = Card(13, "Hearts")
card3 = Card(12, "Hearts")
card4 = Card(11, "Hearts")
card5 = Card(10, "Hearts")

p1.hand.cards_in_hand = [card1, card2, card3, card4, card5]
# sami.print_hand()
print(p1.check_hand())
