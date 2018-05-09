#!/usr/bin/env python
from Bio import SeqIO
import lmdb
import sys




env = lmdb.Environment('database', max_dbs=35)
masterenv = lmdb.Environment('masterdb')

indexEnv = lmdb.Environment('indexDatabase', max_dbs=2)
indexEnv.set_mapsize(5000000000)
genomeDB = indexEnv.open_db('genomeIndex'.encode(),dupsort=True)
kmerDB = indexEnv.open_db('kmerIndex'.encode(),dupsort=True)



genomeCounter = 0
kmerCounter = 0


with env.begin(write=False) as transaction, indexEnv.begin(write=True, db=genomeDB) as transaction1:
    genomeCursor = transaction.cursor()
    for genome, value in genomeCursor:
        #now looping between each genome
        genome = genome.decode('ascii')
        genome_db = env.open_db(genome.encode('ascii'))
        transaction1.put(genome.encode(), str(genomeCounter).encode())
        genomeCounter += 1

with masterenv.begin(write=False) as txn, indexEnv.begin(write=True, db=kmerDB) as txn1:
    kmerCursor = txn.cursor()
    for kmerSeq, kmerCount in kmerCursor:
        #now looping through the genomes kmer counts
        kmerSeq = kmerSeq.decode('ascii')
        #kmerCount = int (kmerCount)
        txn1.put(kmerSeq.encode(), str(kmerCounter).encode())
        kmerCounter += 1

"""
with indexEnv.begin(write=True, db=genomeDB) as transaction1:
    print(int(transaction1.get(b'results/bovine/ECI-1910.fa')))
"""
