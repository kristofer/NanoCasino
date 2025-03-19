package rocks.zipcode.kasino.cards;

import java.util.ArrayList;
import java.util.List;

public class Hand {
    private final List<Card> cards;

    public Hand() {
        cards = new ArrayList<>();
    }

    public Card getAt(int n) {
        return cards.remove(n);
    }
    public void add(Card c) {
        cards.add(c);
    }
    public int size() {
        return cards.size();
    }
    public Card pop() {
        if (cards.isEmpty() == false) {
            return cards.remove(0);
        } else {
            return null;
        }
    }

    public int getSumOfCards() {
        int sum = 0;
        for (Card c : cards) {
            sum += c.cardValue(c);
        }
        return sum;
    }

    public String showHand() {
        StringBuilder sb = new StringBuilder();
        for (Card c : cards) {
            sb.append(c.toString());
            sb.append("; ");
        }
        return sb.toString();
     }

    public void clear() {
        cards.clear();
    }
}
