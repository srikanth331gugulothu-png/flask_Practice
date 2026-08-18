pipeline {
    agent any

    stages {

        stage('Check Jenkins Environment') {
            steps {
                sh '''
                    echo "===== OS ====="
                    uname -a

                    echo "===== Python ====="
                    python3 --version || true
                    which python3 || true

                    echo "===== Pip ====="
                    python3 -m pip --version || true

                    echo "===== Venv ====="
                    python3 -m venv --help || true

                    echo "===== Working Directory ====="
                    pwd

                    echo "===== Files ====="
                    ls -la
                '''
            }
        }
    }
}