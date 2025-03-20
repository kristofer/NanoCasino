package rocks.zipcode.kasino;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// and then you had something like this
//
public class Casino {

    private final Scanner scanner = new Scanner(System.in);

    // I only have One game for this version
    private final List<GameInterface> availableGames;
    private final List<PlayerInterface> registeredPlayers;

    public Casino() {
        this.availableGames = new ArrayList<>();
        this.registeredPlayers = new ArrayList<>();
    }

    public void addGame(GameInterface game) {
        availableGames.add(game);
    }

    public void registerPlayer(PlayerInterface player) {
        registeredPlayers.add(player);
    }

    public List<GameInterface> getAvailableGames() {
        return availableGames;
    }

    public String promptUser(String message) {
        System.out.println(message);
        return scanner.nextLine();
    }
    public void tellUser(String message) {
        System.out.println(message);
    }
    public void wasteTime(int secs) {
        long durationMillis = secs * 1000;
        char[] twirl = {'/', '-', '\\', '|'};
        long endTime = System.currentTimeMillis() + durationMillis;
    
        int idx = 0;
        while (System.currentTimeMillis() < endTime) {
            System.out.print("\r" + twirl[idx]); // \r moves the cursor back to the start of the line
            idx = (idx + 1) % twirl.length; // Cycle through the twirl array
            try {
                Thread.sleep(100); // Adjust delay for speed (100ms per frame)
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); // Restore interrupted status
                break;
            }
        }
        System.out.print("\r \n"); // Clear the line after animation
            // try {
        //     for (int idx = secs; idx > 0; idx--) {
        //         System.out.print("\\");
        //         Thread.sleep(300);
        //         System.out.print("|");
        //         Thread.sleep(300);
        //         System.out.print("/");
        //         Thread.sleep(300);
        //     }
        //     System.out.println();
        // } catch (InterruptedException e) {
        //     e.printStackTrace();
        // }
    }

    public PlayerInterface registerPlayer() {
        String user = promptUser("What is your name? ");
        tellUser("Hello "+user);
        PlayerInterface newPlayer = new SimplePlayer(user);
        this.registerPlayer(newPlayer);
        return newPlayer;
    }

    public void run() {
        // Main casino interface logic
        // Make this is the only place where I/O to the user happens
        PlayerInterface currentPlayer = null;
        GameInterface game = null;

        // this would be the main loop
         while (true) {
             System.out.println("Welcome to the casino!");
             System.out.println("1. Register a player");
             System.out.println("2. Play SumTwo"); // how would you add multiple games?
             System.out.println("3. Play TwoCardStud"); // how would you add multiple games?
             System.out.println("4. Play CoinFlip"); // how would you add multiple games?
             System.out.println("5. Exit");
             System.out.print("Enter your choice: ");
             String choice = scanner.nextLine();

             switch (choice) {
                 case "2":
                     if (currentPlayer == null) currentPlayer = registerPlayer();
                     game = new SumTwo(this, currentPlayer);
                     game.play(); // how would you add multiple games?
                     break;
                case "3":
                     if (currentPlayer == null) currentPlayer = registerPlayer();
                     game = new TwoCard(this, currentPlayer);
                     game.play(); // how would you add multiple games?
                     break;
                case "4":
                     if (currentPlayer == null) currentPlayer = registerPlayer();
                     game = new CoinFlip(this, currentPlayer);
                     game.play(); // how would you add multiple games?
                     break;
                 case "1":
                     currentPlayer = registerPlayer();
                     break;
                 case "5":
                     System.out.println("Thank you for playing!");
                     System.exit(0);
                 default:
                     System.out.println("Invalid choice!");
             }
         }
    }

    // this is a simolest interactive test for this class. Not used for the real 'project'
    public static void main(String[] args) {
        new Casino().run();
    }
}
