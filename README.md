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
git clone https://github.com/iovisor/bcc.git```

Lancer l'exemple suivant :

```
sudo bcc/examples/hello_world.py
```
