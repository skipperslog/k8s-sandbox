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

        stage('Deploy') {
            steps {
                withCredentials([string(
                        credentialsId: 'github-token',
                        variable: 'GH_TOKEN')]) {
                    sh '''
                        rm -rf deploy
                        git clone --depth 1 https://x-access-token:$GH_TOKEN@github.com/skipperslog/k8s-sandbox.git deploy
                        cd deploy
                        sed -i "s|smartx-ledger:.*|smartx-ledger:jenkins-$BUILD_NUMBER|" manifests/deployment.yaml
                        git config user.name "Jenkins"
                        git config user.email "jenkins@localhost"
                        git commit -am "Deploy smartx-ledger:jenkins-$BUILD_NUMBER" || exit 0
                        git push
                    '''
                }
            }
        }
    }
}
