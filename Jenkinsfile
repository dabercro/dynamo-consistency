pipeline {
  agent any

  environment {
    VENV = 'source venv/bin/activate'
  }

  stages {

    stage('Virtual Env') {
      steps {
        sh 'ls'
        sh 'if [ -d venv ]; then rm -rf venv; fi'
        sh '/home/jenkins/python/bin/virtualenv venv'
        sh 'ls'
      }    
    }

    stage('Build') {
      steps {
        sh 'ls'
        // Had this leftover a bunch
        sh 'test ! -f docs/customdocs.py || rm docs/customdocs.py'
        sh 'test ! -f docs/customdocs.pyc || rm docs/customdocs.pyc'
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
