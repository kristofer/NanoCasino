package rocks.zipcode.kasino;
/**
 * Interface for the Sum It Up dice game in a casino simulation.
 * This game involves players betting on outcomes of rolling two dice.
 */
public interface SumItUp {

    /**
     * Enum representing different betting options for Sum It Up.
     */
    enum BetType {
        OVER_SEVEN,   // Sum will be greater than 7
        UNDER_SEVEN,  // Sum will be less than 7
        EXACTLY_SEVEN, // Sum will be exactly 7
        ODD,          // Sum will be odd
        EVEN          // Sum will be even
    }

    /**
     * Start a new game with the specified player.
     *
     * @param playerId The unique identifier for the player
     * @return true if the game was successfully started, false otherwise
     */
    boolean startGame(String playerId);

    /**
     * Places a bet for a player on a specific outcome.
     *
     * @param playerId The unique identifier for the player
     * @param betType The type of bet (OVER_SEVEN, UNDER_SEVEN, etc.)
     * @param amount The amount of money being bet
     * @return true if the bet was successfully placed, false otherwise
     */
    boolean placeBet(String playerId, BetType betType, double amount);

    /**
     * Roll the dice and determine the outcome of the game.
     * This method should use the Dice interface's roll method.
     *
     * @return The sum of the two dice
     */
    int rollDice();

    /**
     * Determines if a bet is a winner based on the dice roll outcome.
     *
     * @param betType The type of bet placed
     * @param diceSum The sum of the dice roll
     * @return true if the bet wins, false otherwise
     */
    boolean isBetWinner(BetType betType, int diceSum);

    /**
     * Calculate the payout amount for a winning bet.
     * Different bet types may have different payout ratios.
     *
     * @param betType The type of bet placed
     * @param betAmount The amount that was bet
     * @return The amount to be paid out (including the original bet)
     */
    double calculatePayout(BetType betType, double betAmount);

    /**
     * Settle all bets after the dice have been rolled.
     * This should update player wallets accordingly.
     *
     * @param diceSum The sum of the dice roll
     * @return A map of player IDs to their winnings (negative for losses)
     */
    java.util.Map<String, Double> settleBets(int diceSum);

    /**
     * End the current game and perform any necessary cleanup.
     *
     * @return true if the game was successfully ended, false otherwise
     */
    boolean endGame();

    /**
     * Get the odds for a specific bet type.
     *
     * @param betType The type of bet
     * @return The payout multiplier for the bet (e.g., 1.0 means 1:1 odds)
     */
    double getOdds(BetType betType);

    /**
     * Get the house edge for this game.
     *
     * @return The house edge as a percentage
     */
    double getHouseEdge();
}