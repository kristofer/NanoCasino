package rocks.zipcode.kasino;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class CoinFlipTest {

    @Test
    void testFlipCoin() {
        CoinFlip coinFlip = new CoinFlip(new Casino(), new SimplePlayer("playerOne"));
        int n = 1_000_000;
        int heads = 0;
        int tails = 0;
        for (int i = 0; i < n; i++) {
            if (coinFlip.flipCoin()) {
                heads++;
            } else {
                tails++;
            }
        }
        System.out.println("heads: " + heads);
        System.out.println("tails: " + tails);
        System.out.println("heads + tails: " + (heads + tails));
        int gap = Math.abs(heads - tails);
        System.out.println("gap: " + gap);
        assertEquals(heads, tails, n / 100);
        
    }
}
