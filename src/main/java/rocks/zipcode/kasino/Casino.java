package rocks.zipcode.kasino;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// and then you had something like this
//
public class Casino {

    private final Scanner scanner = new Scanner(System.in);

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
        // this would be the main loop
         while (true) {
             System.out.println("Welcome to the casino!");
             System.out.println("1. Play SumTwo"); // how would you add multiple games?
             System.out.println("2. Register a player");
             System.out.println("3. Exit");
             System.out.print("Enter your choice: ");
             String choice = scanner.nextLine();

             switch (choice) {
                 case "1":
                     if (currentPlayer == null) currentPlayer = registerPlayer();
                     GameInterface game = new SumTwo(this, currentPlayer);
                     game.play(); // how would you add multiple games?
                     break;
                 case "2":
                     currentPlayer = registerPlayer();
                     break;
                 case "3":
                     System.out.println("Thank you for playing!");
                     System.exit(0);
                 default:
                     System.out.println("Invalid choice!");
             }
         }
    }

    public static void main(String[] args) {
        new Casino().run();
    }
}
