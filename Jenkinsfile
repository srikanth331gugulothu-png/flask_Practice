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

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    . venv/bin/activate
                    python --version
                    pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest -v
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pylint app.py || true
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m bandit -r app.py
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
            echo 'CI PIPELINE FAILED'
        }
    }
}