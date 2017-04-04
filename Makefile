VIRTUAL_ENV ?= .env
NODE_BIN = node_modules/.bin
SCSS_FILES := $(shell find 'meinberlin/assets/scss' -name '*.scss')
JS_FILES := $(shell find 'meinberlin/assets/js' | grep '\.jsx\?$$')
PO_FILES := $(shell find . -name '*.po')

help:
	@echo mein.berlin development tools
	@echo
	@echo It will either use a exisiting virtualenv if it was entered
	@echo before or create a new one in the .env subdirectory.
	@echo
	@echo usage:
	@echo
	@echo   make install      -- install dev setup
	@echo   make build        -- build js and css and create new po and mo files
	@echo   make lint         -- lint javascript and python
	@echo   make server       -- start a dev server
	@echo   make watch        -- start a dev server and rebuild js and css files\
	                             on changes
	@echo

install:
	npm install
	if [ ! -f $(VIRTUAL_ENV)/bin/python3 ]; then python3 -m venv $(VIRTUAL_ENV); fi
	$(VIRTUAL_ENV)/bin/python3 -m pip install -r requirements/dev.txt
	$(VIRTUAL_ENV)/bin/python3 manage.py migrate

webpack: $(SCSS_FILES) $(JS_FILES)
	$(NODE_BIN)/webpack

makemessages:
	$(VIRTUAL_ENV)/bin/python manage.py makemessages

compilemessages: $(PO_FILES)
	$(VIRTUAL_ENV)/bin/python manage.py compilemessages

build: webpack compilemessages

server:
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000

watch:
	$(NODE_BIN)/webpack --watch & \
	$(VIRTUAL_ENV)/bin/python3 manage.py runserver 8000

lint:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint

lint-quick:
	. $(VIRTUAL_ENV)/bin/activate && $(NODE_BIN)/polylint -SF
