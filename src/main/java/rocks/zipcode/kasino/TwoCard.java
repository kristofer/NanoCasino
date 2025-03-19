package rocks.zipcode.kasino;

import rocks.zipcode.kasino.cards.Deck;
import rocks.zipcode.kasino.cards.Hand;

// the dealer is the house.
// at the atrt of the game, the dealer deals two cards to the player and two cards to the house.
// the player can see both of the house cards.
// the player can see both of their own cards.
// the player wins if the sum of the player's two cards is higher than the dum of the dealer's two cards.
public class TwoCard implements GameInterface {
    

    private Hand playerhand;
    private Hand dealerhand;
    private Casino theHouse;
    private PlayerInterface player;
    private Deck deck;
        
    public TwoCard(Casino theHouse, PlayerInterface player) {
        this.theHouse = theHouse;
        this.player = player;
        this.playerhand = new Hand();
        this.dealerhand = new Hand();
        this.deck = new Deck();
        this.deck.shuffle();
    }

    public void play() {
        // welcome to TwoCard
        // the dealer will deal two cards to you and two cards to the house.
        // you can see both of the house cards.
        // you can see both of your own cards.
        // you win if the sum of your two cards is higher than the sum of the dealer's two cards.
        // good luck!
        while (true) {
            deal();
            // show the player their cards
            theHouse.tellUser("Your Hand: ["+playerhand.showHand()+"]");
            theHouse.tellUser("Dealer   : ["+dealerhand.showHand()+"]");
            // show the player the sum of their cards
            theHouse.tellUser("Your sum is: " + playerhand.getSumOfCards());
            // show the player the sum of the dealer's cards
            theHouse.tellUser("The dealer's sum is: " + dealerhand.getSumOfCards());
            // declare the winner or a tie
            if (playerWins(playerhand, dealerhand)) {
                theHouse.tellUser("You win!");
            } else if (dealerWins(playerhand, dealerhand)) {
                theHouse.tellUser("The dealer wins!");
            } else {
                theHouse.tellUser("It's a tie!");
            }
            // do you want to play again?
            if (!playAgain()) {
                break;
            }
            playerhand.clear();
            dealerhand.clear();
            
        }
    }

    public boolean playerWins(Hand playerhand, Hand dealerhand) {
        return playerhand.getSumOfCards() > dealerhand.getSumOfCards();
    }
    public boolean dealerWins(Hand playerhand, Hand dealerhand) {
        return playerhand.getSumOfCards() < dealerhand.getSumOfCards();
    }

    private void deal() {
        playerhand.add(deck.drawCard());
        playerhand.add(deck.drawCard());
        dealerhand.add(deck.drawCard());
        dealerhand.add(deck.drawCard());
    }

    private boolean playAgain() {
        String resp = theHouse.promptUser("Do you wish to play again? (yes or no)");
        return resp.equalsIgnoreCase("yes");
    }

    @Override
    public void addPlayer(PlayerInterface player) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'addPlayer'");
    }

    @Override
    public void removePlayer(PlayerInterface player) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'removePlayer'");
    }

    @Override
    public boolean isGambling() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'isGambling'");
    }

    @Override
    public String getName() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getName'");
    }

}
