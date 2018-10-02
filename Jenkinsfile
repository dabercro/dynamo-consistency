pipeline {
  agent {
    dockerfile {
      args '-u root:root -v ${HOME}/public_html:/html'
    }
  }

  stages {

    stage('Installation') {
      steps {
        sh 'python setup.py install'
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'opsspace-test'
      }
    }

    stage('Copy Coverage') {
      steps {
        sh 'copy-coverage-html /html/coverage/${JOB_NAME}/${BUILD_NUMBER}'
      }
    }

  }
}
