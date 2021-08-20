#!/usr/bin/python
from bcc import BPF

# Loads eBPF program
b = BPF(src_file = "ddos.c",debug = 0)

# Attach kprobe to kernel function ip_rcv and sets detect as kprobe handler
b.attach_kprobe(event="ip_rcv", fn_name="detect")


# displays a  message when eBPF starts
print("eBPF en fonctionnement .... Ctrl-C pour annuler")

while 1:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        print("%f ==> %s " % (ts, msg))