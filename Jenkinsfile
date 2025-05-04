pipeline {
    agent any
    environment {
        IMAGE_NAME = 'netanelbukris/to_do_list'
        VERSION = "${BUILD_NUMBER}"
        email = 'netanel.nisim.bukris@gmail.com'
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '172.31.39.147'
        DB_HOST = '172.31.42.36'

    }
    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build --no-cache -t myapp ./app
                    docker tag myapp ${IMAGE_NAME}:${VERSION}
                    docker tag myapp ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Verify Image Exists') {
            steps {
                echo 'Verifying Docker image exists...'
                sh """
                    if ! docker images | grep ${IMAGE_NAME}; then
                        echo "ERROR: Docker image '${IMAGE_NAME}' not found!"
                        exit 1
                    fi
                """
            }
        }

        stage('Test Docker Image Run') {
            steps {
                echo 'Testing if Docker container runs correctly from image...'
                sh """
                    set -e
                    CONTAINER_ID=\$(docker run -d -e DB_NAME=todo -e DB_USER=myuser -e DB_PASSWORD=pass -e DB_HOST=${DB_HOST} -p 5000:5000 ${IMAGE_NAME}:${VERSION})
                    sleep 10
                    if ! docker ps | grep \$CONTAINER_ID; then
                        echo "ERROR: Container failed to start!"
                        docker logs \$CONTAINER_ID
                        docker logs \$CONTAINER_ID || true
                        
                        exit 1
                    fi
                    echo "Container is running successfully."
                    docker rm -f \$CONTAINER_ID
                """
            }
        }

        stage('Run up with Docker Compose') {
            steps {
                echo 'Running Docker Compose up...'
                sh '''
                    docker compose down || true
                    docker compose up -d 
                '''    
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Creating virtual environment..."
                    python3 -m venv .venv

                    echo "Installing dependencies..."
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r tests/requirements.txt

                    echo "Running tests with pytest..."
                    .venv/bin/python -m pytest tests/
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

        stage('Deploy to Production') {
            steps {
                    // Requires "SSH Agent" plugin in Jenkins:
                    // Manage Jenkins → Plugin Manager → Install "SSH Agent"
                    echo 'Deploying to production...'
                    // Note: Make sure the remote user (ubuntu@...) is in the "docker" group
                    // Run on remote server: sudo usermod -aG docker ubuntu
                    // Then reconnect SSH or run: newgrp docker
                    // Without this, you'll get "permission denied" when running docker
                    sshagent (credentials: ['ubuntu-frankfurt']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "
                                docker pull ${IMAGE_NAME}:${VERSION} && \
                                docker rm -f myapp || true && \
                                docker run -d --name myapp -e DB_NAME=todo -e DB_USER=myuser -e DB_PASSWORD=pass -e DB_HOST=${DB_HOST} -p 5000:5000 ${IMAGE_NAME}:${VERSION}
                            "
                        """ 
                }                                               
            }
        }          
    }

    post {
        // Requires "Slack Notification" plugin in Jenkins:
        // Manage Jenkins → Plugin Manager → Install "Slack Notification"
        failure {
            slackSend(
                channel: '#jenkins',
                color: 'danger',
                message: "${JOB_NAME}.${BUILD_NUMBER} FAILED"
            )
            emailext(
                subject: "${JOB_NAME}.${BUILD_NUMBER} FAILED",
                mimeType: 'text/html',
                to: "$email",
                body: "${JOB_NAME}.${BUILD_NUMBER} FAILED"
            )
        }

        success {
            slackSend(
                channel: '#jenkins',
                color: 'good',
                message: "${JOB_NAME}.${BUILD_NUMBER} PASSED"
            )
            emailext(
                subject: "${JOB_NAME}.${BUILD_NUMBER} PASSED",
                mimeType: 'text/html',
                to: "$email",
                body: "${JOB_NAME}.${BUILD_NUMBER} PASSED"
            )
        }

        always {
            sh '''
                docker compose down || true
                docker rmi myapp || true
            '''
        }
    }
}
