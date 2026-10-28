pipeline {
    agent any
    environment {
        // REPLACE WITH YOUR ACTUAL DOCKER HUB USERNAME
        DOCKER_HUB_USER = 'your_dockerhub_username'
        IMAGE_NAME      = 'student-calculator'
        // Jenkins Credentials ID mapping to your Docker Hub login token
        REGISTRY_CRED   = 'docker-hub-credentials'
        GIT_COMMIT_SHA  = ""
    }
    stages {
        stage('Source Code') {
            steps {
                echo 'Checking out source code from Git...'
                // Code is pulled automatically by the Jenkins Pipeline job configuration
            }
        }
        stage('Version Control') {
            steps {
                script {
                    // Extract short Git commit hash cleanly on Windows
                    def gitCommit = bat(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    // Filter down to get only the alphanumeric hash safely
                    GIT_COMMIT_SHA = gitCommit.lines().last()
                    echo "Current Git Commit Hash: ${GIT_COMMIT_SHA}"
                }
            }
        }
        stage('Continuous Integration') {
            steps {
                echo 'Installing dependencies and executing Automated Unit Tests...'
                bat """
                pip install --user -r requirements.txt
                python -m pytest test_app.py -v
                """
            }
        }
        stage('Build & Push') {
            steps {
                echo 'Building Docker Image...'
                bat "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${GIT_COMMIT_SHA} ."
                
                echo 'Authenticating to Docker Hub and Pushing Image...'
                withCredentials([usernamePassword(credentialsId: REGISTRY_CRED, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    bat """
                    echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                    docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${GIT_COMMIT_SHA}
                    """
                }
            }
        }
        stage('Deployment') {
            steps {
                echo 'Updating Kubernetes Manifest and Deploying App...'
                // Modifies the YAML image reference placeholder with the dynamic commit hash tag
                bat """
                powershell -Command "(Get-Content deployment.yaml) -replace 'IMAGE_TAG_PLACEHOLDER', '${GIT_COMMIT_SHA}' | Set-Content deployment.yaml"
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                kubectl rollout status deployment/student-calculator-deployment --timeout=60s
                """
            }
        }
    }
}
