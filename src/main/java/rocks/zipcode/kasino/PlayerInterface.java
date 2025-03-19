package rocks.zipcode.kasino;

public interface PlayerInterface {
    String getName();
    Wallet getAccount();
    void setAccount(Wallet account);
    String getIdent();
    // Additional methods for player functionality
}
