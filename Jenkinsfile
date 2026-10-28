pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'abomination14'
        IMAGE_NAME      = 'student-calculator'
        REGISTRY_CRED   = 'docker-hub-credentials'
        GIT_COMMIT_SHA  = ""
    }
    stages {
        stage('Source Code') {
            steps {
                echo 'Checking out source code from Git...'
            }
        }
        stage('Version Control') {
            steps {
                script {
                    def gitCommit = bat(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    GIT_COMMIT_SHA = gitCommit.split()[-1]
                    echo "Current Git Commit Hash: ${GIT_COMMIT_SHA}"
                }
            }
        }
        stage('Continuous Integration') {
            steps {
                echo 'Installing dependencies and executing Automated Unit Tests...'
                bat """
                python -m pytest test_app.py -v
                """
            }
        }
        stage('Build & Push') {
            steps {
                echo 'Building Docker Image...'
                bat "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${GIT_COMMIT_SHA} ."
                
                echo 'Authenticating to Docker Hub and Pushing Image...'
                // Using withCredentials variables directly inside a secure batch execution block
                withCredentials([usernamePassword(credentialsId: REGISTRY_CRED, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    bat """
                    docker logout
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${GIT_COMMIT_SHA}
                    """
                }
            }
        }
        stage('Deployment') {
            steps {
                echo 'Updating Kubernetes Manifest and Deploying App...'
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
