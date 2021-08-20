#!/usr/bin/python
from bcc import BPF

# prog will store the eBPF C program
prog = """

// Create Associative Arrays called compteur
// If access index type is not specified, it defaults to u64
BPF_HASH(compteur); // equivalent to BPF_HASH(compteur, u64);

int detect(void *ctx){
	u64 index_compteur = 0;	// index variable to access compteur elements
	u64 *compteur_pointeur;// to read content of element chosen with index_compteur
    u64 nouveauCompteur=1; // to update content of element chosen with index_compteur
    compteur_pointeur = compteur.lookup(&index_compteur);

    nouveauCompteur = *compteur_pointeur + 1;
    bpf_trace_printk("Nombre de dossier(s) : %d\\n", nouveauCompteur);
    compteur.delete(&index_compteur);
        
	compteur.update(&index_compteur, &nouveauCompteur);
	return 0; // always return 0
}
"""

# Loads eBPF program
b = BPF(text=prog)

# Attach kprobe to kernel function sys_mkdir and sets detect as kprobe handler
b.attach_kprobe(event="__x64_sys_mkdir", fn_name="detect")


# Show a message when eBPF starts
print("Detection stated .... Ctrl-C to end")

b.trace_print()