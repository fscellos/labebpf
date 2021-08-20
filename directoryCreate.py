#!/usr/bin/python
# ----------------- Part 1 - Import python libraries ---------------------- 
# On importe la librairie python BCC
from bcc import BPF
# ----------------- End Part 1 - Importing libraries ----------------------
# ----------------- -------------------------------------------------------


# ------------------ Part 2 - Define eBPF program -------------------------
# -------------------------------------------------------------------------
# On défini le programme BPF, en C dans une variable.
# On verra dans le prochain example comment l'importer depuis un autre fichier
programme = """
	int creationDossier(void *ctx){
		bpf_trace_printk("Creation nouveau dossier");
// Il faut toujours renvoyer 0
		return 0;
	}
"""

# Indique le programme à utiliser
b = BPF(text = programme)

# Executer la méthode "creationDossier" quand un appel au kprobe __x64_sys_mkdir est effectue
b.attach_kprobe(event="__x64_sys_mkdir", fn_name="creationDossier")

# ------------------ End part 2 - eBPF program ----------------------------
# ------------------------------------------------ ------------------------


# ------------------ Part 3 - Report traces to user -----------------------
# -------------------------------------------------------------------------
print("Pour stopper eBPF ..... Ctrl+C")


# ------------------- Reading traces and displaying them ------------------
while 1:
        # b.trace_fields() parses traces and saves result into a tuple
	(task, pid, cpu, flags, ts, msg) = b.trace_fields()
        # Customize the display to user
	print("%s at : %f ==> %s " % (msg, ts, task))
# ------------------ End part 3 - Report to user --------------------------
# -------------------------------------------------------------------------