#!/usr/bin/env python
from Bio import SeqIO
import lmdb
import sys
import zarr

def makeZarr(fileName):
    env = lmdb.Environment('database', max_dbs=35)
    masterenv = lmdb.Environment('masterdb')
    indexEnv = lmdb.Environment('indexDatabase', max_dbs=2)
    numRows = env.stat()["entries"] #33
    numCols = masterenv.stat()["entries"] #3.6 mil
    zarrFile = zarr.open('zarr/zarrFile.zarr',mode='w', shape=(numRows, numCols),chunks=(1,numCols), dtype='?',synchronizer=zarr.ThreadSynchronizer())

    genomeDB = indexEnv.open_db('genomeIndex'.encode(),dupsort=True)
    kmerDB = indexEnv.open_db('kmerIndex'.encode(),dupsort=True)

    #set whole array to zero
    #zarrFile[:] = 0;

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

    genome = fileName#.decode('ascii')
    genome = genome.split('.')[0]
    genome_db = env.open_db(genome.encode('ascii'))
    #genomeToIndex[genome] = genomeCounter
    #genomeCounter += 1
    print('reading genome at: ',genome) #macro speedtest
    with env.begin(write=False, db=genome_db) as txn, indexEnv.begin(db=genomeDB) as gIndex, indexEnv.begin(db=kmerDB) as kIndex:
        kmerCursor = txn.cursor()
        for kmerSeq, kmerCount in kmerCursor:
            #now looping through the genomes kmer counts
            kmerSeq = kmerSeq.decode('ascii')
            kmerCount = int (kmerCount)

            if kmerCount > 0 :
                #genomeIndex = genomeToIndex[genome]
                #kmerIndex = kmerToIndex[kmerSeq]
                zarrFile[int(gIndex.get(genome.encode())), int(kIndex.get(kmerSeq.encode()))] = 1

if __name__ == "__main__":
    makeZarr(sys.argv[1])
