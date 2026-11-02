
# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | Le système doit empêcher les injections SQL lors de la recherche d'un étudiant. | Vérifier que les paramètres SQL sont utilisés. | Développement | S1 |
| 2 | Le système doit authentifier l'utilisateur avant toute modification d'une note. | Une requête sans jeton doit retourner 401. | Développement et tests | S2 |
| 3 | Le système doit interdire aux étudiants de modifier les notes. | Un étudiant doit recevoir 403. | Tests | S3 |
| 4 | Le système doit limiter chaque enseignant à son propre module. | Un enseignant d'un autre module doit recevoir 403. | Tests | S4 |
| 5 | Le système doit accepter uniquement une note numérique entre 0 et 20. | Une note invalide doit retourner 400. | Tests | S5 |
| 6 | Le système doit autoriser l'enseignant du module à modifier la note de son étudiant et ne pas divulguer de détails techniques en cas d'erreur. | La modification autorisée retourne 200 et les erreurs ne révèlent pas les détails internes. | Tests et validation | S6, S7 |
