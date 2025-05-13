pipeline {
// This Jenkinsfile is for a CI/CD pipeline that builds, tests, and deploys a Dockerized application.
// It includes stages for building the Docker image, running tests, and deploying to staging and production environments.
// The pipeline uses Jenkins plugins for Docker, SSH, and Slack notifications.
   agent any
    environment {
        IMAGE_NAME = 'netanelbukris/to_do_list'
        VERSION = "${BUILD_NUMBER}"
        email = 'netanel.nisim.bukris@gmail.com'
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST_STAGE = '172.31.45.253'
        REMOTE_HOST_PRODUCTION = '172.31.39.147'
        DB_HOST = '172.31.42.36'
        GITOPS_REPO = "netanelburkis/todo_list-cd"
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
        // 3. The credentialsId ('TEST_MASK_PASSWORD') is correctly configured under Jenkins → Credentials.
        // 4. Passwords are only used or echoed inside withCredentials {} blocks.
        // 5. In the Console Output, the actual password should appear as ******** (masked), not in plain text.
        // 6. The password should not be echoed or logged outside the withCredentials {} block.
        // 7. Avoid printing the password in any post or error section to ensure masking.
        stage('Test Mask Password') {
            steps {
                echo 'Testing Masked Password Output...'
                withCredentials([usernamePassword(credentialsId: 'TEST_MASK_PASSWORD', passwordVariable: 'TEST_PASS_PASSWORD', usernameVariable: 'TEST_PASS_USERNAME')]) {                    
                    sh('echo 🔐 TEST MASCK PASS Username is: ' + TEST_PASS_USERNAME)
                    sh('echo 🔐 TEST MASCK PASS Password is: ' + TEST_PASS_PASSWORD)                    
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

        stage('Update stage version') {
            when { not {branch 'main'} }
            steps {
                echo 'Updating stage version...'
                withCredentials([usernamePassword(credentialsId: 'Branch_Sources_GitHub_Credentials', passwordVariable: 'GH_PASSWORD', usernameVariable: 'GH_USERNAME')]) {
                    script {
                        // Clone the GitOps repository
                        // Update the stage_version.txt file with the new version, commit the changes and push them
                        // The GitOps repository is assumed to be a separate repository that manages the deployment of the application.
                        sh """
                            rm -rf gitops 
                            git clone https://\${GH_PASSWORD}@github.com/${GITOPS_REPO} gitops
                            cd gitops
                            echo "${VERSION}" > stage_version.txt
                            git config user.name "jenkins"
                            git config user.email "${email}"
                            git add stage_version.txt
                            git commit -m "Update stage version to ${VERSION}"
                            git push origin main
                        """   
                    }
                }                                               
            }    
        }

        stage('Create PR to main') {
            when { not {branch 'main'} }
            steps {
                echo 'Creating PR to main...'
                withCredentials([string(credentialsId: 'github-token-for-jenkinsfile', variable: 'GH_TOKEN')]) {
                    script {
                        def prTitle = "Merge ${BRANCH_NAME} into main @${VERSION}"
                        def prBody = "This PR merges the latest changes from the ${BRANCH_NAME} branch into the 'main' branch. You can preview the deployed staging version here: http://stage.netaneltodolist.wuaze.com/"
                        def prUrl = "https://api.github.com/repos/netanelburkis/netanelburkis-netanel_bukris_todo_app_repu/pulls"
                        sh """
                            curl -X POST \
                            -H "Authorization: token \${GH_TOKEN}" \
                            -H "Accept: application/vnd.github.v3+json" \
                            -d '{ \
                            \"title\": \"${prTitle}\", \
                            \"head\": \"${BRANCH_NAME}\", \
                            \"base\": \"main\", \
                            \"body\": \"${prBody}\" \
                            }' \
                            ${prUrl}
                        """
                    }
                }
            }
        }

        stage('update production version') {
            when { branch 'main' }
            steps {
                echo 'updating production version...'
                // Extract version number from the latest Git commit message
                // The commit message should include a version number in the format @<number>
                script {
                    def version = sh(
                        script: "git log -1 --pretty=%B | grep -oE '@[0-9]+' | tr -d '@'",
                        returnStdout: true
                    ).trim()
                    
                    if (!version) {
                        error("❌ ERROR: No version number found in commit message. Make sure it includes @<number>.")
                    }

                    env.NEW_VERSION = version
                    echo "📦 Extracted version from commit: ${env.NEW_VERSION}"
                }

                withCredentials([usernamePassword(credentialsId: 'Branch_Sources_GitHub_Credentials', passwordVariable: 'GH_PASSWORD', usernameVariable: 'GH_USERNAME')]) {
                    sshagent (credentials: ['ubuntu-frankfurt']) {
                        // Clone the GitOps repository
                        // Update the production_version.txt file with the new version, commit the changes and push them
                        // The GitOps repository is assumed to be a separate repository that manages the deployment of the application.
                        sh """
                            rm -rf gitops
                            git clone https://\${GH_PASSWORD}@github.com/${GITOPS_REPO} gitops
                            cd gitops
                            echo "${NEW_VERSION}" > production_version.txt
                            git config user.name "jenkins"
                            git config user.email "${email}"
                            git add production_version.txt
                            git commit -m "Update production version to ${NEW_VERSION}"
                            git push origin main   
                        """
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
 
