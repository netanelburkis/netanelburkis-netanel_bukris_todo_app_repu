pipeline {
    agent any
    environment {
        IMAGE_NAME = 'netanelbukris/to_do_list'
        VERSION = "${BUILD_NUMBER}"
        email = 'netanel.nisim.bukris@gmail.com'
    }
    stages {
        stage('Build docker image') {
            steps {
                echo 'Building docker image...'
                sh '''
                    sudo docker build -t myapp ./app
                    sudo docker tag myapp ${IMAGE_NAME}:${VERSION}
                    sudo docker tag myapp ${IMAGE_NAME}:latest
                '''
            }
        }
        stage('Run up with Docker compose') {
            steps {
                echo 'Running Docker compose up...'
                sh '''
                    sudo docker compose down || true
                    sudo docker compose up -d 
                '''    
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv .venv && \
                    . .venv/bin/activate && \
                    python3 -m ensurepip --upgrade && \  
                    pip install -r tests/requirements.txt && \
                    pytest ./tests
                '''
            }
        }    
        stage('Push Docker Image') {
            steps {
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
                sudo docker compose down || true
            '''
        }
    }
}
