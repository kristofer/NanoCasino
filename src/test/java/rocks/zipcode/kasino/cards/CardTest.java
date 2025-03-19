package rocks.zipcode.kasino.cards;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;


class CardTest {

    @Test
    void testCardConstructor() {
        Card card = new Card(Card.Rank.ACE, Card.Suit.SPADES);
        assertEquals(Card.Rank.ACE, card.rank);
        assertEquals(Card.Suit.SPADES, card.suit);
    }

    @Test
    void testToString() {
        Card card = new Card(Card.Rank.KING, Card.Suit.HEARTS);
        assertEquals("HEARTS of KING", card.toString());
    }

    @Test
    void testAllRanks() {
        for (Card.Rank rank : Card.Rank.values()) {
            assertNotNull(rank);
        }
    }

    @Test
    void testAllSuits() {
        for (Card.Suit suit : Card.Suit.values()) {
            assertNotNull(suit);
        }
    }
}