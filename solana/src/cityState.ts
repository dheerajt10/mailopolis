import { Connection, PublicKey, Keypair, Transaction, SystemProgram, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { CityState } from './types';
import { getWalletKeypair } from './config';

export class CityStateProgram {
  private connection: Connection;
  private cityAccount: Keypair;
  private wallet: Keypair;

  constructor() {
    this.connection = new Connection('https://api.devnet.solana.com', 'confirmed');
    this.wallet = getWalletKeypair();
    this.cityAccount = Keypair.generate();
  }

  async initializeCity(initialBudget: number): Promise<string> {
    try {
      // Create account for city budget
      const createAccountIx = SystemProgram.createAccount({
        fromPubkey: this.wallet.publicKey,
        newAccountPubkey: this.cityAccount.publicKey,
        lamports: LAMPORTS_PER_SOL * 0.01, // Rent for account
        space: 8 + 8, // 8 bytes discriminator + 8 bytes for budget
        programId: SystemProgram.programId,
      });

      // Transfer initial budget to city account
      const transferIx = SystemProgram.transfer({
        fromPubkey: this.wallet.publicKey,
        toPubkey: this.cityAccount.publicKey,
        lamports: initialBudget * LAMPORTS_PER_SOL,
      });

      const transaction = new Transaction();
      transaction.add(createAccountIx);
      transaction.add(transferIx);
      const latestBlockhash = await this.connection.getLatestBlockhash();
      transaction.recentBlockhash = latestBlockhash.blockhash;
      transaction.feePayer = this.wallet.publicKey;
      
      transaction.sign(this.wallet, this.cityAccount);
      const rawTransaction = transaction.serialize();
      const signature = await this.connection.sendRawTransaction(rawTransaction);
      await this.connection.confirmTransaction({
        signature,
        blockhash: latestBlockhash.blockhash,
        lastValidBlockHeight: latestBlockhash.lastValidBlockHeight
      }, 'confirmed');

      console.log(`City initialized with budget: ${initialBudget} SOL`);
      console.log(`City Account: ${this.cityAccount.publicKey.toString()}`);
      console.log(`Transaction: ${signature}`);

      return signature;
    } catch (error) {
      console.error('Error initializing city:', error);
      throw error;
    }
  }

  async updateBudget(newBudget: number): Promise<string> {
    try {
      const currentBalance = await this.connection.getBalance(this.cityAccount.publicKey);
      const targetBalance = newBudget * LAMPORTS_PER_SOL;
      const difference = targetBalance - currentBalance;

      if (difference !== 0) {
        const transaction = new Transaction();
        
        if (difference > 0) {
          // Add funds to city account
          transaction.add(
            SystemProgram.transfer({
              fromPubkey: this.wallet.publicKey,
              toPubkey: this.cityAccount.publicKey,
              lamports: difference,
            })
          );
        } else {
          // Remove funds from city account (send back to wallet)
          transaction.add(
            SystemProgram.transfer({
              fromPubkey: this.cityAccount.publicKey,
              toPubkey: this.wallet.publicKey,
              lamports: Math.abs(difference),
            })
          );
        }

        const latestBlockhash = await this.connection.getLatestBlockhash();
        transaction.recentBlockhash = latestBlockhash.blockhash;
        transaction.feePayer = this.wallet.publicKey;
        transaction.sign(this.wallet, this.cityAccount);
        const rawTransaction = transaction.serialize();
        const signature = await this.connection.sendRawTransaction(rawTransaction);
        await this.connection.confirmTransaction({
          signature,
          blockhash: latestBlockhash.blockhash,
          lastValidBlockHeight: latestBlockhash.lastValidBlockHeight
        }, 'confirmed');

        console.log(`City budget updated to: ${newBudget} SOL`);
        console.log(`Transaction: ${signature}`);
        return signature;
      }

      return 'No change needed';
    } catch (error) {
      console.error('Error updating budget:', error);
      throw error;
    }
  }

  async getCityState(): Promise<CityState> {
    try {
      const balance = await this.connection.getBalance(this.cityAccount.publicKey);
      return {
        cityBudget: balance / LAMPORTS_PER_SOL
      };
    } catch (error) {
      console.error('Error getting city state:', error);
      throw error;
    }
  }

  // Get the city account public key
  getCityAccount(): PublicKey {
    return this.cityAccount.publicKey;
  }

  // Get wallet balance
  async getWalletBalance(): Promise<number> {
    try {
      const balance = await this.connection.getBalance(this.wallet.publicKey);
      return balance / LAMPORTS_PER_SOL;
    } catch (error) {
      console.error('Error getting wallet balance:', error);
      return 0;
    }
  }
}