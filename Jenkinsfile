pipeline {
    agent any
    environment {
        IMAGE_NAME = 'to_do_list'
    }
    stages {
        stage('Build docker image') {
            steps {
                echo 'Building docker image...'
                sh '''
                    docker build -t myapp ./app
                '''
            }
        }

        stage('Run up with Docker compose') {
            steps {
                echo 'Running Docker compose up...'
                sh '''
                    docker compose down || true
                    docker compose up -d 
                '''    
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r ./tests/requirements.txt
                    pytest --maxfail=1 ./tests
                '''    
            }
        }    

        stage('Push Docker image') {
            steps {
                echo 'Pushing Docker image...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login --username foo --password-stdin
                        docker tag myapp $DOCKER_USERNAME/$IMAGE_NAME:latest
                        docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
                    '''
                }
            }                       
        }  
    }

    post {
        always {
            echo 'Cleaning up...'
            sh '''
                docker compose down || true
                docker rmi myapp || true
            '''
        }
    }
}
