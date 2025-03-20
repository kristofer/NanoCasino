package rocks.zipcode.kasino;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import static rocks.zipcode.kasino.SumItUp.BetType.EVEN;
import static rocks.zipcode.kasino.SumItUp.BetType.EXACTLY_SEVEN;
import static rocks.zipcode.kasino.SumItUp.BetType.ODD;
import static rocks.zipcode.kasino.SumItUp.BetType.OVER_SEVEN;
import static rocks.zipcode.kasino.SumItUp.BetType.UNDER_SEVEN;

// my game
public class SumTwo implements SumItUp, GameInterface {


    static class SumTwoEnded extends Exception {
        // thrown at the end of the SumTwo game.
    }

    PlayerInterface player;
    Casino theHouse;
    Random random = new Random();

    HashMap<BetType, Double> odds = new HashMap<>();

    // this will need to be abstracted for multiple players
    HashMap<BetType, Double> currentBets = new HashMap<>();

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
        currentBets.put(betType, amount);
        return true;
    }

    private boolean askForBet() throws SumTwoEnded {
        BetType bet = this.askForBetType();
        Double amt = this.askForBetAmount();
        return placeBet(player.getName(), bet, amt);        //return true;
    }

    private BetType askForBetType() throws SumTwoEnded {
        while (true) {
            theHouse.tellUser("Place a bet on one of the following:");
            theHouse.tellUser("1. Even");
            theHouse.tellUser("2. Odd");
            theHouse.tellUser("3. Exactly 7:0");
            theHouse.tellUser("4. Over 7");
            theHouse.tellUser("5. Under 7");
            String answer = theHouse.promptUser("Enter your choice: ");
            switch (answer) {
                case "1":
                    return EVEN;
                case "2":
                    return ODD;
                case "3":
                    return EXACTLY_SEVEN;
                case "4":
                    return OVER_SEVEN;
                case "5":
                    return UNDER_SEVEN;
                case "quit":
                    throw new SumTwoEnded();
            }
            theHouse.tellUser("Invalid choice. Please try again.");
        }   
    }
    private Double askForBetAmount() {
        while (true) {
            String answer = theHouse.promptUser("Enter your bet amount: ");
            try {
                Double amt = Double.parseDouble(answer);
                if (amt > 0) {
                    if (player.getAccount().getBalance() < amt) {
                        theHouse.tellUser("Insufficient funds. Please try again.");
                    } else {
                        return amt;
                    }
                }
            } catch (NumberFormatException e) {
                theHouse.tellUser("Invalid amount. Please try again.");
            }
        }
    }

    private int RollOne() {
        return random.nextInt(6) + 1;
    }
    @Override
    public int rollDice() {
        int die1 = this.RollOne();
        int die2 = this.RollOne();
        return die1 + die2;
    }

    @Override
    public boolean isBetWinner(BetType betType, int diceSum) {
        if (betType == EVEN && diceSum % 2 == 0) return true;
        if (betType == ODD && diceSum % 2 == 1) return true;
        if (betType == EXACTLY_SEVEN && diceSum == 7) return true;
        if (betType == UNDER_SEVEN && diceSum < 7) return true;
        if (betType == OVER_SEVEN && diceSum > 7) return true;
        return false;
    }

    @Override
    public double calculatePayout(BetType betType, double betAmount) {
        /* well, working on this block, when I finished the first one... */
//        if (betType == EVEN) return this.getOdds(EVEN) * betAmount;
//        if (betType == ODD) return true;
//        if (betType == EXACTLY_SEVEN) return true;
//        if (betType == UNDER_SEVEN) return true;
//        if (betType == OVER_SEVEN) return true;

        /* much better soln */
        return this.getOdds(betType) * betAmount;
    }

    // with one player, I may NOT NEED this. de-prioritize.
    @Override
    public Map<String, Double> settleBets(int diceSum) {
        return Map.of();
    }

    private Double totalBetAdjust(int diceSum) {
        Double totalAdjust = 0.0;
        for (Map.Entry<BetType, Double> entry : currentBets.entrySet()) {
                BetType bt = entry.getKey();
                Double bet = entry.getValue();
                if (this.isBetWinner(bt, diceSum)) {
                    totalAdjust += this.calculatePayout(bt, bet);
                } else {
                    totalAdjust -= bet;
                }
        }
        theHouse.tellUser("You won/lost");
        theHouse.tellUser(String.format("%.2f dollars", totalAdjust));
        return totalAdjust;
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
                //boolean b = askForBet();
                /* for now, place a simple bet each time */
                boolean betok = askForBet();
                if (!betok) {
                    throw new SumTwoEnded();
                }
                // throw dice
                int rollResult = this.rollDice();
                theHouse.tellUser("The roll was "+rollResult);
                // win or lose
                Double netWinLoss = this.totalBetAdjust(rollResult);
                // modify the player account
                player.getAccount().deposit(netWinLoss);
                // clear the bets
                currentBets.clear();

                String answer = theHouse.promptUser("Roll again? ");
                if (answer.equals("no")) {
                    throw new SumTwoEnded();
                }
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
