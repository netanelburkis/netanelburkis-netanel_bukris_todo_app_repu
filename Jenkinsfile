pipeline {
    agent any

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
                        docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                        docker tag myapp $DOCKER_USERNAME/to_do_list:latest
                        docker push $DOCKER_USERNAME/to_do_list:latest
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
