pipeline {
    agent any

    environment {
        IMAGE = 'pb26457093/smartx-ledger'
    }

    stages {
        stage('Test') {
            steps {
                dir('smartx-ledger') {
                    sh '''
                        python3 -m venv .venv
                        .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
                        .venv/bin/pytest -q
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                dir('smartx-ledger') {
                    withCredentials([usernamePassword(
                            credentialsId: 'dockerhub',
                            usernameVariable: 'DH_USER',
                            passwordVariable: 'DH_PASS')]) {
                        sh '''
                            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                            docker build -t $IMAGE:jenkins-$BUILD_NUMBER .
                            docker push $IMAGE:jenkins-$BUILD_NUMBER
                            docker logout
                        '''
                    }
                }
            }
        }
    }
}
