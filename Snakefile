configfile: "genomes.yaml"
rule all:
    input:
        "results/.touchFile3"


rule count:
    input:
        "genomes/{species}/{sample}.fasta"
    output:
        temp("results/{species}/{sample}.jf")
        #tt=touch("touchFile1")
    benchmark:
        "benchmarks/{sample}.benchmark.txt"
    threads:
        2
    shell:
        "jellyfish count -m 4 -s 100M -t {threads} {input} -o {output}"

rule dump:
    input:
        "results/{species}/{sample}.jf"
    output:
        "results/{species}/{sample}.fa"
    benchmark:
        "benchmarks/{sample}.benchmark.txt"
    shell:
        "jellyfish dump {input} > {output}"

rule loadIntoLmdb:
    input:
        "results/{species}/{sample}.fa"
    output:
        touch("results/{species}/.{sample}")
    benchmark:
        "benchmarks/{sample}.benchmark.txt"
    threads:
        10000
    shell:
        "python fastaParser.py {input}"

rule createIndexer:
    output:
        touch("results/.touchFile2")

    input:
        expand("results/human/.{humans}", humans=config["humans"]),
        expand("results/bovine/.{bovines}", bovines=config["bovines"])
    shell:
        "python indexCreator.py",

rule createZarr:
    input:
        "results/.touchFile2"
    output:
        touch("results/.touchFile3")
    shell:
        "python zarrCreate.py"
