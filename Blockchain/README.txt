
Refer to the main() of blockchain.py code for an test case. I hard coded transactions and created a Block chain. 

Block0 is genesis block. It meets all the given requirements

Block1 meets all the requirements

Block2 meets all the requirements

If you run: 

python3 blockchain.py 

On your command line in your terminal, you will see Function 1 and Function 2 printed out.

Function 1 works as required. Function 1: There must be some means of asking your Blockchain for a given block by block height and by block hash.  It is up to you how to implement this.

Function 2 works as required. Function 2: There must be some means of searching the Blockchain for a given Transaction by TransactionHash, which should return the Transaction being searched.

Note: a user can search the Blockchain for a given Transaction by TransactionHash via searching the TransactionHashes dictionary. A user can take the Transaction hash ID, use it as a key in TransactionHashes dictionary, and the returned value will be the Transaction.

