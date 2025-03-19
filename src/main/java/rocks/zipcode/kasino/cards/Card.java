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
        KING;}

    public enum Suit {
        CLUBS,
        SPADES,
        HEARTS,
        DIAMONDS;}

    final Rank rank;
    final Suit suit;

    public Card (final Rank rank, final Suit suit) {
        this.rank = rank;
        this.suit = suit;
    }

    @Override
    public String toString(){
        return suit.name()+ " of " +rank.name();
    }
}

