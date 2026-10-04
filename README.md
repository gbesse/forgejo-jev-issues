# Forgejo Jev Issues

Experimental community alpha v0.1.0 · MIT · Python 3.11+.

## Français

Un service reçoit les webhooks d'issues Forgejo, vérifie la signature HMAC SHA-256 avant de lire le JSON et demande à Jev de choisir `bug`, `feature`, `question` ou `other`. Les cas sous le seuil `0.9` restent `review`. Le mode par défaut prévisualise la décision sans modifier Forgejo ; `FORGEJO_APPLY=1` ajoute uniquement l'étiquette configurée à l'issue du dépôt autorisé. Les réponses ne contiennent pas le texte de l'issue.

```sh
python3 app.py --demo
python3 -m unittest discover -s tests -v
```

Pour recevoir un vrai webhook, configurer `FORGEJO_WEBHOOK_SECRET` et `TYPESAFE_API_KEY`, puis lancer `python3 app.py --config examples/config.json`. Le serveur écoute uniquement sur `127.0.0.1:8090` : placer un proxy TLS devant lui. Pour autoriser l'écriture, configurer aussi `FORGEJO_URL`, `FORGEJO_API_TOKEN`, les identifiants d'étiquettes du dépôt, puis `FORGEJO_APPLY=1`. Tester d'abord sans cette option. Aucun hôte Forgejo ni service Jev réel n'a été testé.

## English

A service receives Forgejo issue webhooks, verifies the HMAC SHA-256 signature before parsing JSON, and asks Jev to choose `bug`, `feature`, `question`, or `other`. Cases below the `0.9` threshold become `review`. By default it previews decisions without changing Forgejo; `FORGEJO_APPLY=1` adds only the configured label to an issue in the allowlisted repository. Responses contain no issue text.

```sh
python3 app.py --demo
python3 -m unittest discover -s tests -v
```

For a real webhook, set `FORGEJO_WEBHOOK_SECRET` and `TYPESAFE_API_KEY`, then run `python3 app.py --config examples/config.json`. The server binds to `127.0.0.1:8090` only: place a TLS reverse proxy in front. To allow writes, also set `FORGEJO_URL`, `FORGEJO_API_TOKEN`, repository label IDs, then `FORGEJO_APPLY=1`. Test without it first. No live Forgejo host or Jev service has been exercised.

## Español

Un servicio recibe webhooks de incidencias Forgejo, verifica la firma HMAC SHA-256 antes de leer el JSON y pide a Jev elegir `bug`, `feature`, `question` u `other`. Los casos por debajo del umbral `0.9` pasan a `review`. Por defecto muestra la decisión sin modificar Forgejo; `FORGEJO_APPLY=1` añade solo la etiqueta configurada a una incidencia del repositorio permitido. Las respuestas no contienen el texto de la incidencia.

```sh
python3 app.py --demo
python3 -m unittest discover -s tests -v
```

Para recibir un webhook real, configura `FORGEJO_WEBHOOK_SECRET` y `TYPESAFE_API_KEY`, luego ejecuta `python3 app.py --config examples/config.json`. El servidor solo escucha en `127.0.0.1:8090`: utiliza un proxy TLS delante. Para permitir escrituras, configura además `FORGEJO_URL`, `FORGEJO_API_TOKEN`, los identificadores de etiquetas del repositorio y `FORGEJO_APPLY=1`. Prueba primero sin esa opción. No se ha probado con un host Forgejo ni con un servicio Jev real.

[Forgejo Actions events](https://forgejo.org/docs/latest/user/actions/reference/) · [compatible label API](https://docs.gitea.com/api/1.27/operations/issue-add-label/). Independent project, unaffiliated with Forgejo or TypeSafe.
