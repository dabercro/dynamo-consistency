def run(os) {
  return {

    docker.build("dynamo-consistency-${os}:${env.BUILD_ID}", "test/${os}").inside('-u root:root -v ${HOME}/public_html:/html') {

      stage("${os}: Copy Source") {
        sh """
           mkdir /work
           cp --parents `git ls-files` /work
           """
      }

      stage("${os}: Installation") {
        sh "cd /work; python setup.py install"
      }

      stage("${os}: Unit Tests") {
        sh '''
           cd /work
           opsspace-test
           if which dynamo
           then
               mysqld_safe &
               sleep 5
               source /usr/local/dynamo/etc/profile.d/init.sh

               test/dynamo/fillsql.sh

               # Start server

               test/dynamo/setupcert.sh
               dynamod &
               sleep 5
               su -c 'test/dynamo/testinventory.sh' dynamo
           fi
           '''
      }

      stage("${os}: Copy Coverage") {
        if (os == 'sl7') {
          sh "cd /work; copy-coverage-html /html/coverage/${env.JOB_NAME}/${env.BUILD_NUMBER}"
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
