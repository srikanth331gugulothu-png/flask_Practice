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
                    python3 -m pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --user -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m pytest -v
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    python3 -m pylint app.py || true
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    python3 -m bandit -r app.py
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'CI build completed successfully.'
            }
        }
    }

    post {
        success {
            echo '========================================='
            echo ' CI PIPELINE COMPLETED SUCCESSFULLY '
            echo '========================================='
        }

        failure {
            echo '========================================='
            echo ' CI PIPELINE FAILED '
            echo '========================================='
        }
    }
}