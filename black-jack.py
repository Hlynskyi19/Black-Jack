class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def card_value(self):
        """Повертає кількість очок, яке дає карта"""
        if self.rank in "TJQK":
            # По 10 за десятку, валета, даму і короля
            return 10
        else:
            # Повертає відповідне число очок за будь-яку іншу карту
            # Туз спочатку дає одне очко.
            return " A23456789".index(self.rank)

    def get_rank(self):
        return self.rank

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)


class Hand(object):
    def __init__(self, name):
        # ім'я гравця
        self.name = name
        # Спочатку рука порожня
        self.cards = []

    def add_card(self, card):
        """Додає карту до руки"""
        self.cards.append(card)

    def get_value(self):
        """Метод отримання кількості очок на руці"""
        result = 0
        # Кількість тузів на руці.
        aces = 0
        for card in self.cards:
            result += card.card_value()
            # Якщо на руці є туз - збільшуємо кількість тузів
            if card.get_rank() == "A":
                aces += 1
        # Визначаємо, рахувати тузи як 1 або 11 очок
        if result + aces * 10 <= 21:
            result += aces * 10
        return result

    def __str__(self):
        text = "%s має:\n" % self.name
        for card in self.cards:
            text += str(card) + " "
        text += "\nЗначення руки: " + str(self.get_value())
        return text


class Deck(object):
    def __init__(self):
        # ранги карт
        ranks = "23456789TJQKA"
        # масті карт
        suits = "DCHS"
        # генератор списку, що створює колоду з 52 карт
        self.cards = [Card(r, s) for r in ranks for s in suits]
        # перетасовуємо колоду. Не забудьте імпортувати функцію shuffle з модуля random
        shuffle(self.cards)

    def deal_card(self):
        """Функція видачі карти"""
        return self.cards.pop()


def new_game():
    # створюємо колоду
    d = Deck()
    # задаємо "руки" для гравця і дилера
    player_hand = Hand("Гравець")
    dealer_hand = Hand("Дилер")
    # здаємо дві карти гравцеві
    player_hand.add_card(d.deal_card())
    player_hand.add_card(d.deal_card())
    # здаємо одну карту дилеру
    dealer_hand.add_card(d.deal_card())
    print(dealer_hand)
    print("=" * 20)
    print(player_hand)
    # Прапор перевірки необхідності продовжувати гру
    in_game = True
    # Набирати карти гравцеві має сенс лише якщо у нього на руці менше 21 очка
    while player_hand.get_value() < 21:
        ans = input("Взяти ще карту чи зупинитися? (h/s) ")
        if ans == "h":
            player_hand.add_card(d.deal_card())
            print(player_hand)
            # Якщо у гравця перебір - дилеру немає сенсу набирати карти
            if player_hand.get_value() > 21:
                print("Ви програли")
                in_game = False
        else:
            print("Ви зупинилися!")
            break
    print("=" * 20)
    if in_game:
        # За правилами дилер зобов’язаний набирати карти, поки його рахунок менше 17
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(d.deal_card())
            print(dealer_hand)
            # Якщо у дилера перебір, грати далі немає сенсу - гравець виграв
            if dealer_hand.get_value() > 21:
                print("Перебір у дилера")
                in_game = False
    if in_game:
        # Ніхто не має перебору - порівнюємо кількість очок у гравця та дилера.
        # У нашій версії, якщо у дилера та гравця однакова кількість очок - виграє казино
        if player_hand.get_value() > dealer_hand.get_value():
            print("Ви виграли")
        else:
            print("Дилер виграв")
