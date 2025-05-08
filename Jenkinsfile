pipeline {
   agent any
    environment {
        IMAGE_NAME = 'netanelbukris/to_do_list'
        VERSION = "${BUILD_NUMBER}"
        email = 'netanel.nisim.bukris@gmail.com'
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST_STAGE = '172.31.45.253'
        DB_HOST = '172.31.42.36'

    }
    stages {
        stage('Build Docker Image') {
            when { not {branch 'main'} }
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
            when { not {branch 'main'} }
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
        
        stage('Run up with Docker Compose') {
            when { not {branch 'main'} }
            steps {
                echo 'Running Docker Compose up...'
                sh '''
                    docker compose down || true
                    docker compose up -d 
                '''    
            }
        }

        stage('container check') {
            when { not {branch 'main'} }
            steps {
                echo 'Checking if containers are running...'
                sh '''
                    # Check if myapp container (based on image) is running
                    if ! docker ps | grep "myapp"; then
                        echo "ERROR: Docker container with image 'myapp' not found!"
                        exit 1
                    fi

                    # Check if mysql container (based on image) is running and healthy
                    if ! docker ps | grep "mysql:8.0" | grep -q "healthy"; then
                        echo "ERROR: Docker container with image 'mysql:8.0' is not healthy or not running!"
                        exit 1
                    fi

                    # Check if nginx container (based on image) is running
                    if ! docker ps | grep "nginx:latest"; then
                        echo "ERROR: Docker container with image 'nginx:latest' not found!"
                        exit 1
                    fi

                    echo "All containers are running successfully."
                '''
            }
        }

        stage('Run Tests') {
            when { not {branch 'main'} }
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

        // 🔒 Stage to test that credentials are properly masked in Jenkins logs.
        // Make sure:
        // 1. The "Mask Passwords" plugin is installed (Manage Jenkins → Plugin Manager).
        // 2. Jenkins was restarted after installing the plugin.
        // 3. The credentialsId ('DB_PASS') is correctly configured under Jenkins → Credentials.
        // 4. Passwords are only used or echoed inside withCredentials {} blocks.
        // 5. In the Console Output, the actual password should appear as ******** (masked), not in plain text.
        // 6. The password should not be echoed or logged outside the withCredentials {} block.
        // 7. Avoid printing the password in any post or error section to ensure masking.
        stage('Test Mask Password') {
            when { not { branch 'main' } }
            steps {
                echo 'Testing Masked Password Output...'
                withCredentials([usernamePassword(credentialsId: 'DB_PASS', passwordVariable: 'DB_PASSWORD', usernameVariable: 'DB_USERNAME')]) {                    
                    sh('echo 🔐 DB Username is: ' + DB_USERNAME)
                    sh('echo 🔐 DB Password is: ' + DB_PASSWORD)                    
                }
                echo 'Masked Password Test Completed.'
            }
        }

        stage('Push Docker Image') {
            when { not {branch 'main'} }
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

        stage('Deploy to staging') {
            when { not {branch 'main'} }
            steps {
                    // Requires "SSH Agent" plugin in Jenkins:
                    // Manage Jenkins → Plugin Manager → Install "SSH Agent"
                    echo 'Deploying to staging...'
                    // Note: Make sure the remote user (ubuntu@...) is in the "docker" group
                    // Run on remote server: sudo usermod -aG docker ubuntu
                    // Then reconnect SSH or run: newgrp docker
                    // Without this, you'll get "permission denied" when running docker
                    withCredentials([usernamePassword(credentialsId: 'DB_PASS', passwordVariable: 'DB_PASSWORD', usernameVariable: 'DB_USERNAME')]) {
                    sshagent (credentials: ['ubuntu-frankfurt']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST_STAGE} \\
                            "docker pull ${IMAGE_NAME}:${VERSION} && \\
                            docker rm -f myapp || true && \\
                            docker run -d --name myapp \\
                            -e DB_NAME=todo \\
                            -e DB_USER=${DB_USERNAME} \\
                            -e DB_PASSWORD=\\\${DB_PASSWORD} \\
                            -e DB_HOST=${DB_HOST} \\
                            -p 5000:5000 ${IMAGE_NAME}:${VERSION}"
                        """
                    }    
                }                                               
            }    
        }  

        stage('Create PR to main') {
            when {not {branch 'main'} }
            steps {
                echo 'Creating PR to main...'
                withCredentials([string(credentialsId: 'github-token-for-jenkinsfile', variable:'GITHUB_TOKEN')]) {
                    script {
                        def prTitle = "Merge ${BRANCH_NAME} into main ${VERSION}"
                        def prBody = "This PR merges changes from ${BRANCH_NAME} into main."    
                        def prUrl = "https://api.github.com/repos/netanelburkis/netanelburkis-netanel_bukris_todo_app_repu/pulls"
                        def json = """
                        {
                            "title": "${prTitle}",
                            "head": "${BRANCH_NAME}",
                            "base": "main",
                            "body": "${prBody}"
                        }
                        """
                        sh """
                            curl -X POST -H "Authorization: token \\${GITHUB_TOKEN}" \\
                            -H "Accept: application/vnd.github.v3+json" \\
                            -d '${json}' \\
                            ${prUrl}
                        """
                        echo "Pull request created successfully."
                    }
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
                message: "${JOB_NAME}.${BUILD_NUMBER} PASSED, link for remote host stage for checking: http://stage.netaneltodolist.wuaze.com/"
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
 
