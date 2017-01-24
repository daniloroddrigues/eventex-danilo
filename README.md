# Eventex

Sistema de Eventos encomendado pela Morena.

[![Build Status](https://travis-ci.org/daniloroddrigues/eventex-danilo.svg?branch=master)](https://travis-ci.org/daniloroddrigues/eventex-danilo)
[![Code Health](https://landscape.io/github/daniloroddrigues/eventex-danilo/master/landscape.svg?style=flat)](https://landscape.io/github/daniloroddrigues/eventex-danilo/master)

## Como desenvolver?

1. Clone o repositorio.
2. Crie um virtualenv com Python 3.5
3. Ative o virtualenv.
4. Instale as dependencias.
5. Configure a instancia com o .env
6. Execute os testes.

```console
git clone git@github.com:daniloroddrigues/eventex-danilo.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer deploy?

1. Crie uma instancia no heroku.
2. Envie as configuraçoes para o heroku.
3. Defina uma SECRET_KEY segura para a instancia.
4. Defina DEBUG=False.
5. Configure o serviço de email.
6. Envie o codigo para o heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# configurar o email
git push heroku master --force
```