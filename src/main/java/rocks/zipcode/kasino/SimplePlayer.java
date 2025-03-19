package rocks.zipcode.kasino;

public class SimplePlayer implements PlayerInterface{
    String name = "PlayerOne";
    Wallet wallet = null;

    public SimplePlayer(String name) {
        name = name;
        wallet = new Wallet(500.0, name);
    }
    @Override
    public String getName() {
        return this.name;
    }

    @Override
    public Wallet getAccount() {
        return this.wallet;
    }

    @Override
    public void setAccount(Wallet account) {
        this.wallet = account;
    }

    @Override
    public String getIdent() {
        return this.name;
    }
}
