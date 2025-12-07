pipeline {
    agent any // Use any available Jenkins agent

    stages {
        stage('Checkout') {
            steps {
                // This step assumes you've configured your Jenkins job to check out your Git repository
                // You can add a 'git branch: "main", credentialsId: "your-github-credential-id"' here if needed
                echo 'Source code checked out.'
            }
        }

        stage('Build and Push Images') {
            steps {
                // Ensure Docker is available on the Jenkins agent (your EC2 instance)
                
                script {
                    // Build Backend Image
                    echo 'Building Backend Image...'
                    // Tag the image with the build number for easy tracking
                    sh "docker build -t myapp-backend:${env.BUILD_NUMBER} ./Backend -f ./Backend/Dockerfile.backend"
                    
                    // Build Frontend Image
                    echo 'Building Frontend Image...'
                    sh "docker build -t myapp-frontend:${env.BUILD_NUMBER} ./Frontend -f ./Frontend/Dockerfile.frontend"
                    
                    // NOTE: Add 'docker push' commands here if you were using a Docker Registry (like Docker Hub or ECR)
                    // sh "docker push myapp-backend:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                // Stop and remove previous services, then start new ones using the current configuration
                // The `-d` flag runs the containers in detached mode (in the background)
                echo 'Tearing down old services and deploying new ones...'
                sh 'docker compose down' // Stop and remove existing containers/networks
                sh 'docker compose up -d --build' // Build and start new services
            }
        }

        stage('Clean up Old Images') {
            steps {
                script {
                    echo 'Cleaning up intermediate images...'
                    // Prune dangling images to save disk space (optional but recommended)
                    sh 'docker image prune -f'
                }
            }
        }
    }
    
    // Post-build actions for success/failure notification (optional)
    post {
        always {
            // Echo deployment status
            echo "Pipeline finished. Status: ${currentBuild.result}"
        }
        success {
            echo "Deployment successful! Access the app on your EC2 instance's public IP."
        }
        failure {
            echo "Deployment FAILED. Check build logs for errors."
        }
    }
}