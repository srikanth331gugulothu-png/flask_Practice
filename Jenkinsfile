pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out by Jenkins.'
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    python3 --version
                    docker --version
                    docker info > /dev/null
                    echo "Docker daemon is running"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t srikanth-flask-app:${BUILD_NUMBER} .
                    docker tag srikanth-flask-app:${BUILD_NUMBER} srikanth-flask-app:latest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                    srikanth-flask-app:${BUILD_NUMBER} \
                    python -m pytest -v
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Docker CI build completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'SRikanth CI PIPELINE SUCCESSFUL'
        }

        failure {
            echo 'CI PIPELINE FAILED'
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}