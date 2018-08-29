pipeline {
  agent any

  environment {
    VENV = 'source venv/bin/activate'
  }

  stages {

    stage('Virtual Env') {
      steps {
        sh 'if [ -d venv ]; then rm -rf venv; fi'
        sh '/home/jenkins/python/bin/virtualenv venv'
      }    
    }

    stage('Build') {
      steps {
        sh '$VENV; python setup.py install'
      }
    }

    stage('Test') {
      steps {
        sh '$VENV; opsspace-test'
      }
    }

    stage('Copy Coverage') {
      steps {
        sh '$VENV; copy-coverage-html ${HOME}/public_html/coverage/${JOB_NAME}/${BUILD_NUMBER}'
      }
    }

  }
}
