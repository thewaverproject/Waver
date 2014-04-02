# The Waver Project

## Introduction

*The Waver Project* est un projet de TIPE (Travail d'Initiative Personnel Encadré), c'est-à-dire un projet à présenter à l'oral des concours d'admission aux grandes écoles.
Le thème de cette année étant *Échange et Transfert* nous avons décidé que faire un projet d'échange de fichiers par l'intermédiaire de l'internet serai à la fois pleinement dans le sujet et que ce serait l'occassion de découvrir comment fonctionne les réseaux en informatique.

## Utilité d'un tel système

Permettre le partage de fichiers a une réelle utilité. Au-delà des usages illégaux qui en sont faits, le partage de fichiers permet de mettre à disposition des créations de façon légale. On peut prendre l'exemple de la mise à disposition des distributions Linux ou encore la mise en place d'un système de télévision par l'internet.

## Préliminaires nécessaires à la mise en place

 Dès le début plusieurs questions sont apparues. La première et la plus importante est celle de l'architecture de notre système d'échange de fichiers.
 Deux architectures classiques sont l'architecture centralisée et l'architecture décentralisée.

### Architecture centralisée et architecture décentralisée

 Dans le *modèle d'une architecture centralisée*, il y a __un serveur maître__ - qui contient les fichiers à partager - et __des clients__ qui se connectent à ce serveur pour récupérer les fichiers mis à disposition.
 Le principal avantage de cette architecture est qu'elle est relativement simple à mettre en place puisqu'il suffit de créer un serveur auquel les utilisateurs peuvent se connecter - soit depuis un navigateur internet, soit depuis un programme spécialisé. Pour mettre en place un tel système l'ordinateur hôte du système a simplement besoin de faire tourner un serveur http sur le port 80 et l'affaire est entendue.
 Néanmoins, derrière cette apparante simplicité se cache un problème ennuyeux : celui de la charge - i.e. le nombre de connexions simultanées auxquelles devra faire face le serveur. En effet, à la base le serveur à une certaine bande passante (par exemple : 100 Mb/s) qu'il va devoir répartir équitablement entre ses différents clients. Ainsi, __plus il y aura de clients plus le système sera lent__, et dans le pire des cas une forte demande de la part des clients peut provoquer un crash du serveur (c'est d'ailleurs le principe d'une attaque DDOS (Distributed Deny Of Service - Attaque par denis de service distribuée)).
 Il est cependant possible de répartir la charge sur plusieurs serveurs qui semblent agir - pour l'utilisateur - comme un seul et même serveur mais c'est déjà moins simple.

 Dans le *modèle d'une architecture décentralisée*, __le réseau est constitué de pairs__ qui possèdent chacun la totalité - ou des bouts du fichier (que l'on appelera pièces) - à partager. On s'aperçoit alors qu'il n'y a plus vraiment de distinction client/serveur qui tienne puisque __chaque pair est à la fois un client et un serveur__.
 Cette architecture, quoique plus compliquée que la précédente, corrige totalement le point faible du système centralisé. En effet, dans ce cas là, plus il y a de pairs, plus le réseau est efficace.
 Néanmoins, la solution apportée par ce modèle n'est pas toute rose non plus, puisqu'il faut que chaque pair ait l'occasion de découvrir les autre pairs en plus de savoir à qui demander quelle pièce. Cela impose donc de créer une sorte de cartographie.

## Le choix d'une architecture hybride

Notre choix s'est porté sur *une architecture décentralisée hybride*. Nous entendons par là que __l'initiation se fait toujours grâce à un serveur maître__, de cette manière le nouveau pair demande au serveur maître - dorénavant dénommé *tracker* - la liste des pairs partagant le fichier qu'il souhaite. Dans ce modèle le *tracker* envoie un petit fichier (~ 200-500 Kb) ce qui fait que l'on a pas vraiment de problème au niveau de la réparatition de la charge puisque le transfert du fichier d'adresses IPs est rapide (~ 1-10 s en général, ~ 1 min dans le pire de tous les cas). Le reste est assuré par le réseau de pairs.

À ce niveau-là, plusieurs questions se posent :
 - Comment mettre à disposition un fichier / un répertoire de fichiers grâce à ce système ?
 - Comment les pairs communiquent entre eux ? Définition d'un protocole de communication.
 - Dans quel ordre les pièces de fichiers seront transmises ?
 - Comment vérifier l'intégrité de chaque pièce ?
 - Comment les pairs savent chez qui sont les pièces ?


 ### Un nouveau format de fichier

 Pour pouvoir partager des fichiers à l'aide de notre système nous avons besoin de mettre en place un nouveau format de fichier que nous nommerons simplement *le format waver*.
 Un tel fichier aura pour but d'indiquer à notre système quoi partager/recevoir, comment ? quelle est l'adresse du *tracker* ? quelle est la taille des pièces ? etc.
 Dans ce but notre fichier est découpé en plusieurs sections : `properties`, `tracker`, `pieces` et `hash`. Chaque section est précédée de `:begin nom__de__la__section` et est suivie de `:end nom__la__section`.
 La section `tracker` - la plus simple - contient l'addresse du serveur maître (voire des serveurs maîtres).
 La section `pièces` contient l'arborescence du répertoire (éventuellement réduite à un fichier) annotée avec les informations relatives aux pièces à partager.
 La section `hash` contient le hash md5 de chaque pièce de manière à pouvoir s'assurer de l'intégrité des pièces reçues.
 La section `properties` contient des propriétés relatives au fichier *.waver* en question.
 Enfin, une fois le fichier *.waver* construit, on calcule le hash md5 du fichier et on le place en tête du fichier. Ainsi, le fichier *.waver* contient le hash md5 de tout le fichier exceptée la première ligne détentrice du hash.

### Un nouveau protocole de communication

Les pairs doivent pouvoir échanger entre-eux : il nous faut donc expliciter comment les pairs doivent communiquer et pour cela nous avons besoin d'un protocole de communication que nous nommerons - l'originalité ayant ses limites - *the waver protocole*. Ce protocole doit expliciter comment les pièces circuleront sur le réseau.

Les règles principales sont :
 - Les pièces rares sont prioritaires.
 - Il faut partager ce que l'on a reçu dans la mesure du possible : les sangsues ne sont pas profitable à un tel écosystème.


 Il nous faut donc pouvoir déterminer où sont les pièces rares et obliger les sangsues à partager un minimum.

 ### Une cartographie du réseau

 Étant donnée l'ampleur d'un tel système maintenir une cartographie exacte est mission impossible. Pour illustrer la dimension du système prenons un fichier de 3 Gb divisé en pièces de 2 Mb : cela fait 1500 pièces. Si en plus de cela il y a 150 pairs, une cartographie précise requiert au moins 225 000 espaces de mémoire disponibles, et ce pour un seul fichier `.waver`.

 On emploiera pour cela une approche heuristique - c'est à dire que l'on aura pas le résultat mais seulement une approximation du résultat. Plutôt que de regarder toute les pièces on s'intéressera au premier pourcent des pièces : ce sera comme si chaque fichier *.waver* était coupé en 100 parties. Ainsi, quand on cherchera une pièce en particulier on regardera dans quelle partie elle se trouve puis on cherchera les pairs ayant le plus complété cette partie jusqu'à en trouver un qui a la pièce que l'on cherche. En plus de cela, on gardera quand même les numéros du premier pourcent des pièces les plus rares.
 Toutes les demi-heures, chaque pair est tenu de mettre à jour sa cartographie en contactant ses changements aux autres. Cela permet de maintenir une cartographie à peu près fidèle du réseau.
