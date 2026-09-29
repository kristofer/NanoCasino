package rocks.zipcode.kasino;

// just from the readme, this is kind of thing you'll need to implement
//
public interface GameInterface {
    void play();
    void addPlayer(PlayerInterface player);
    void removePlayer(PlayerInterface player);
    boolean isGambling();
    String getName();
    // Additional methods for game functionality
}
