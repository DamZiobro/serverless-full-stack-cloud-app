#
# Makefile
#

#set default ENV based on your username and hostname
APP_DIR=api
TEST_DIR=tests
#get name of GIT branchse => remove 'feature/' if exists and limit to max 20 characters
#GIT_BRANCH_TAG=$(shell git rev-parse --abbrev-ref HEAD | sed -E 's/[\/]+/-/g' | sed -E 's/feature-//g' | cut -c 1-9)
#ENV = $(GIT_BRANCH_TAG)
#ENV ?= $(shell echo $(TMP_ENV) | tr A-Z a-z | tr - _) #lowercase ENV
ENV ?= dev
AWS_DEFAULT_REGION ?= eu-west-1
PYTHON_VERSION=python3.7
activate = VIRTUAL_ENV_DISABLE_PROMPT=true . .venv/bin/activate;
activate_updir = VIRTUAL_ENV_DISABLE_PROMPT=true . ../.venv/bin/activate;
PYTHON_EXEC=$(activate) PYTHONPATH=$(PYTHONPATH):$(PWD)/$(APP_DIR) $(PYTHON_VERSION)

#==========================================================================
# Test and verify quality of the app
serverless:
	#install serverless framework for Continous Deployment
	npm install -g serverless@1.51.0 || true
	sls plugin install -n serverless-plugin-cloudwatch-dashboard
	sls plugin install -n serverless-python-requirements
	sls plugin install -n serverless-finch
	touch $@


ensure-venv:
ifeq ($(wildcard .venv),)
	@$(MAKE) -f $(THIS_FILE) venv
endif

venv:
	if [ -d .venv ]; then rm -rf .venv; fi
	$(PYTHON_VERSION) -m venv .venv --clear
	$(activate) pip3 install --upgrade pip
	touch $@

requirements: venv serverless
	$(activate) pip install -r requirements.txt #requirements which should be included into lambdas zip packages of DBMigrationLambda
	$(activate) pip install -r api/requirements.txt #requirements which should be included into lambdas zip packages of API
	$(activate) pip install -r other-requirements.txt #other requirements should not not be included in zip packages
	$(activate) pip install -r tests/test-requirements.txt #unittest related requirements
	$(activate) pip install -r load-tests/test-requirements.txt #load tests related requirements
	@echo "\n\n   PATCH: enable docutils in lambda zip in Zappa to avoid DistributionNotFound error\n\n"
	patch -p1 < allow_docutils_in_zappa_zip.diff || true
	touch $@

clean:
	rm -f serverless venv requirements

unittest: requirements
	$(PYTHON_EXEC) -m unittest discover ${TEST_DIR}

coverage: requirements
	$(PYTHON_EXEC) -m coverage --version
	$(PYTHON_EXEC) -m coverage run --source ${APP_DIR} --branch -m unittest discover -v 
	$(PYTHON_EXEC) -m coverage report -m
	$(PYTHON_EXEC) -m coverage html

lint: requirements
	$(PYTHON_EXEC) -m pylint --version
	$(PYTHON_EXEC) -m pylint ${APP_DIR}

security:
	$(PYTHON_EXEC) -m bandit --version
	$(PYTHON_EXEC) -m bandit ${APP_DIR}

code-checks: lint security

deploy-api: requirements
	@echo "======> Deploying Flask-based API resources in env $(ENV) <======"
	cd $(APP_DIR) && \
		$(activate_updir) zappa deploy $(ENV) -s zappa_settings.json || \
		$(activate_updir) zappa update $(ENV) -s zappa_settings.json

deploy-db: requirements
	@echo "======> Deploying RDS Aurora-based AWS resources server $(ENV) <======"
ifeq ($(FUNC),)
	sls deploy --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION)
else
	sls deploy --stage $(ENV) -f $(FUNC) --verbose --region $(AWS_DEFAULT_REGION)
endif

deploy-ui: requirements
	sls client deploy --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION) --no-confirm

deploy-all: deploy-db deploy-api deploy-ui

e2e-tests: 
	@echo "e2e-tests - TO BE IMPLEMENTED"

load-tests:
	@echo "Starting Locust-based load tests of Flask-based RESTful API"
	ENV=$(ENV) $(PYTHON_EXEC) -m locust -f load-tests/locusttest.py --config load-tests/locust.conf

destroy-api: requirements
	@echo "======> DELETING Flask-based API resources in env $(ENV) <======"
	cd $(APP_DIR) && \
		$(activate_updir) zappa undeploy --yes $(ENV)

destroy-db: requirements
	@echo "======> DELETING RDS Aurora-based AWS resources server $(ENV) <======"
	sls remove --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION)

destroy-ui: requirements
	sls client remove --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION) --no-confirm

destroy-all: destroy-ui destroy-api destroy-db #should be recersed order than deploy-all

ci: code-checks unittest coverage
cd: ci deploy-all e2e-tests load-tests

.PHONY: e2e-test deploy destroy unittest coverage lint security code-checks smoke-run logs destroy load-tests
