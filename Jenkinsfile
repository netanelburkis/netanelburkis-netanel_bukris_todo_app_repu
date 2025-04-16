pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
                echo 'Building...'
                sh '''
                    docker build -t myapp ./app
                '''
            }
        }
    }
}
