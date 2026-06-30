# Documentation Technique - Déploiement du serveur d'inférence

**Projet :** TechCorp Industries – Challenge IA

**Auteur :** Équipe Infrastructure

**Version :** 1.0

**Date :**  30/06/2026

---

# 1. Contexte

## Objectif

Dans le cadre du projet **TechCorp Industries**, l'équipe Infrastructure avait pour mission de déployer une plateforme d'inférence permettant de rendre le modèle **Phi-3.5-Financial** accessible via une API REST afin que l'équipe **Développement Web** puisse créer une interface de chat.

Le serveur devait répondre aux contraintes suivantes :

- Héberger le modèle d'inférence.
- Fournir une API HTTP accessible.
- Permettre une intégration simple avec l'interface de chat.
- Être facilement reproductible.

---

# 2. Choix techniques

Après étude des solutions proposées dans le sujet (**Ollama**, **Triton Inference Server** et **serveur maison**), le choix s'est porté sur **Ollama**.

## Justification

### Ollama

Avantages :

- Déploiement rapide.
- Configuration simple.
- API REST native.
- Documentation complète.
- Compatible Docker.
- Support CPU et GPU.

### Docker

Docker permet :

- L'isolation de l'environnement.
- La portabilité.
- Un redéploiement rapide.
- La persistance des modèles grâce aux volumes Docker.

---

# 3. Architecture

```text
                     Internet
                          │
                          ▼
                Oracle Cloud Infrastructure
                          │
                    Machine virtuelle Ubuntu
                          │
                     Docker Engine
                          │
                    Conteneur Ollama
                          │
               Modèle Phi-3.5-Financial
                          │
                     API REST (11434)
                          │
                   Interface Web (DEV WEB)
```

---

# 4. Environnement

| Élément | Valeur |
|----------|---------|
| Hébergement | Oracle Cloud Infrastructure |
| Système | Ubuntu Server |
| Conteneurisation | Docker |
| Serveur IA | Ollama |
| Modèle | Phi3-Financial |
| API | REST |

---

# 5. Déploiement

## Installation de Docker

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2
```

Activation du service :

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

---

## Déploiement du conteneur

Le serveur Ollama est exécuté dans un conteneur Docker.

```bash
docker compose up -d
```

Vérification :

```bash
docker ps
```

---

## Téléchargement du modèle

```bash
docker exec -it ollama ollama pull phi3.5
```

---

## Création du modèle

Le modèle spécifique au projet est créé à partir du fichier **Modelfile** fourni.

```bash
docker exec -it ollama ollama create phi3-financial -f /root/Modelfile
```

Vérification :

```bash
docker exec -it ollama ollama list
```

---

# 6. Configuration réseau

Le serveur Ollama écoute sur :

```text
0.0.0.0:11434
```

Le port **11434/TCP** est publié par Docker.

Le pare-feu Oracle Cloud a été configuré afin d'autoriser les connexions entrantes sur ce port.

Les développeurs peuvent accéder au serveur via :

```text
http://IP_PUBLIQUE:11434
```

---

# 7. API REST

## URL

```text
http://IP_PUBLIQUE:11434
```

## Endpoint principal

```text
POST /api/chat
```

## Exemple de requête

```json
{
  "model": "phi3-financial",
  "messages": [
    {
      "role": "user",
      "content": "Bonjour"
    }
  ],
  "stream": false
}
```

## Exemple de réponse

```json
{
  "model": "phi3-financial",
  "message": {

---

# 8. Tests réalisés

## Vérification du serveur
```

Résultat attendu :

```json
{
    }
  ]
}
```

---

## Test conversationnel

```bash
curl http://localhost:11434/api/chat \
-H "Content-Type: application/json" \
-d '{
  "model":"phi3-financial",
      "content":"Explique le principe des intérêts composés."
    }
  ],
  "stream":false
}'
```

Résultat :

Le modèle retourne une réponse générée correspondant à la question.

---
Depuis un poste distant :

```bash
curl http://IP_PUBLIQUE:11434/api/tags
```

Résultat :

Le serveur répond correctement et retourne la liste des modèles disponibles.

---

Le serveur fournit une API REST accessible permettant à l'équipe Développement Web d'intégrer rapidement le modèle dans son interface de chat.
# 9. Intégration avec l'équipe Développement Web

L'équipe Développement Web communique directement avec l'API REST.

L'utilisation d'Ollama associée à Docker a permis de mettre en place une plateforme simple à déployer, facilement reproductible et compatible avec les besoins du projet.

---
Les objectifs fixés pour la partie Infrastructure ont été atteints.

# 12. Conclusion

Exemple JavaScript :


- API REST fonctionnelle.
- Accessibilité depuis le réseau.
- Intégration possible avec l'interface développée par l'équipe DEV WEB.
```javascript
fetch("http://IP_PUBLIQUE:11434/api/chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
- Déploiement du modèle Phi-3.5-Financial.
# 11. Résultat


Le serveur d'inférence est désormais opérationnel.

Fonctionnalités validées :

---

    },
    body: JSON.stringify({
        model: "phi3-financial",
        messages: [
            {
- validant l'accès depuis des machines externes.
                role: "user",
- publiant le port 11434 avec Docker ;
- ajoutant une règle Ingress dans Oracle Cloud ;
                content: "Bonjour"
            }
- configurant Ollama pour écouter sur toutes les interfaces (`0.0.0.0`) ;
        ],
Ces problèmes ont été résolus en :

        stream: false
- Validation de l'accessibilité depuis des postes distants.

    })
})
.then(response => response.json())
.then(data => console.log(data));
- Exposition correcte du service Docker.
- Ouverture du port 11434 sur Oracle Cloud Infrastructure.
```

- Configuration initiale du serveur Ollama.

---

# 10. Difficultés rencontrées

Au cours du déploiement, plusieurs difficultés ont été rencontrées :

## Test d'accessibilité réseau

  "messages":[
    {
      "role":"user",
  "models": [
    {
      "name": "phi3-financial"

```bash
curl http://localhost:11434/api/tags
  }
}
```

