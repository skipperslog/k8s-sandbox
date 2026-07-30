pipeline {
    agent any

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
    }
}
