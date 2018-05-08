#!/usr/bin/env python
from Bio import SeqIO
import lmdb
import sys
import zarr


env = lmdb.Environment('database', max_dbs=35)
masterenv = lmdb.Environment('masterdb')
numRows = env.stat()["entries"] #33
numCols = masterenv.stat()["entries"] #3.6 mil
zarrFile = zarr.open('zarr/zarrFile.zarr',mode='w', shape=(numRows, numCols),chunks=True, dtype='?')

#set whole array to zero
zarrFile[:] = 0;

#now we want to go through and change the zeros for where there kmer count > 0

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

#prints all genome kmer counts as results/bovine/ECI-0715.fa AACAGCGTAAA 9
with env.begin(write=False) as transaction:
    genomeCursor = transaction.cursor()
    for genome, value in genomeCursor:
        #now looping between each genome
        genome = genome.decode('ascii')
        genome_db = env.open_db(genome.encode('ascii'))

        with env.begin(write=False, db=genome_db) as txn:
            kmerCursor = txn.cursor()
            for kmerSeq, kmerCount in kmerCursor:
                #now looping through the genomes kmer counts
                print(genome, kmerSeq.decode('ascii'), kmerCount.decode('ascii'))
