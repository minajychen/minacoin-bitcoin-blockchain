from binascii import unhexlify, hexlify
import hashlib




def byteswap(transaction):
    return ''.join(a+b for a, b in zip(transaction[::-2], transaction[-2::-2])) #"".join(reversed([transaction[i:i+2] for i in range(0, len(transaction), 2)]))


def doubleHash(id1, id2):
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

txids=["b5f60977102f95a9ed855b61acec86e2e434248b38c5f263ccf708a302832f3c",
    "e6922d44c520c52dca2cd5300784af55944c11839684e5c1671d9b330f871f55",
    "a72ef0e0240fb592dd1d6ec3d1ab24890def0870f5c44d478f1feb1f87701e43",
    "51ef089bd2fc330cd02ee9d5a3cb5532ed48d8668ed78a92b84c8da97922975a",
    "ae22ea6889a5712eb2e13736ce4586afd310295c6ddbbc2b56b1305441017a70",
    "cfce9664889e17fa006cfa23dd82852a999f9a748478cf325e3791241dd27a50",
    "4db4ac98aa68d75dc3602f8f3b06157ac93485268df220cc6dc4aa39f6f9d7a9",
    "a0337aef8e3739e6b705c51202a9d58addc375e2830e3429727a461052279d46",
    "0dc7b3bf9b1a98859d694146a0acd5a988d4184ab9c048ea91d8be7fd1cd84e6",
    "72e15234eb42c9f4b650dec5727205dacbbcb039e8c22034b00bf805192abec7",
    "dca4db368d5241219a0f5f8c744c42293b9bc4959b99e4ed43abc075c284b78c",
    "a5e67793f9193a7b9192e4c3e7cd27268ef354b0513a9cd595c04778d3fa3eef",
    "4d53b64a343589f9b76643c80eacdd632cc50fcec6ece4dd7d3c0c65dba1d0f9",
    "3495a4fab0ff587f6050a22035e12253b250d088413dbd30b1cb44365b87bd86"]

level2=[]

print("Number of Branches in Level 1 is {} \n".format(len(txids)))

print("Branch 1 is {}".format(txids[0]))
print("Branch 2 is {}".format(txids[1]))
print("Branch hash is {} \n".format(doubleHash(txids[0], txids[1])))
level2.append(doubleHash(txids[0], txids[1]))

print("Branch 3 is {}".format(txids[2]))
print("Branch 4 is {}".format(txids[3]))
print("Branch hash is {} \n".format(doubleHash(txids[2], txids[3])))
level2.append(doubleHash(txids[2], txids[3]))

print("Branch 5 is {}".format(txids[4]))
print("Branch 6 is {}".format(txids[5]))
print("Branch hash is {} \n".format(doubleHash(txids[4], txids[5])))
level2.append(doubleHash(txids[4], txids[5]))

print("Branch 7 is {}".format(txids[6]))
print("Branch 8 is {}".format(txids[7]))
print("Branch hash is {} \n".format(doubleHash(txids[6], txids[7])))
level2.append(doubleHash(txids[6], txids[7]))

print("Branch 9 is {}".format(txids[8]))
print("Branch 10 is {}".format(txids[9]))
print("Branch hash is {} \n".format(doubleHash(txids[8], txids[9])))
level2.append(doubleHash(txids[8], txids[9]))

print("Branch 11 is {}".format(txids[10]))
print("Branch 12 is {}".format(txids[11]))
print("Branch hash is {} \n".format(doubleHash(txids[10], txids[11])))
level2.append(doubleHash(txids[10], txids[11]))

print("Branch 13 is {}".format(txids[12]))
print("Branch 14 is {}".format(txids[13]))
print("Branch hash is {} \n".format(doubleHash(txids[12], txids[13])))
level2.append(doubleHash(txids[12], txids[13]))

print("Completed level 1.")
print("*"*40)

print("Number of Branches in Level 2 is {} \n".format(len(level2)))

level3=[]

print("Branch 1 is {}".format(level2[0]))
print("Branch 2 is {}".format(level2[1]))
print("Branch hash is {} \n".format(doubleHash(level2[0], level2[1])))
level3.append(doubleHash(level2[0], level2[1]))

print("Branch 3 is {}".format(level2[2]))
print("Branch 4 is {}".format(level2[3]))
print("Branch hash is {} \n".format(doubleHash(level2[2], level2[3])))
level3.append(doubleHash(level2[2], level2[3]))

print("Branch 5 is {}".format(level2[4]))
print("Branch 6 is {}".format(level2[5]))
print("Branch hash is {} \n".format(doubleHash(level2[4], level2[5])))
level3.append(doubleHash(level2[4], level2[5]))

print("Branch 7 is {}".format(level2[6]))
print("Unbalanced Branch 7 is self-hashed to yield:")
print("Branch hash is {} \n".format(doubleHash(level2[6], level2[6])))
level3.append(doubleHash(level2[6], level2[6]))

print("Completed level 2.")
print("*"*40)

print("Number of Branches in Level 3 is {} \n".format(len(level3)))

level4=[]

print("Branch 1 is {}".format(level3[0]))
print("Branch 2 is {}".format(level3[1]))
print("Branch hash is {} \n".format(doubleHash(level3[0], level3[1])))
level4.append(doubleHash(level3[0], level3[1]))

print("Branch 3 is {}".format(level3[2]))
print("Branch 4 is {}".format(level3[3]))
print("Branch hash is {} \n".format(doubleHash(level3[2], level3[3])))
level4.append(doubleHash(level3[2], level3[3]))

print("Completed level 3.")
print("*"*40)

print("Number of Branches in Level 4 is {} \n".format(len(level4)))

print("Branch 1 is {}".format(level4[0]))
print("Branch 2 is {}".format(level4[1]))
print("Branch hash is {} \n".format(doubleHash(level4[0], level4[1])))
final=[]
final.append(doubleHash(level4[0], level4[1]))


print("Completed level 4.")
print("*"*40)

print("FINAL MERKLE ROOT: {}".format(final))