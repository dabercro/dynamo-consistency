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

    stage('Copy Coverage') {
      steps {
        sh '$VENV; cd test; coverage html'
        sh 'mkdir -p ${HOME}/public_html/coverage/${JOB_NAME}'
        sh 'cp -r test/htmlcov ${HOME}/public_html/coverage/${JOB_NAME}/${BUILD_NUMBER}' /// ugly output
        // Index page looks like a disaster, so let's fix that to
        // sh '$VENV; clean-coverage-html ${HOME}/public_html/coverage/${JOB_NAME}/${BUILD_NUMBER}'
      }
    }

  }
}
