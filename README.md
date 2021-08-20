# Labebpf

## Installation bcc-tools.
En supposant que vous soyez bien comme le prévoit le Lab connecté via VSStudio sur une instance Centos8 (noyau 4.18; uname -a pour vérifier), lancer les commandes suivantes:

Installation de Python3 et création d'un lien symbolique pour les scripts BCC

```
sudo dnf install -y python3
sudo ln -s /usr/bin/python3 /usr/bin/python
```

puis installation des bcc-tools et clone du repo de code associé pour directement tester les exemples

```sudo dnf -y install bcc-tools 
git clone https://github.com/iovisor/bcc.git
```

Lancer l'exemple suivant :

```
sudo bcc/examples/hello_world.py
```

Si tout se passe bien vous devriez voir quelque chose comme ça (affichage d'un message pour les différents process créés; pas de soucis ceux-ci sont probablement lié au server VSCode installé dans la VM)

![helloworld](images/hello_world.png)

Ok, vous vous en doutez probablement, mais vous venez d'exécuter votre premier programme eBPF avec BCC.

# Lab 1

Si sur CentOS/7 la manipulation n'était pas nécessaire, sur CentOS/8 elle semble l'être pour que le programme ci-dessus fonctionne 

```
cat 1 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_mkdir/enable
```

Executer le script directoryCreate.py dans un second terminal et vous devriez obtenir ceci :

![directorycreate](images/DirectoryCreate.png)

Il n'est pas facile de savoir à quelle event attacher sa probe (en effet les traitements enregsitrent ces probes dynamiquement sur le système).
Néanmoins un sous-ensemble de celles qui sont disponible sur le système sont consultables ici :
* /sys/kernel/debug/tracing/available_filter_functions

On pourra aussi trouver la liste des kprobes actives sur le système en consultant le contenu de ce fichier :
* /sys/kernel/debug/tracing/kprobe_events

Enfin, il faut s'assurer que celle qu'on cherche à suivre n'est pas blacklisté. A consulter dans :
* /sys/kernel/debug/kprobes/blacklists