package rocks.zipcode.kasino;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

import rocks.zipcode.kasino.SumItUp.BetType;

public class SumTwoTest {
    @Test
    void testCalculatePayout() {

    }

    @Test
    void testGetOdds() {
        SumTwo sumTwo = new SumTwo(new Casino(), new SimplePlayer("playerOne"));
        int[] odds = {0,0,0,0,0}; 
        odds[0] = (int) sumTwo.calculatePayout(BetType.EVEN, 1.0);
        odds[1] = (int) sumTwo.calculatePayout(BetType.ODD, 1.0);
        odds[2] = (int) sumTwo.calculatePayout(BetType.OVER_SEVEN, 1.0);
        odds[3] = (int) sumTwo.calculatePayout(BetType.UNDER_SEVEN, 1.0);
        odds[4] = (int) sumTwo.calculatePayout(BetType.EXACTLY_SEVEN, 1.0);

        int[] expected = {1,1,2,2,3};
        for (int i = 0; i < odds.length; i++) {
            assertEquals(expected[i],odds[i]);
        }


    }

    @Test
    void testIsBetWinner() {
        SumTwo sumTwo = new SumTwo(new Casino(), new SimplePlayer("playerOne"));
        int testint = 7;
        boolean[] expected = {false,true,false,false,true};
        boolean[] win = {false,false,false,false,false};
        win[0] = sumTwo.isBetWinner(BetType.EVEN, testint);
        win[1] = sumTwo.isBetWinner(BetType.ODD, testint);
        win[2] = sumTwo.isBetWinner(BetType.OVER_SEVEN, testint);
        win[3] = sumTwo.isBetWinner(BetType.UNDER_SEVEN, testint);
        win[4] = sumTwo.isBetWinner(BetType.EXACTLY_SEVEN, testint);
        for (int i = 0; i < win.length; i++) {
            assertEquals(expected[i],win[i]);
        }

    }

    @Test
    void testRollDice() {
        SumTwo sumTwo = new SumTwo(new Casino(), new SimplePlayer("playerOne"));
        int[] test = {0,0,0,0,0,0,0,0,0,0,0};
        for (int i = 0; i < 1000; i++) {
            int roll = sumTwo.rollDice();
            test[roll-2]++;
        }
        for (int idx = 0; idx < test.length; idx++) {
            System.out.println("Test: " + test[idx]);
        }
        // for (int i = 0; i < test.length; i++) {
        assertEquals(166,test[6], 1);
        // }
    }
}
