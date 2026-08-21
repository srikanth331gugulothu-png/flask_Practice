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

        stage('Push Docker Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'dockerhub-srikanth',
                usernameVariable: 'DOCKER_USERNAME',
                passwordVariable: 'DOCKER_PASSWORD'
            )
        ]) {
            sh '''
                set -e

                echo "===== Docker Hub Login ====="
                echo "$DOCKER_PASSWORD" | docker login \
                    --username "$DOCKER_USERNAME" \
                    --password-stdin

                echo "===== Tagging Docker Image ====="
                docker tag srikanth-flask-app:${BUILD_NUMBER} \
                    $DOCKER_USERNAME/flask-student-app:${BUILD_NUMBER}

                docker tag srikanth-flask-app:${BUILD_NUMBER} \
                    $DOCKER_USERNAME/flask-student-app:latest

                echo "===== Pushing Build Image ====="
                docker push \
                    $DOCKER_USERNAME/flask-student-app:${BUILD_NUMBER}

                echo "===== Pushing Latest Image ====="
                docker push \
                    $DOCKER_USERNAME/flask-student-app:latest

                echo "===== Docker Push Completed ====="

                docker logout
            '''
        }
    }
}

stage('Deploy to EC2') {
    steps {
        sshagent(['ec2-ssh-srikanth']) {
            sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@3.83.240.44 << 'EOF'

echo "===== Deploying Flask Application ====="

docker pull srikanthgugulothu/flask-student-app:latest

docker rm -f flask-student-app 2>/dev/null || true

docker run -d \
    --name flask-student-app \
    --restart unless-stopped \
    --env-file ~/flask.env \
    -p 5000:5000 \
    srikanthgugulothu/flask-student-app:latest

echo "===== Container Status ====="
docker ps --filter "name=flask-student-app"

echo "===== Health Check ====="

sleep 5

curl -f http://localhost:5000/health|| exit 1

echo "===== Flask Application is Healthy ====="

echo "===== Deployment Completed ====="

EOF
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
                bandit app.py

            echo "===== Bandit Scan Passed ====="
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

emailext(
    subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    body: """
        CI/CD Pipeline Successful

        Job: ${env.JOB_NAME}
        Build: #${env.BUILD_NUMBER}
        Status: SUCCESS

        Health Check: PASSED
    """,
    to: "srikanth331gugulothu@gmail.com"
)
}