#!/usr/bin/env python
from Bio import SeqIO
import lmdb
import sys
import zarr

env = lmdb.Environment('database', max_dbs=35)
masterenv = lmdb.Environment('masterdb')
indexEnv = lmdb.Environment('indexDatabase', max_dbs=2)
numRows = env.stat()["entries"] #33
numCols = masterenv.stat()["entries"] #3.6 mil
zarrFile = zarr.open('zarr/zarrFile.zarr',mode='w', shape=(numRows, numCols),chunks=True, dtype='?')

genomeDB = indexEnv.open_db('genomeIndex'.encode(),dupsort=True)
kmerDB = indexEnv.open_db('kmerIndex'.encode(),dupsort=True)

#set whole array to zero
zarrFile[:] = 0;

#prints all key value pairs in the masterdb as b'
"""
with masterenv.begin() as txn:
    cursor = txn.cursor()
    for key, value in cursor:
        print(key,value)
"""

#prints all file names as results/bovine/ECI-0715.fa
"""
with env.begin() as transaction:
    cursor = transaction.cursor()
    for key, value in cursor:
        print(key.decode("ascii"))
"""

#genome indexer, used to convert genome name to row number for zarr
#genomeToIndex={}
#genomeCounter=0

#kmer indexer, used to convert kmer sequence to column number for zarr
#kmerToIndex={}
#kmerCounter=0
#counter=0
#prints all genome kmer counts as results/bovine/ECI-0715.fa AACAGCGTAAA 9
with env.begin(write=False) as transaction:
    genomeCursor = transaction.cursor()
    for genome, value in genomeCursor:
        #now looping between each genome
        genome = genome.decode('ascii')
        genome_db = env.open_db(genome.encode('ascii'))
        #genomeToIndex[genome] = genomeCounter
        #genomeCounter += 1
        print('reading genome at: ',genome)

        with env.begin(write=False, db=genome_db) as txn, indexEnv.begin(db=genomeDB) as gIndex, indexEnv.begin(db=kmerDB) as kIndex:
            kmerCursor = txn.cursor()
            for kmerSeq, kmerCount in kmerCursor:
                #now looping through the genomes kmer counts
                kmerSeq = kmerSeq.decode('ascii')
                kmerCount = int (kmerCount)
                #kmerToIndex[kmerSeq] = kmerCounter
                #print(genome, kmerSeq, kmerCount)
                #counter +=1
                #if(counter % 1000 == 0): #speedtest
                #    print('thow')
                if kmerCount > 0 :
                    #genomeIndex = genomeToIndex[genome]
                    #kmerIndex = kmerToIndex[kmerSeq]
                    zarrFile[int(gIndex.get(genome.encode())), int(kIndex.get(kmerSeq.encode()))] = 1
