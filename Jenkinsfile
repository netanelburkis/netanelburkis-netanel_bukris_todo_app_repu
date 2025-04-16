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

        stage('Run up with Docker compose') {
            steps {
                sh '''
                    docker compose down || true
                    dokcer compose up -d 
                '''    
            }
        }

    }
}
