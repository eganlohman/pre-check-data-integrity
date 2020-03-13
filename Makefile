# names the docker image after the basename of the current repository
DOCKER_NAME     ?= $(shell basename -s .git `git config --get remote.origin.url`|tr '[:upper:]' '[:lower:]')
DOCKER_REGISTRY ?= docker-oncology.dockerhub.illumina.com
DOCKER_TAG      ?= ${PRODUCT_VERSION}
DOCKER_USER_ID  ?= $(shell id -u)
ECR_REPO_URL    ?= local_testing_ecr_url_goes_here
PRODUCT_VERSION ?= 0.0.0.1

build:
	docker build -t ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG} .
	docker tag ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG} ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG}

run-with-manifest:
	docker run --rm -v ${OUTPUT_FOLDER}:/outputs/output-folder:rw -v ${INPUT_FOLDER}:/mount/inputs/input-folder:ro -v ${MANIFEST}:/mount/inputs/manifest.json:ro ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG} --inputFolderPath /mount/inputs/input-folder/ --outputFolderPath /outputs/output-folder/ --manifest /mount/inputs/manifest.json

run-without-manifest:
	docker run --rm -v ${OUTPUT_FOLDER}:/outputs/output-folder:rw -v ${INPUT_FOLDER}:/mount/inputs/input-folder:ro ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG} --inputFolderPath /mount/inputs/input-folder/ --outputFolderPath /outputs/output-folder/

interactive:
	docker run --rm -it --entrypoint bash ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG}

artifactory-push:
	docker push ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG}

# ecr-login is a target for Jenkins use `gimme-aws-creds` to cg-sandbox-1 to login locally
ecr-login:
	DOCKER_LOGIN=`docker run --rm -a stdout --user ${DOCKER_USER_ID} \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		${AWS_CLI} aws ecr get-login --no-include-email --region ${ECR_REGION}` ; \
	eval $$DOCKER_LOGIN ; \
	echo $$DOCKER_LOGIN

ecr-tag:
	docker tag ${DOCKER_REGISTRY}/${DOCKER_NAME}:${DOCKER_TAG} ${ECR_REPO_URL}/${DOCKER_NAME}:${DOCKER_TAG}

ecr-push:
	docker push ${ECR_REPO_URL}/${DOCKER_NAME}:${DOCKER_TAG}

ecr-jenkins-push: ecr-login ecr-tag ecr-push
	echo "pushing image to ECR"
