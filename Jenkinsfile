pipeline {
  agent { label 'starkiller-base' }
  options { disableConcurrentBuilds() }
  environment{
    AWS_CLI         = "docker-oncology.dockerhub.illumina.com/ops/awscli:2"
    BUILD_PREFIX    = "1.0.0"
    ECR_CREDENTIALS = "svc_jenkins_builder_integration"
    ECR_REGION      = "us-east-1"
    ECR_REPO_URL    = "413488955463.dkr.ecr.us-east-1.amazonaws.com"
    PRODUCT_VERSION = ""
  }
  stages {
    stage('Product Version') { steps { script { PRODUCT_VERSION = getNextBuildVer(BUILD_PREFIX) } } } // Product Version

    stage('Git Tag') { steps { script { gitTag(PRODUCT_VERSION) } } } // Git Tag

    stage('Build') { steps { sh "make build PRODUCT_VERSION=${PRODUCT_VERSION}" } } // Build

    stage('Artifactory-push') {
      when { branch 'master' }
      steps { 
        dockerLogin('docker-oncology')
        sh "make artifactory-push PRODUCT_VERSION=${PRODUCT_VERSION}" 
      } 
    } // Artifactory-push

    stage('Ecr-push') {
      when { branch 'master' }
      steps {
        script {
          // dockerLogin so we can pull the awscli ops container
          dockerLogin('docker-oncology')
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: ECR_CREDENTIALS, passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID']]) {
              sh "make ecr-jenkins-push \
                  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                  AWS_CLI=${AWS_CLI} \
                  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                  ECR_REGION=${ECR_REGION} \
                  ECR_REPO_URL=${ECR_REPO_URL} \
                  PRODUCT_VERSION=${PRODUCT_VERSION} \
                 "
            }
        }
      } 
    } // Ecr-push   
  } // stages
  post { cleanup { deleteDir() } } // remove jenkins workspace at end
} // pipeline
