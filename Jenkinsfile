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
                    docker compose up -d 
                '''    
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r ./tests/requirements.txt
                    pytest ./tests
                '''    
            }
        }    

    }
}
