# Orion Empire

## setup (juste une fois)

1. créer un compte / loggez vous sur github
2. fork le repo
3. clone ton fork

```sh
$ git clone https://github.com/TON_USERNAME/orion_empire
```
4. ajouter le remote vers le repo principal

```sh
$ git remote add upstream https://github.com/escargotprodige/orion_empire
$ git fetch upstream
```

## travailler sur une fonctionnalité

créer une nouvelle branche pour le nouveau code
<nouveau-feature> = nom de la nouvelle fonctionnalité
```sh
$ git checkout -b <nouveau-feature>
```

mettre à jour la branche
```sh
$ git pull --rebase upstream master
```

1. codez
2. faites vos commits  
3. push vers votre fork

```sh
$ git push origin <nouveau-feature>
```

faire un pull request (sur github) quand la fonctionnalité est fini