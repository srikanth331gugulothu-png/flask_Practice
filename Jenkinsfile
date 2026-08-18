stage('Run Tests') {
    steps {
        sh '''
            echo "Starting MongoDB test container..."

            docker network create srikanth-test-network || true

            docker run -d \
                --name srikanth-mongodb-test \
                --network srikanth-test-network \
                mongo:7

            echo "Waiting for MongoDB..."

            sleep 10

            echo "Running tests..."

            docker run --rm \
                --network srikanth-test-network \
                -e MONGO_URI=mongodb://srikanth-mongodb-test:27017/test_student_db \
                srikanth-flask-app:${BUILD_NUMBER} \
                python -m pytest -v

            echo "Tests completed."

            docker stop srikanth-mongodb-test || true
            docker rm srikanth-mongodb-test || true
            docker network rm srikanth-test-network || true
        '''
    }
}