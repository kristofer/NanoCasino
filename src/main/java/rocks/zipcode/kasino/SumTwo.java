package rocks.zipcode.kasino;

import java.util.HashMap;
import java.util.Map;

import static rocks.zipcode.kasino.SumItUp.BetType.*;

// my game
public class SumTwo implements SumItUp, GameInterface {


    static class SumTwoEnded extends Exception {
        // thrown at the end of the SumTwo game.
    }

    PlayerInterface player;
    Casino theHouse;

    HashMap<BetType, Double> odds = new HashMap<>();

    public SumTwo() {
        odds.put(OVER_SEVEN, 2.0);   // Sum will be greater than 7
        odds.put(UNDER_SEVEN, 2.0);  // Sum will be less than 7
        odds.put(EXACTLY_SEVEN, 3.0); // Sum will be exactly 7
        odds.put(ODD, 1.0); // Sum will be odd
        odds.put(EVEN, 1.0); // Sum will be even
    }

    public SumTwo(Casino house, PlayerInterface p) {
        this();
        this.theHouse = house;
        this.player = p;
    }

    @Override
    public boolean startGame(String playerId) {
        return true;
    }

    @Override
    public boolean placeBet(String playerId, BetType betType, double amount) {
        return false;
    }
    private boolean askForBet() throws SumTwoEnded {
        throw new SumTwoEnded();
        //return true;
    }

    private BetType askForBetType() throws SumTwoEnded {
        return null;
    }
    private Double askForBetAmount() {
        return 0.0;
    }

    @Override
    public int rollDice() {
        return 0;
    }

    @Override
    public boolean isBetWinner(BetType betType, int diceSum) {
        return false;
    }

    @Override
    public double calculatePayout(BetType betType, double betAmount) {
        return 0;
    }

    // with one player, I may NOT NEED this. de-prioritize.
    @Override
    public Map<String, Double> settleBets(int diceSum) {
        return Map.of();
    }

    @Override
    public boolean endGame() {
        return false;
    }

    @Override
    public double getOdds(BetType betType) {
        return 0;
    }

    @Override
    public double getHouseEdge() {
        return 0;
    }

    @Override
    public void play() {
        Boolean playing = true;

        while (playing) {
            try {
                boolean b = askForBet();
                //place bet
                // throw dice
                // win or loose
                // modify the player account
            } catch (SumTwoEnded e) {
                playing = false;
            }
        }
        theHouse.tellUser("Thanks for playing SumTwo!\n");
    }

    @Override
    public void addPlayer(PlayerInterface player) {
        this.player = player;
    }

    @Override
    public void removePlayer(PlayerInterface player) {
        this.player = null;
    }

    @Override
    public boolean isGambling() {
        return true;
    }

    @Override
    public String getName() {
        return "SumTwo";
//        if (player != null) {
//            return player.getName();
//        }
//        return "No Player";
    }
}
