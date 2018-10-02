def run(os) {
  return {
    node {
      checkout scm
      docker.build("dynamo-consistency-${os}:${env.BUILD_ID}", "test/${os}").inside('-u root:root -v ${HOME}/public_html:/html') {

        stage("${os}: Installation") {
          sh 'python setup.py install'
        }

        stage("${os}: Unit Tests") {
          sh 'opsspace-test'
        }

        stage("${os}: Copy Coverage") {
          if (os == 'sl7') {
            sh 'copy-coverage-html /html/coverage/${JOB_NAME}/${BUILD_NUMBER}'
          } else {
            echo 'Not going to store coverage results'
          }
        }

      }
    }
  }
}

def osList = ['sl6', 'sl7']

parallel osList.collectEntries{
  ["${it}": run(it)]
}
