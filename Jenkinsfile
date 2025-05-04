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
        
        // Make sure port 5000 is open in the security group for internal network access before running the test.
        stage('Test Docker Container') {
            steps {
                sh '''
                    set -e
                    echo "Running container from image..."

                    CONTAINER_ID=$(docker run -d \
                        -e DB_NAME=todo \
                        -e DB_USER=myuser \
                        -e DB_PASSWORD=pass \
                        -e DB_HOST=172.31.42.36 \
                        -p 5000:5000 \
                        netanelbukris/to_do_list:12)

                    echo "Waiting for container to start..."
                    sleep 20

                    echo "Checking if container is running..."
                    if ! docker inspect -f '{{.State.Running}}' $CONTAINER_ID | grep -q true; then
                        echo "ERROR: Container is not running!"
                        EXIT_CODE=$(docker inspect -f '{{.State.ExitCode}}' $CONTAINER_ID)
                        echo "Exit code: $EXIT_CODE"
                        docker logs $CONTAINER_ID
                        docker rm -f $CONTAINER_ID
                        exit 1
                    fi

                    echo "Container is running successfully."

                    curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q 200 || {
                        echo "ERROR: App did not respond with 200 OK"
                        docker logs $CONTAINER_ID
                        docker rm -f $CONTAINER_ID
                        exit 1
                    }

                    docker rm -f $CONTAINER_ID
                '''
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
