package rocks.zipcode.kasino;

public class CoinFlip implements GameInterface {
    private final Casino theHouse;
    private final PlayerInterface player;

    public CoinFlip(Casino theHouse, PlayerInterface player) {
        this.theHouse = theHouse;
        this.player = player;
    }

    public void play() {
        introduceGame();
        while (true) {
            // flip the coin
            boolean heads = flipCoin();
            theHouse.tellUser("Flipping the coin...");
            theHouse.wasteTime(3);
            theHouse.tellUser("The coin landed on " + (heads ? "HEADS" : "TAILS"));
            // declare the winner
            if (heads) {
                theHouse.tellUser("You win!");
            } else {
                theHouse.tellUser("The dealer wins!");
            }
            // do you want to play again?
            if (!playAgain()) {
                break;
            }
        }
    }

    boolean flipCoin() {
        return Math.random() < 0.5;
    }

    private boolean playAgain() {
        return theHouse.promptUser("Do you want to play again? (yes or no): ").equalsIgnoreCase("yes");
    }

    private void introduceGame() {
        theHouse.tellUser("Welcome to CoinFlip\n");
        theHouse.tellUser("The dealer will flip a coin.\n");
        theHouse.tellUser("You win if the coin lands on heads.\n");
        theHouse.tellUser("Good luck!\n\n");

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
        return false;
    }


    @Override
    public String getName() {
        return "CoinFlip";
    }
    
}
