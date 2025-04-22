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
                    echo $USER
                    docker build -t myapp ./app
                    docker tag myapp ${IMAGE_NAME}:${VERSION}
                    docker tag myapp ${IMAGE_NAME}:latest
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

        stage('Push Docker Image') {
            steps {
                // Requires "Docker Pipeline" plugin in Jenkins:
                // Manage Jenkins → Plugin Manager → Install "Docker Pipeline"
                echo 'Pushing Docker image...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    script {
                        docker.withRegistry('', 'docker-hub') {
                            docker.image("${IMAGE_NAME}").push("${VERSION}")
                            docker.image("${IMAGE_NAME}").push('latest')    
                        }
                    }
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
