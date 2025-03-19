package rocks.zipcode.kasino;

public interface PlayerInterface {
    String getName();
    CasinoAccount getAccount();
    void setAccount(CasinoAccount account);
    String getIdent();
    // Additional methods for player functionality
}
