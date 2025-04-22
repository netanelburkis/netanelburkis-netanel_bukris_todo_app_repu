pipeline {
    agent any
    environment {
        IMAGE_NAME = "netanelbukris/to_do_list"
        VERSION = "${BUILD_NUMBER}"
    }
    stages {
        stage('Build docker image') {
            steps {
                echo 'Building docker image...'
                sh '''
                    docker build -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest ./app
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
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push ${IMAGE_NAME}:${VERSION}
                        docker push ${IMAGE_NAME}:latest
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
            '''
        }
    }
}
