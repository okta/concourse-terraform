#!/bin/bash

# Docker build var
export timeStamp=$(date -d "7 hours ago" "+%d%B%Y-%H%M%S-PST")
export imageName=${BASE_DOCKER_IMAGE}:${SHA}-${timeStamp}
export DOCKER_REPOSITORY_NAME=concourse-terraform
export DOCKER_REPOSITORY_PATH="${OKTA_HOME}/concourse-terraform"
export DOCKER_FILE_PATH="${DOCKER_REPOSITORY_PATH}/Dockerfile"
export CI_DOCKER_IMAGE="true"
export TERRAFORM_VERSION="0.14.3"
  concourse-terraform
source ${OKTA_HOME}/robo-warrior/util/functions.sh
source ${OKTA_HOME}/robo-warrior/scripttemplates/utils/docker/docker_build_utils.sh

function buildImage() {
    DOCKER_FILE_PATH="${DOCKER_FILE_PATH:-$DOCKER_REPOSITORY_PATH/Dockerfile}"
    pushd "${DOCKER_REPOSITORY_PATH}"
        docker build --build-arg RELEASE_VERSION="$RELEASE_VERSION"  --build-arg "TERRAFORM_VERSION=${TERRAFORM_VERSION}" -t  'TERRAFORM_VERSION:'${TERRAFORM_VERSION} -f ${DOCKER_FILE_PATH} -t ${DOCKER_REPOSITORY_NAME}':'${RELEASE_VERSION} .
    popd
}

setup_service docker
setup_service node v12.16.2
setup_service yarn 1.22.4

set_fullversion

current_version=$(get_version_from_dockerfile_label $DOCKER_FILE_PATH)


if ! buildImage; then
    echo "Docker build command failed!"
    report_results FAILURE fail
    exit 1
fi

if ! tagAndPushImages; then
  echo "Failed in tagging and pushing image up to artifactory."
  report_results FAILURE build_failure
  exit 1
fi

DOCKER_TOPIC_UPLOAD_LATEST_IMAGE_TAG=${DOCKER_TOPIC_UPLOAD_REG}'/'${DOCKER_REPOSITORY_NAME}':'latest

docker tag  ${DOCKER_REPOSITORY_NAME}:${RELEASE_VERSION} ${DOCKER_TOPIC_UPLOAD_LATEST_IMAGE_TAG}
docker push ${DOCKER_TOPIC_UPLOAD_LATEST_IMAGE_TAG} && echo -e "\nSuccessfully tagged and pushed image for latest-cache\n" || exit 1

docker manifest inspect ${DOCKER_REPOSITORY_NAME}

echo ${TEST_SUITE_TYPE} > ${TEST_SUITE_TYPE_FILE}
echo ${TEST_RESULT_FILE_DIR} > ${TEST_RESULT_FILE_DIR_FILE}

exit ${SUCCESS}



