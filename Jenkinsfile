pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = 'abomination14'
        IMAGE_NAME      = 'student-calculator'
        GIT_COMMIT_SHA  = 'YWJvbWluYXRpb24xNDp5b3VyX2NvcGllZF9kb2NrZXJfaHViX3Rva2Vu'
        // Paste your base64 alphanumeric token string inside the single quotes below
        DOCKER_AUTH_B64 = 'PASTE_YOUR_BASE64_STRING_HERE'
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
                echo 'Executing Automated Unit Tests...'
                bat "python -m pytest test_app.py -v"
            }
        }
        stage('Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker build -t abomination14/student-calculator:%GIT_COMMIT_SHA% .'
                    // The pipe (|) must immediately follow the variable to avoid passing whitespace in cmd
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push abomination14/student-calculator:%GIT_COMMIT_SHA%'
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
