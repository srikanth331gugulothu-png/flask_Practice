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
                withPythonEnv('python3') {
                    sh '''
                        python --version
                        pip --version
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                withPythonEnv('python3') {
                    sh '''
                        python -m pytest -v
                    '''
                }
            }
        }

        stage('Code Quality') {
            steps {
                withPythonEnv('python3') {
                    sh '''
                        python -m pylint app.py || true
                    '''
                }
            }
        }

        stage('Security Scan') {
            steps {
                withPythonEnv('python3') {
                    sh '''
                        python -m bandit -r app.py
                    '''
                }
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