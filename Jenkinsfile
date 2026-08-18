pipeline {
    agent any

    stages {

        stage('Python Check') {
            steps {
                pysh '''
                    import sys
                    print("Python executable:", sys.executable)
                    print("Python version:", sys.version)
                '''
            }
        }

    }
}