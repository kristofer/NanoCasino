package rocks.zipcode.kasino;

public class Wallet {

    private double balance;
    private String accountId;

    public Wallet(double initialBalance, String accountId) {
        this.balance = initialBalance;
        this.accountId = accountId;
    }

    public double getBalance() {
        return balance;
    }

    public String balanceString() {
        // return string of balance in dollars and cents
        return String.format("$%.2f", this.balance);
    }

    public void deposit(double amount) {
        this.balance += amount;
    }

    public boolean withdraw(double amount) {
        if (balance >= amount) {
            balance -= amount;
            return true;
        }
        return false;
    }

    public String getAccountId() {
        return accountId;
    }
}
