package rocks.zipcode.kasino.cards;

public class Card {

    public enum Rank {
        ACE,
        TWO,
        THREE,
        FOUR,
        FIVE,
        SIX,
        SEVEN,
        EIGHT,
        NINE,
        TEN,
        JACK,
        QUEEN,
        KING;
    }

    public enum Suit {
        CLUBS,
        SPADES,
        HEARTS,
        DIAMONDS;
    }

    final public Rank rank;
    final public Suit suit;

    public Card (final Rank rank, final Suit suit) {
        this.rank = rank;
        this.suit = suit;
    }

    @Override
    public String toString(){
        return rank.name()+ " of " +suit.name();
    }

    public String toCard() {
        int baseCodePoint;
    
        // Determine the base code point for the suit
        switch (suit) {
            case SPADES -> baseCodePoint = 0x1F0A0; // Spades
            case HEARTS -> baseCodePoint = 0x1F0B0; // Hearts
            case DIAMONDS -> baseCodePoint = 0x1F0C0; // Diamonds
            case CLUBS -> baseCodePoint = 0x1F0D0; // Clubs
            default -> throw new IllegalStateException("Unexpected suit: " + suit);
        }
    
        // Add the rank offset
        int rankOffset = switch (rank) {
            case ACE -> 1;
            case TWO -> 2;
            case THREE -> 3;
            case FOUR -> 4;
            case FIVE -> 5;
            case SIX -> 6;
            case SEVEN -> 7;
            case EIGHT -> 8;
            case NINE -> 9;
            case TEN -> 10;
            case JACK -> 11;
            case QUEEN -> 13;
            case KING -> 14;
            default -> throw new IllegalStateException("Unexpected rank: " + rank);
        };
    
        // Combine base code point and rank offset
        int codePoint = baseCodePoint + rankOffset;
    
        // Return the Unicode character as a string
        return new String(Character.toChars(codePoint));
    } 

    // very interesting new switch expression!
    public int cardValue(Card c) {
        return switch (c.rank) {
            case ACE -> 1;
            case TWO -> 2;
            case THREE -> 3;
            case FOUR -> 4;
            case FIVE -> 5;
            case SIX -> 6;
            case SEVEN -> 7;
            case EIGHT -> 8;
            case NINE -> 9;
            case TEN -> 10;
            case JACK -> 10;
            case QUEEN -> 10;
            case KING -> 10;
            default -> 0;
        };
    }
}

