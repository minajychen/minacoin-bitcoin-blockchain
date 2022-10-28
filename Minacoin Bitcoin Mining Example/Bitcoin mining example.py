
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
        self.MAX_TXNS=9

    
    def ListOfOutputs(self):
        """function to represent the list of outputs"""
        index=0
        Outputs=[self.OutCounter,index,self.transactions]
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
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[4], self.TransactionsEncrypt_list[5]))
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[6], self.TransactionsEncrypt_list[7]))
        level1.append(self.doubleHash(self.TransactionsEncrypt_list[8], self.TransactionsEncrypt_list[9]))
        self.MerkleDict["Level 1"]=level1
        level2=[]
        level2.append(self.doubleHash(level1[0], level1[1]))
        level2.append(self.doubleHash(level1[2], level1[3]))
        level2.append(self.doubleHash(level1[4], level1[4]))
        self.MerkleDict["Level 2"]=level2
        level3=[]
        level3.append(self.doubleHash(level2[0], level2[1]))
        level3.append(self.doubleHash(level2[2], level2[2]))
        self.MerkleDict["Level 3"]=level3
        level4=[]
        level4.append(self.doubleHash(level3[0], level3[1]))
        self.MerkleDict["Level 4"]=level4
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

    # def coinbase_generator(self):
    #     #doesn't have UTXO as inputs, first transaction, "coinbase" input
    #     #do I include this in list of inputs & list of outputs?
    #     coinbase=25
    #     transaction_fees=self.OutCounter-self.InCounter
    #     total_fees=coinbase+transaction_fees
    #     self.TransactionsEncrypt_list.append(hashlib.sha256(total_fees.encode('utf-8')).hexdigest())
    #     return


class Header(Transaction):
    def __init__(self, trans_obj, Bits=0x207fffff, nonce=0):
        """the Header takes in an instance of a Transaction object"""
        self.trans_obj=trans_obj
        self.Version=1
        self.TimeStamp=time.time()
        self.hashMerkleRoot= trans_obj.MerkleDict["Level 4"]
        self.Bits=Bits
        self.nonce=nonce
        self.hashPrevBlock=trans_obj.prevBlockHash
        self.HeaderDict={}
    
    def miner(self):
        "this is my miner function"
        text=[("Version:", self.Version),("hashPrevBlock:", self.hashPrevBlock),("hashMerkleRoot:",self.hashMerkleRoot),("Timestamp:",self.TimeStamp),("Bits:",self.Bits)]
        Target = int('0x7fffff',base=16)*2**(int('0x8',base=16)*(int('0x20',base=16)-int('0x3',base=16)))
        for non in range(256):
            input_data=str(text)+str(non)
            hash_data=hashlib.sha256(input_data.encode('utf-8')).hexdigest()
            ihash=int(hash_data,16)
            if ihash<Target:
                self.nonce=non
                return self.nonce
    
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

class Miner:
    def __init__(self):
        """takes newly-created transactions and collect transactions into blocks
        1. Goes through the TxnMemoryPool class
        2. Create a block, Blockhash < Target = 0x7fffff * 2^(0x8*(0x20-0x3)"""
        return


def main():
    coinbase="15000"
    t1="Mina input 1500 output 1400 Luke"
    t2="Luke input 1400 output 1300 Andy"
    t3="Andy input 1300 output 1200 Eric"
    t4="Eric input 1200 output 1100 Cody"
    t5="Cody input 1100 output 1000 Mina"
    t6="Cody input 1000 output 900 Erasmo"
    t7="Mina input 1000 output 900 Charlie"
    t8="Charlie input 900 output 800 Queso"
    t9="Queso input 800 output 700 Emma"
    t10="Emma input 700 output 600 Philip"
    t11="Philip input 600 output 500 Matthew"
    t12="Matthew input 500 output 400 Sindhu"
    t13="Sindhu input 400 output 300 Lisa"
    t14="Mina input 1500 output 1400 Luke"
    t15="Luke input 1400 output 1300 Andy"
    t16="Andy input 1300 output 1200 Eric"
    t17="Eric input 1200 output 1100 Cody"
    t18="Cody input 1100 output 1000 Mina"
    t19="Cody input 1000 output 900 Erasmo"
    t20="Mina input 1000 output 900 Charlie"
    t21="Charlie input 900 output 800 Queso"
    t22="Queso input 800 output 700 Emma"
    t23="Andy input 1300 output 1200 Eric"
    t24="Philip input 600 output 500 Matthew"
    t25="Sindhu input 400 output 300 Lisa"
    t26="Mina input 1000 output 900 Charlie"
    t27="Philip input 600 output 500 Matthew"
    t28="Queso input 800 output 700 Emma"
    t29="Andy input 1300 output 1200 Eric"
    t30="Philip input 600 output 500 Matthew"
    t31="Matthew input 500 output 400 Sindhu"
    t32="Queso input 800 output 700 Emma"
    t33="Sindhu input 400 output 300 Lisa"
    t34="Philip input 600 output 500 Matthew"
    t35="Mina input 1000 output 900 Charlie"
    t36="Andy input 1300 output 1200 Eric"
    t37="Queso input 800 output 700 Emma"
    t38="Matthew input 500 output 400 Sindhu"
    t39="Mina input 1000 output 900 Charlie"
    t40="Sindhu input 400 output 300 Lisa"
    t41="Luke input 1400 output 1300 Andy"
    t42="Mina input 1000 output 900 Charlie"
    t43="Queso input 800 output 700 Emma"
    t44="Mina input 1000 output 900 Charlie"
    t45="Philip input 600 output 500 Matthew"
    t46="Luke input 1400 output 1300 Andy"
    t47="Andy input 1300 output 1200 Eric"
    t48="Emma input 700 output 600 Philip"
    t49="Luke input 1400 output 1300 Andy"
    t50="Matthew input 500 output 400 Sindhu"
    t51="Mina input 1000 output 900 Charlie"
    t52="Cody input 1100 output 1000 Mina"
    t53="Philip input 600 output 500 Matthew"
    t54="Sindhu input 400 output 300 Lisa"
    t55="Andy input 1300 output 1200 Eric"
    t56="Cody input 1100 output 1000 Mina"
    t57="Andy input 1300 output 1200 Eric"
    t58="Matthew input 500 output 400 Sindhu"
    t59="Philip input 600 output 500 Matthew"
    t60="Emma input 700 output 600 Philip"
    t61="Cody input 1100 output 1000 Mina"
    t62="Sindhu input 400 output 300 Lisa"
    t63="Mina input 1000 output 900 Charlie"
    t64="Emma input 700 output 600 Philip"
    t65="Matthew input 500 output 400 Sindhu"
    t66="Mina input 1500 output 1400 Luke"
    t67="Charlie input 900 output 800 Queso"
    t68="Luke input 1400 output 1300 Andy"
    t69="Mina input 1000 output 900 Charlie"
    t70="Cody input 1100 output 1000 Mina"
    t71="Charlie input 900 output 800 Queso"
    t72="Queso input 800 output 700 Emma"
    t73="Mina input 1500 output 1400 Luke"
    t74="Sindhu input 400 output 300 Lisa"
    t75="Emma input 700 output 600 Philip"
    t76="Mina input 1500 output 1400 Luke"
    t77="Andy input 1300 output 1200 Eric"
    t78="Charlie input 900 output 800 Queso"
    t79="Luke input 1400 output 1300 Andy"
    t80="Cody input 1100 output 1000 Mina"
    t81="Mina input 1000 output 900 Charlie"
    t82="Matthew input 500 output 400 Sindhu"
    t83="Luke input 1400 output 1300 Andy"
    t84="Charlie input 900 output 800 Queso"
    t85="Sindhu input 400 output 300 Lisa"
    t86="Mina input 1500 output 1400 Luke"
    t87="Cody input 1100 output 1000 Mina"
    t88="Andy input 1300 output 1200 Eric"
    t89="Emma input 700 output 600 Philip"
    t90="Mina input 1000 output 900 Charlie"
    t91="Sindhu input 400 output 300 Lisa"

    TxnMemoryPool=[t1,t2,t3,t4,t5,t6,t7,t7,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50,t51,t52,t53,t54,t55,t56,t57,t58,t59,t60,t61,t62,t63,t64,t65,t66,t67,t68,t69,t70,t71,t72,t73,t74,t75,t76,t77,t78,t79,t80,t81,t82,t83,t84,t85,t86,t87,t88,t89,t90,t91]

    BlockCreation=Blockchain()
    GenesisBlockTransaction=Transaction('0000000000000000000000000000000000000000000000000000000000000000', ["Nancy Pelosi", "visits", "Taiwan", "on", "02/Aug/2022","0","0","0","0","0"], 0, 0)
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


    Transaction1=Transaction(Block0.Blockhash, [coinbase,TxnMemoryPool[0],TxnMemoryPool[1],TxnMemoryPool[2],TxnMemoryPool[3],TxnMemoryPool[4],TxnMemoryPool[5],TxnMemoryPool[6],TxnMemoryPool[7],TxnMemoryPool[8]], 1500, 1400)
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
    Header1.miner()
    Header1.header_info()
    Header1.Blockhash_Header()

    Block1=Block(Transaction1, Header1)
    BlockCreation.addBlock(Block1)

    Transaction2=Transaction(Block1.Blockhash, [coinbase,TxnMemoryPool[9],TxnMemoryPool[10],TxnMemoryPool[11],TxnMemoryPool[12],TxnMemoryPool[13],TxnMemoryPool[14],TxnMemoryPool[15],TxnMemoryPool[16],TxnMemoryPool[17]], 16, 16)
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
    Header2.miner()
    Header2.header_info()
    Header2.Blockhash_Header()

    Block2=Block(Transaction2, Header2)
    BlockCreation.addBlock(Block2)

    Transaction3=Transaction(Block2.Blockhash, [coinbase,TxnMemoryPool[18],TxnMemoryPool[19],TxnMemoryPool[20],TxnMemoryPool[21],TxnMemoryPool[22],TxnMemoryPool[23],TxnMemoryPool[24],TxnMemoryPool[25],TxnMemoryPool[26]], 16, 16)
    Transaction3.prevBlockHash
    Transaction3.transactions
    Transaction3.InCounter
    Transaction3.OutCounter
    Transaction3.Transactions_encrypt()
    Transaction3.TransactionsEncrypt_list
    Transaction3.buildMerkleTree()

    Header3=Header(Transaction3)
    Header3.hashMerkleRoot
    Header3.hashPrevBlock
    Header3.miner()
    Header3.header_info()
    Header3.Blockhash_Header()

    Block3=Block(Transaction3, Header3)
    BlockCreation.addBlock(Block3)

    Transaction4=Transaction(Block3.Blockhash, [coinbase,TxnMemoryPool[27],TxnMemoryPool[28],TxnMemoryPool[29],TxnMemoryPool[30],TxnMemoryPool[31],TxnMemoryPool[32],TxnMemoryPool[33],TxnMemoryPool[34],TxnMemoryPool[35]], 16, 16)
    Transaction4.prevBlockHash
    Transaction4.transactions
    Transaction4.InCounter
    Transaction4.OutCounter
    Transaction4.Transactions_encrypt()
    Transaction4.TransactionsEncrypt_list
    Transaction4.buildMerkleTree()

    Header4=Header(Transaction4)
    Header4.hashMerkleRoot
    Header4.hashPrevBlock
    Header4.miner()
    Header4.header_info()
    Header4.Blockhash_Header()

    Block4=Block(Transaction4, Header4)
    BlockCreation.addBlock(Block4)

    Transaction5=Transaction(Block4.Blockhash, [coinbase,TxnMemoryPool[36],TxnMemoryPool[37],TxnMemoryPool[38],TxnMemoryPool[39],TxnMemoryPool[40],TxnMemoryPool[41],TxnMemoryPool[42],TxnMemoryPool[43],TxnMemoryPool[44]], 16, 16)
    Transaction5.prevBlockHash
    Transaction5.transactions
    Transaction5.InCounter
    Transaction5.OutCounter
    Transaction5.Transactions_encrypt()
    Transaction5.TransactionsEncrypt_list
    Transaction5.buildMerkleTree()

    Header5=Header(Transaction5)
    Header5.hashMerkleRoot
    Header5.hashPrevBlock
    Header5.miner()
    Header5.header_info()
    Header5.Blockhash_Header()

    Block5=Block(Transaction5, Header5)
    BlockCreation.addBlock(Block5)

    Transaction6=Transaction(Block5.Blockhash, [coinbase,TxnMemoryPool[45],TxnMemoryPool[46],TxnMemoryPool[47],TxnMemoryPool[48],TxnMemoryPool[49],TxnMemoryPool[50],TxnMemoryPool[51],TxnMemoryPool[52],TxnMemoryPool[53]], 16, 16)
    Transaction6.prevBlockHash
    Transaction6.transactions
    Transaction6.InCounter
    Transaction6.OutCounter
    Transaction6.Transactions_encrypt()
    Transaction6.TransactionsEncrypt_list
    Transaction6.buildMerkleTree()

    Header6=Header(Transaction6)
    Header6.hashMerkleRoot
    Header6.hashPrevBlock
    Header6.miner()
    Header6.header_info()
    Header6.Blockhash_Header()

    Block6=Block(Transaction6, Header6)
    BlockCreation.addBlock(Block6)

    Transaction6=Transaction(Block5.Blockhash, [coinbase,TxnMemoryPool[45],TxnMemoryPool[46],TxnMemoryPool[47],TxnMemoryPool[48],TxnMemoryPool[49],TxnMemoryPool[50],TxnMemoryPool[51],TxnMemoryPool[52],TxnMemoryPool[53]], 16, 16)
    Transaction6.prevBlockHash
    Transaction6.transactions
    Transaction6.InCounter
    Transaction6.OutCounter
    Transaction6.Transactions_encrypt()
    Transaction6.TransactionsEncrypt_list
    Transaction6.buildMerkleTree()

    Header6=Header(Transaction6)
    Header6.hashMerkleRoot
    Header6.hashPrevBlock
    Header6.miner()
    Header6.header_info()
    Header6.Blockhash_Header()

    Block6=Block(Transaction6, Header6)
    BlockCreation.addBlock(Block6)

    Transaction7=Transaction(Block6.Blockhash, [coinbase,TxnMemoryPool[54],TxnMemoryPool[55],TxnMemoryPool[56],TxnMemoryPool[57],TxnMemoryPool[58],TxnMemoryPool[59],TxnMemoryPool[60],TxnMemoryPool[61],TxnMemoryPool[62]], 16, 16)
    Transaction7.prevBlockHash
    Transaction7.transactions
    Transaction7.InCounter
    Transaction7.OutCounter
    Transaction7.Transactions_encrypt()
    Transaction7.TransactionsEncrypt_list
    Transaction7.buildMerkleTree()

    Header7=Header(Transaction7)
    Header7.hashMerkleRoot
    Header7.hashPrevBlock
    Header7.miner()
    Header7.header_info()
    Header7.Blockhash_Header()

    Block7=Block(Transaction7, Header7)
    BlockCreation.addBlock(Block7)

    Transaction8=Transaction(Block7.Blockhash, [coinbase,TxnMemoryPool[63],TxnMemoryPool[64],TxnMemoryPool[65],TxnMemoryPool[66],TxnMemoryPool[67],TxnMemoryPool[68],TxnMemoryPool[69],TxnMemoryPool[70],TxnMemoryPool[71]], 16, 16)
    Transaction8.prevBlockHash
    Transaction8.transactions
    Transaction8.InCounter
    Transaction8.OutCounter
    Transaction8.Transactions_encrypt()
    Transaction8.TransactionsEncrypt_list
    Transaction8.buildMerkleTree()

    Header8=Header(Transaction8)
    Header8.hashMerkleRoot
    Header8.hashPrevBlock
    Header8.miner()
    Header8.header_info()
    Header8.Blockhash_Header()

    Block8=Block(Transaction8, Header8)
    BlockCreation.addBlock(Block8)

    Transaction9=Transaction(Block8.Blockhash, [coinbase,TxnMemoryPool[72],TxnMemoryPool[73],TxnMemoryPool[74],TxnMemoryPool[75],TxnMemoryPool[76],TxnMemoryPool[77],TxnMemoryPool[78],TxnMemoryPool[79],TxnMemoryPool[80]], 16, 16)
    Transaction9.prevBlockHash
    Transaction9.transactions
    Transaction9.InCounter
    Transaction9.OutCounter
    Transaction9.Transactions_encrypt()
    Transaction9.TransactionsEncrypt_list
    Transaction9.buildMerkleTree()

    Header9=Header(Transaction9)
    Header9.hashMerkleRoot
    Header9.hashPrevBlock
    Header9.miner()
    Header9.header_info()
    Header9.Blockhash_Header()

    Block9=Block(Transaction9, Header9)
    BlockCreation.addBlock(Block9)

    Transaction10=Transaction(Block9.Blockhash, [coinbase,TxnMemoryPool[81],TxnMemoryPool[82],TxnMemoryPool[83],TxnMemoryPool[84],TxnMemoryPool[85],TxnMemoryPool[86],TxnMemoryPool[87],TxnMemoryPool[88],TxnMemoryPool[89]], 16, 16)
    Transaction10.prevBlockHash
    Transaction10.transactions
    Transaction10.InCounter
    Transaction10.OutCounter
    Transaction10.Transactions_encrypt()
    Transaction10.TransactionsEncrypt_list
    Transaction10.buildMerkleTree()

    Header10=Header(Transaction10)
    Header10.hashMerkleRoot
    Header10.hashPrevBlock
    Header10.miner()
    Header10.header_info()
    Header10.Blockhash_Header()

    Block10=Block(Transaction10, Header10)
    BlockCreation.addBlock(Block10)

    BlockCreation.print_block_height()
    print("*"*80,"\n")

    return


if __name__== "__main__":
    main()
