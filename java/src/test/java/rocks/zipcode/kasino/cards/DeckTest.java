package rocks.zipcode.kasino.cards;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;




public class DeckTest {
    private Deck deck;

    @BeforeEach
    public void setUp() {
        deck = new Deck();
    }

    @Test
    public void testDeckInitialization() {
        // A standard deck should have 52 cards
        assertEquals(52, deck.size(), "Deck should contain 52 cards after initialization.");
    }

    @Test
    public void testShuffle() {
        Deck unshuffledDeck = new Deck();
        deck.shuffle();
        // Since shuffle is random, we can't guarantee order, but size should remain the same
        assertEquals(52, deck.size(), "Deck size should remain 52 after shuffling.");
        assertNotEquals(unshuffledDeck.drawCard(), deck.drawCard(), "Shuffled deck should have a different order.");
    }

    @Test
    public void testDrawCard() {
        int initialSize = deck.size();
        Card drawnCard = deck.drawCard();
        assertNotNull(drawnCard, "Drawn card should not be null.");
        assertEquals(initialSize - 1, deck.size(), "Deck size should decrease by 1 after drawing a card.");
    }

    @Test
    public void testDrawCardUntilEmpty() {
        while (deck.size() > 0) {
            deck.drawCard();
        }
        assertEquals(0, deck.size(), "Deck size should be 0 after drawing all cards.");
        assertThrows(IllegalStateException.class, deck::drawCard, "Drawing from an empty deck should throw an exception.");
    }

    @Test
    public void testDeckSize() {
        assertEquals(52, deck.size(), "Deck size should be 52 after initialization.");
        deck.drawCard();
        assertEquals(51, deck.size(), "Deck size should decrease to 51 after drawing one card.");
    }
}