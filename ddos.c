#include <linux/skbuff.h>
#include <uapi/linux/ip.h>
// Create a MAP
BPF_HASH(compteur_packet_recu); // equivalent a BPF_HASH(compteur);

/* struct pt_regs *ctx exists because it is mantadory to be able to use the parameters of the function*/
int detect(struct pt_regs *ctx, struct sk_buff *skb, struct net_device *dev, struct packet_type *pt, struct net_device *orig_dev){
	u64 compteur_packet_recu_nombre = 0, compteur_packet_recu_nombre_inter=1, *compteur_packet_recu_nombre_ptr;	
	u64 compteur_packet_recu_temps_index = 1, compteur_packet_recu_temps_inter=0, *compteur_packet_recu_temps_ptr;

	// Get number of packets 
	compteur_packet_recu_nombre_ptr = compteur_packet_recu.lookup(&compteur_packet_recu_nombre);

	// Get time of last packet
    compteur_packet_recu_temps_ptr = compteur_packet_recu.lookup(&compteur_packet_recu_temps_index);

	if(compteur_packet_recu_nombre_ptr != 0 && compteur_packet_recu_temps_ptr != 0){
        compteur_packet_recu_nombre_inter = *compteur_packet_recu_nombre_ptr;
	    compteur_packet_recu_temps_inter = bpf_ktime_get_ns() - *compteur_packet_recu_temps_ptr;
	    
        // Intervalle de temps entre le paquet courant et le precedent inferieur à 100000 nanosecondes. On incremente le nombre de paquet
        // suspect de 1
	    if(compteur_packet_recu_temps_inter < 100000){
			compteur_packet_recu_nombre_inter++;
	    } else {
		    compteur_packet_recu_nombre_inter = 0;
	    }

        // Ca y est 10 paquets suspects, on emet l'alarme
	    if(compteur_packet_recu_nombre_inter > 10) {
        	bpf_trace_printk("DDOS attack - number of packets : %d\\n", compteur_packet_recu_nombre_inter);
        }
        compteur_packet_recu.delete(&compteur_packet_recu_nombre);
        compteur_packet_recu.delete(&compteur_packet_recu_temps_index);
    }
    compteur_packet_recu_temps_inter = bpf_ktime_get_ns();
	compteur_packet_recu.update(&compteur_packet_recu_nombre, &compteur_packet_recu_nombre_inter);
	compteur_packet_recu.update(&compteur_packet_recu_temps_index, &compteur_packet_recu_temps_inter);
	return 0; // always return 0
}