
import time
import hashlib
from binascii import unhexlify, hexlify

TransactionHashes={}

def printTransactionHash():
    for key, value in TransactionHashes.items():
        print(key, ":", value,"\n")

class Transaction:
    def __init__(self, prevBlockHash, transactions,InCounter,OutCounter):
        """the user starts with an instance of Transaction and inputs the indicated parameters/arguments.
        The indicated lab examples are show in main()"""
        self.VersionNumber=1
        self.InCounter=InCounter
        self.ListOfInputs=transactions
        self.OutCounter=OutCounter
        self.TransactionHash=str()
        self.transactions=list(transactions)
        self.prevBlockHash=prevBlockHash
        self.MerkleDict={}
        self.TransactionInfo=[]
        self.TransactionsEncrypt_list=[]
        self.TransactionHashAutoCalc=self.TransactionHash_calc()

    
    def ListOfOutputs(self):
        """function to represent the list of outputs"""
        Outputs=[]
        Outputs.append(self.transactions)
        return Outputs

    def TransactionHash_calc(self):
        """function to calculate a transaction hash"""
        TransactionFields=[]
        TransactionFields.append(str(self.VersionNumber))
        TransactionFields.append(str(self.InCounter))
        TransactionFields.append(str(self.ListOfInputs))
        TransactionFields.append(str(self.OutCounter))
        TransactionFields.append(str(self.ListOfOutputs))
        first1=hashlib.sha256("".join(TransactionFields).encode('utf-8')).hexdigest()
        self.TransactionHash=hashlib.sha256(first1.encode('utf-8')).hexdigest()
        self.TransactionInfo.append(("List of Inputs:", self.ListOfInputs))
        TransactionHashes[self.TransactionHash]=self.TransactionInfo
        return self.TransactionHash


    def Transactions_encrypt(self):
        """function to encrypt a transaction input"""
        for txn in self.transactions:
            self.TransactionsEncrypt_list.append(hashlib.sha256(txn.encode('utf-8')).hexdigest())
        return self.TransactionsEncrypt_list
    
    def buildMerkleTree(self):
        """function to build a merkle tree"""
        self.MerkleDict={}
        level1=[]
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[0], self.TransactionsEncrypt_list[1]))
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[2], self.TransactionsEncrypt_list[3]))
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[4], self.TransactionsEncrypt_list[4]))
        self.MerkleDict["Level 1"]=level1
        level2=[]
        level2.append(self.doubleHash(level1[0], level1[1]))
        level2.append(self.doubleHash(level1[2], level1[2]))
        self.MerkleDict["Level 2"]=level2
        level3=[]
        level3.append(self.doubleHash(level2[0], level2[1]))
        self.MerkleDict["Level 3"]=level3
        return self.MerkleDict
    
    def doubleHash(self, id1, id2):
        """function to double hash"""
        bin1=unhexlify(id1)
        bin2=unhexlify(id2)
        byt1=bytearray(bin1)
        byt1.reverse()
        byt2=bytearray(bin2)
        byt2.reverse()
        hex1=hexlify(byt1)
        hex2=hexlify(byt2)
        res=hex1+hex2
        temp=unhexlify(res)
        first=hashlib.sha256(temp).digest()
        second=hashlib.sha256(first).digest()
        ba = bytearray(second)
        ba.reverse()
        retval = hexlify(ba)
        return retval

    def printTransactions(self):
        return print(self.TransactionsEncrypt_list)
    
    def print_search_transaction(self, hash_id):
        return print(self.TransactionHash[hash_id])


class Header(Transaction):
    def __init__(self, trans_obj, Bits=0, nonce=0):
        """the Header takes in an instance of a Transaction object"""
        self.trans_obj=trans_obj
        self.Version=1
        self.TimeStamp=time.time()
        self.hashMerkleRoot= trans_obj.MerkleDict["Level 3"]
        self.Bits=Bits
        self.nonce=nonce
        self.hashPrevBlock=trans_obj.prevBlockHash
        self.HeaderDict={}
    
    def header_info(self):
        """a function that stores the header info for a block in a dictionary"""
        self.HeaderDict["Version"]=self.Version
        self.HeaderDict["hashPrevBlock"]=self.hashPrevBlock
        self.HeaderDict["hashMerkleRoot"]=self.hashMerkleRoot
        self.HeaderDict["Timestamp"]=self.TimeStamp
        self.HeaderDict["Bits"]=self.Bits
        self.HeaderDict["Nonce"]=self.nonce
        return self.HeaderDict

    def Blockhash_Header(self):
        """a function that hashes the block header"""
        headerFields=str(list(self.HeaderDict.items()))
        first=hashlib.sha256(headerFields.encode('utf-8')).hexdigest()
        self.BlockHashHeaderString=hashlib.sha256(first.encode('utf-8')).hexdigest()
        return self.BlockHashHeaderString

class Block:
    def __init__(self, trans_obj1, header_obj):
        """the Block class takes in 2 parameters. 1) a transaction objection 2) a header object"""
        self.MagicNumber=0xD9B4BEF9
        self.Blocksize=len(trans_obj1.transactions)
        self.BlockHeader=header_obj.HeaderDict
        self.Blockhash=header_obj.BlockHashHeaderString
        self.Transactions_list=trans_obj1.transactions
    
    def printBlock(self):
        print("Magic Number:", self.MagicNumber)
        print("Block size:", self.Blocksize)
        print("Block Header:", self.BlockHeader)
        print("Block hash:", self.Blockhash)
        print("Transactions:", self.Transactions_list)
        return

class Blockchain:
    def __init__(self):
        self.chain=[]
    
    def addBlock(self, block_obj):
        """this add Block function takes in an instance of a Block object and adds the Block to the chain"""
        return self.chain.append(block_obj.Blockhash)

    def print_block_height(self):
        """this is Function 1, which prints out Blocks by height + hash"""
        for bl in self.chain:
            print ("Block height:", (self.chain.index(bl)))
            print("Block hash:", bl)
        return


def main():
    """this is Step 2 of Lab 5's problem 2"""

    t1="Mina sends 4 BTC to Luke"
    t2="Luke sends 2 BTC to Andy"
    t3="Andy sends 2 BTC to Eric"
    t4="Eric sends 5 BTC to Cody"
    t5="Cody sends 7 BTC to Mina"
    t6="Cody sends 2 BTC to Erasmos"
    t7="Mina sends 1 BTC to Charlie"
    t8="Charlie sends 1 BTC to Queso"
    t9="Queso sends 10 BTC to Emma"
    t10="Emma sends 2 BTC to Philip"


    BlockCreation=Blockchain()
    GenesisBlockTransaction=Transaction('0000000000000000000000000000000000000000000000000000000000000000', ["Nancy Pelosi", "visits", "Taiwan", "on", "02/Aug/2022"], 0, 0)
    GenesisBlockTransaction.prevBlockHash
    GenesisBlockTransaction.transactions
    GenesisBlockTransaction.InCounter
    GenesisBlockTransaction.OutCounter
    GenesisBlockTransaction.Transactions_encrypt()
    GenesisBlockTransaction.TransactionsEncrypt_list
    GenesisBlockTransaction.buildMerkleTree()

    HeaderGenesis=Header(GenesisBlockTransaction)
    HeaderGenesis.hashMerkleRoot   
    HeaderGenesis.hashPrevBlock
    HeaderGenesis.header_info()
    HeaderGenesis.Blockhash_Header()

    Block0=Block(GenesisBlockTransaction, HeaderGenesis)
    BlockCreation.addBlock(Block0)


    Transaction1=Transaction(Block0.Blockhash, [t1,t2,t3,t4,t5], 20, 20)
    Transaction1.prevBlockHash
    Transaction1.transactions
    Transaction1.InCounter
    Transaction1.OutCounter
    Transaction1.Transactions_encrypt()
    Transaction1.TransactionsEncrypt_list
    Transaction1.buildMerkleTree()
    
    Header1=Header(Transaction1)
    Header1.hashMerkleRoot
    Header1.hashPrevBlock
    Header1.header_info()
    Header1.Blockhash_Header()

    Block1=Block(Transaction1, Header1)
    BlockCreation.addBlock(Block1)

    Transaction2=Transaction(Block1.Blockhash, [t6, t7, t8, t9, t10], 16, 16)
    Transaction2.prevBlockHash
    Transaction2.transactions
    Transaction2.InCounter
    Transaction2.OutCounter
    Transaction2.Transactions_encrypt()
    Transaction2.TransactionsEncrypt_list
    Transaction2.buildMerkleTree()
    
    Header2=Header(Transaction2)
    Header2.hashMerkleRoot
    Header2.hashPrevBlock
    Header2.header_info()
    Header2.Blockhash_Header()

    Block2=Block(Transaction2, Header2)
    BlockCreation.addBlock(Block2)
    print("This is an example of Function 1: \n")
    BlockCreation.print_block_height()
    print("*"*80,"\n")
    print("This is an example of Function 2: \n")
    """since the TransactionHashes is a dict, the user can find the transactions via a transaction hash ID by
    using the transaction hash ID as a key. The value returned will be the transactions associated with the hash ID"""
    print("Transaction hash:", Transaction1.TransactionHash)
    print("Transactions:", TransactionHashes[Transaction1.TransactionHash])
    return


if __name__== "__main__":
    main()
