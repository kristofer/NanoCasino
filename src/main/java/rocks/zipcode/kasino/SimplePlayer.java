package rocks.zipcode.kasino;

public class SimplePlayer implements PlayerInterface{
    String name = "";
    CasinoAccount wallet;

    public SimplePlayer(String name) {
        name = name;
        wallet = new CasinoAccount(500.0, name);
    }
    @Override
    public String getName() {
        return this.name;
    }

    @Override
    public CasinoAccount getAccount() {
        return this.wallet;
    }

    @Override
    public void setAccount(CasinoAccount account) {
        this.wallet = account;
    }

    @Override
    public String getIdent() {
        return this.name;
    }
}
