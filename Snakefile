configfile: "genomes.yaml"
rule all:
    input:
        expand("results/human/.{humans}", humans=config["humans"]),
        expand("results/bovine/.{bovines}", bovines=config["bovines"]),


rule count:
    input:
        "genomes/{species}/{sample}.fasta"
    output:
        temp("results/{species}/{sample}.jf")
        #tt=touch("touchFile1")
    threads:
        2
    shell:
        "jellyfish count -m 11 -s 100M -t {threads} {input} -o {output}"

rule dump:
    input:
        "results/{species}/{sample}.jf"
    output:
        "results/{species}/{sample}.fa"
    shell:
        "jellyfish dump {input} > {output}"

rule loadIntoLmdb:
    input:
        "results/{species}/{sample}.fa"
    output:
        touch("results/{species}/.{sample}")
    shell:
        "python fastaParser.py {input}"
