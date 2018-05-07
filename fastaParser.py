#!/usr/bin/env python
from Bio import SeqIO
import lmdb
import sys
import pprint

def readData(fileName):

    #Env max_dbs = 40
    """
    env = lmdb.open('database', max_dbs=40)
    env.set_mapsize(5000000000)
    db1 = env.open_db('child_db')
    with env.begin(write=True) as transaction:
        with open(fileName, "rU") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                kmerCount = str(record.id)
                kmerSeq = str(record.seq)
                transaction.put(kmerSeq.encode("ascii"),kmerCount.encode("ascii"))
    """

    env = lmdb.Environment('database', max_dbs=35)
    env.set_mapsize(5000000000)
    #masterenv = lmdb.Environment('masterdb', max_dbs=5, map_size=5000000000)
    genomeID = fileName;
    db1 = env.open_db(genomeID.encode("ascii"),dupsort=True)
    with env.begin(write=True, db=db1) as transaction:
        with open(fileName, "rU") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                kmerCount = str(record.id)
                kmerSeq = str(record.seq)
                transaction.put(kmerSeq.encode("ascii"),kmerCount.encode("ascii"))

                #with masterenv.begin(write=True) as txn:
                #    txn.put(kmerSeq.encode('ascii'), '0'.encode('ascii'), overwrite=True)

    #pprint(env.stat())

    #pprint(masterenv.stat())

#db = lmdb.open("genomeData")

#with db.begin(write=True) as transaction:
#    transaction.put("newkey".encode("ascii"), "newvalue".encode("ascii"))

if __name__ == "__main__":
    readData(sys.argv[1])
