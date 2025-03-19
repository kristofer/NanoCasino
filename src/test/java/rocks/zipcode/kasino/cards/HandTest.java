package rocks.zipcode.kasino.cards;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.mock;





class HandTest {
    private Hand hand;
    private Card mockCard1;
    private Card mockCard2;

    @BeforeEach
    void setUp() {
        hand = new Hand();
        mockCard1 = mock(Card.class);
        mockCard2 = mock(Card.class);
    }

    @Test
    void testAdd() {
        hand.add(mockCard1);
        assertEquals(1, hand.size());
        hand.add(mockCard2);
        assertEquals(2, hand.size());
    }

    @Test
    void testGetAt() {
        hand.add(mockCard1);
        hand.add(mockCard2);
        Card removedCard = hand.getAt(0);
        assertEquals(mockCard1, removedCard);
        assertEquals(1, hand.size());
    }

    @Test
    void testSize() {
        assertEquals(0, hand.size());
        hand.add(mockCard1);
        assertEquals(1, hand.size());
        hand.add(mockCard2);
        assertEquals(2, hand.size());
    }

    @Test
    void testPop() {
        assertNull(hand.pop());
        hand.add(mockCard1);
        hand.add(mockCard2);
        Card poppedCard = hand.pop();
        assertEquals(mockCard1, poppedCard);
        assertEquals(1, hand.size());
    }
}