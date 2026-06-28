[🇬🇧 English](0001-methodology.md) · 🇫🇷 **Français**

# RFC 0001 — Méthodologie de Le Malentendu

- **Statut :** OUVERT AUX COMMENTAIRES (draft)
- **Auteur :** l'auteur (@trivoallan)
- **Date :** 2026-06-28
- **Spec de référence :** [`../method.fr.md`](../method.fr.md) · schémas & exemples : [`../examples.fr.md`](../examples.fr.md) · vision politique intégrale : [`../political-vision.fr.md`](../political-vision.fr.md)
- **Discussion :** dans la Pull Request de cette RFC. Dépôt public → **n'importe qui peut commenter**, sans être collaborateur.

## Comment commenter

- Commente **en ligne** le point précis (`P#`), la thèse (`T#`) ou la question (`Q#`) dans l'onglet *Files changed*.
- Indique ton **registre** : 🎼 musicologie (un fait, vérifiable) · 👂 ressenti (subjectif, tenu) · ✊ politique (valeurs).
- **Le désaccord est le sujet.** La méthode tient des positions attribuées, pas des vérités. *non = malentendu.*

## Les propositions — à commenter (`P#`)

- **P1.** Le produit = **la méthode** (représentation model-agnostic + compilateur), pas l'audio ni le prompt. Suno/Udio/MusicGen = backends interchangeables.
- **P2.** Une fusion a **deux couches** : son **et** texte. Le texte fusionne aussi.
- **P3.** **Trois registres**, à ne pas confondre : 🎼 musicologie, 👂 ressenti, ✊ politique.
- **P4.** **Atomes** (les ~600 genres) vs **molécules** (les 360k fusions). Curation au niveau **atome**.
- **P5.** **Positions attribuées, pas vérités** — sauf le musicologique, falsifiable.
- **P6.** **Vision politique** — voir les six thèses ci-dessous.
- **P7.** **Garde-fous méta :** forme, pas sermon ; **l'oreille juge, pas la théorie.**

## La vision politique intégrale — les six thèses (`T#`)

> Registre 3. Salle des machines, pas paroles — agie dans les croisements, la licence, la forgerie. Texte intégral + références : [`../political-vision.fr.md`](../political-vision.fr.md). Commente thèse par thèse (ex. *« T4 : … »*).

- **T1 — L'authenticité est un rapport de pouvoir, et on la forge pour le prouver.** « Le vrai » est certifié par des gardiens (labels, Discogs, critiques, le marché). Un faux crédible qui entre dans le registre démontre que l'authenticité est un *effet de certification, pas une essence*. On attaque le **critère du réel**, pas un disque. *(Debord ; Benjamin.)*
- **T2 — Contre l'enclosure, pour le commun.** Les modèles d'IA privatisent la culture musicale collective de l'humanité et la revendent. Le moteur est libre (AGPL) : un **commun qui résiste à la clôture**. Ce qui a été fait par tous ne doit pas être re-privatisé par quelques-uns. *(Logiciel libre ; Hyde, le don.)*
- **T3 — Créolisation, pas smoothie.** Croiser des genres, c'est soit la **créolisation** (Glissant — la collision imprévisible qui produit du vraiment neuf), soit le **lissage** (le smoothie du marché, toute différence dissoute en contenu sans friction = slop). Garder la friction, garder l'oreille humaine, jeter le slop. *(Glissant, Poétique de la Relation.)*
- **T4 — Le droit à l'opacité, contre la lisibilité totale.** *(le cœur.)* Le spectacle / l'IA / la base de données exigent que tout soit lisible, indexable, extractible. Le **droit à l'opacité** de Glissant : les cultures peuvent rester opaques, non extractibles. On le défend en produisant l'inclassable — l'illisibilité comme résistance. Les 360k ne sont pas un flux à vendre, c'est une **crue qui sature le registre**. *(Glissant ; Scott.)*
- **T5 — Pas de dehors propre, donc l'œuvre s'auto-implique.** On utilise une IA extractive, on courtise des investisseurs, on lorgne une conf prestigieuse. Il n'y a **pas d'extérieur** (Debord). L'honnêteté = opérer *dans* la contradiction et la nommer : la critique de l'extraction est elle-même une extraction, nommée. *(Cf. [`../../GENESIS.fr.md`](../../GENESIS.fr.md).)*
- **T6 — Le sens contre le contenu, l'oreille humaine comme position.** Le point d'arrivée du spectacle, c'est le contenu infini sans friction. Défendre l'**irréductiblement humain** — le goût, l'oreille, la surprise de 2h du matin — affirme la culture comme *sens vécu, pas débit extractible*.

**Synthèse positive :** Le Malentendu défend la **créolisation** et le **droit à l'opacité**, contre l'**enclosure** et le **lissage** — avec les armes de l'ennemi, et en l'avouant.

## Questions ouvertes — on veut votre avis (`Q#`)

- **Q1.** 🎼 *(un praticien-expert / un musicologue)* Les définitions de genre tiennent-elles ? Lesquelles corriger en premier ?
- **Q2.** 🎼 Qui peut tenir le rôle de **musicologue** pour le registre objectif ? (trou nommé)
- **Q3.** 👂 *(le cercle d'auditeurs)* Les exemplaires-ancres tiennent-ils ? D'autres à proposer ?
- **Q4.** ✊ *(tous)* Les six thèses (T1–T6) : justes ? trop ? pas assez ? L'**auto-implication** (T5) est-elle tenable, ou un alibi ?
- **Q5.** 🛠️ *(un compositeur / builder)* L'archi **instrument** (pas usine) + atomes/molécules : tu la construirais ? tu la détournerais comment ?
- **Q6.** ✍️ La **couche texte** : jusqu'où pousser le contenu politique des paroles avant le sermon ?

## Décision

Pas de vote. Après un tour de cercle : l'auteur tranche (le registre **politique** est sa position assumée). Les corrections **musicologiques** priment sur les goûts. On *merge* quand le modèle a encaissé les commentaires — la version retenue met à jour [`../method.fr.md`](../method.fr.md) et [`../political-vision.fr.md`](../political-vision.fr.md).

---

*non = malentendu*
