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
        sh '$VENV; python setup.py install'
      }
    }

    stage('Test') {
      steps {
        sh '$VENV; opsspace-test'
      }
    }

  }
}
