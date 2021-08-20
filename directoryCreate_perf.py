#!/usr/bin/python
from bcc import BPF
import ctypes as ct

# prog will store the eBPF program
prog = """

struct timestamp_mkdir_class{
    u64 timestamp_mkdir;
};

// Create a channel in PERF BUFFER
BPF_PERF_OUTPUT(events);


int detect(struct pt_regs *ctx){
    struct timestamp_mkdir_class timestampMkdirInstance = {};
    timestampMkdirInstance.timestamp_mkdir = bpf_ktime_get_ns();
    events.perf_submit(ctx, &timestampMkdirInstance, sizeof(timestampMkdirInstance));
    return 0; // always return 0
}
"""

# Loads eBPF program
b = BPF(text=prog)

# Attach kprobe to kernel function and sets  detect routine as jprobe handler
b.attach_kprobe(event="__x64_sys_mkdir", fn_name="detect")


class Data(ct.Structure):
    _fields_ = [("timestamp_mkdir", ct.c_ulonglong)]


# Show a message when eBPF starts
print("Detection stated .... Ctrl-C to end")


def afficher_evenement(cpu, data, size):
    evenement = ct.cast(data, ct.POINTER(Data)).contents
    print("Timestamp sys en ns : %f " % (evenement.timestamp_mkdir))

b["events"].open_perf_buffer(afficher_evenement)

# print result to user
while 1:
	# read messages from PERF BUFFER
    b.perf_buffer_poll()