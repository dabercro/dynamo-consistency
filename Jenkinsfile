def run(os) {
  return {

    docker.build("dynamo-consistency-${os}:${env.BUILD_ID}", "test/${os}").inside('-u root:root -v ${HOME}/public_html:/html') {

      stage("${os}: Copy Source") {
        sh """
           test ! -d ${os} || rm -rf ${os}
           mkdir ${os}
           cp --parents `git ls-files` ${os}
           """
      }

      stage("${os}: Installation") {
        sh "cd ${os}; python setup.py install"
      }

      stage("${os}: Unit Tests") {
        sh "cd ${os}; opsspace-test"
      }

      stage("${os}: Copy Coverage") {
        if (os == 'sl7') {
          sh "cd ${os}; copy-coverage-html /html/coverage/${env.JOB_NAME}/${env.BUILD_NUMBER}"
        } else {
          echo 'Not going to store coverage results'
        }
      }

    }
  }
}

def osList = ['sl6', 'sl7']

node {
  checkout scm
  parallel osList.collectEntries{
    ["${it}": run(it)]
  }
}
