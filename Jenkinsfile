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
                    echo "===== Python ====="
                    python3 --version

                    echo "===== Docker ====="
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

        stage('Docker Hub Login Test') {
             steps {
                  withCredentials([
            usernamePassword(
                credentialsId: 'dockerhub-srikanth',
                usernameVariable: 'DOCKER_USERNAME',
                passwordVariable: 'DOCKER_PASSWORD'
            )
        ]) {
            sh '''
                echo "$DOCKER_PASSWORD" | docker login \
                    --username "$DOCKER_USERNAME" \
                    --password-stdin
            '''
        }
    }
}

        stage('Run Tests') {
            steps {
                sh '''
                    set -e

                    echo "===== Creating Docker network ====="
                    docker network create srikanth-test-network || true

                    echo "===== Starting MongoDB ====="
                    docker rm -f srikanth-mongodb-test 2>/dev/null || true

                    docker run -d \
                        --name srikanth-mongodb-test \
                        --network srikanth-test-network \
                        mongo:7

                    echo "===== Waiting for MongoDB ====="
                    sleep 10

                    echo "===== Running Pytest ====="

                    docker run --rm \
                        --network srikanth-test-network \
                        -e MONGO_URI=mongodb://srikanth-mongodb-test:27017/test_student_db \
                        srikanth-flask-app:${BUILD_NUMBER} \
                        python -m pytest -v

                    echo "===== Tests Passed ====="

                    echo "===== Cleaning MongoDB ====="
                    docker rm -f srikanth-mongodb-test || true
                    docker network rm srikanth-test-network || true
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    echo "===== Running Pylint ====="

                    docker run --rm \
                        srikanth-flask-app:${BUILD_NUMBER} \
                        python -m pylint app.py --disable=C0114,C0116
                '''
            }
        }


        stage('Security Scan') {
            steps {
                sh '''
                    echo "===== Running Bandit Security Scan ====="

                    docker run --rm \
                        srikanth-flask-app:${BUILD_NUMBER} \
                        bandit -r app.py
        '''
            }
     }

        stage('Build') {
            steps {
                echo 'Build completed successfully.'
            }
        }
    }

    post {

        success {
            echo '========================================='
            echo ' CI PIPELINE SUCCESSFUL '
            echo '========================================='
        }

        failure {
            sh '''
                docker rm -f srikanth-mongodb-test 2>/dev/null || true
                docker network rm srikanth-test-network 2>/dev/null || true
            '''

            echo '========================================='
            echo ' CI PIPELINE FAILED '
            echo '========================================='
        }

        always {
            sh '''
                docker image prune -f || true
            '''
        }
    }
}