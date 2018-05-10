configfile: "genomes.yaml"

ruleorder: createZarr > createIndexer > loadIntoLmdb
rule all:
    input:
        expand("results/human/.{humans}.fake", humans=config["humans"]),
        expand("results/bovine/.{bovines}.fake", bovines=config["bovines"])

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
        touch("results/{species}/{sample}.fake")
    benchmark:
        "benchmarks/{sample}.benchmark.txt"
    threads:
        10000
    shell:
        "python fastaParser.py {input}"

rule createIndexer:
    output:
        touch("results/touchFile")
    shell:
        "python indexCreator.py",

rule createZarr:
    input:
        "results/touchFile",
        a="results/{species}/{sample}.fake"
    output:
        touch("results/{species}/.{sample}.fake")
    threads:
        1000
    shell:
        "python zarrCreate.py {input.a}"
