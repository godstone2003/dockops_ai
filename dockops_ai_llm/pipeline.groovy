pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'  // Set AWS region
        ECR_REPO_NAME = 'dockops_ai_repo'  // ECR repository name
        IMAGE_TAG = "${env.BUILD_NUMBER}"  // Use Jenkins build number as image tag
        AWS_ACCOUNT_ID = '636167220663'  // Your AWS Account ID
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[url: 'https://github.com/godstone2003/dockops_ai.git']]
                ])
            }
        }

        stage('Authenticate with Amazon ECR') {
            steps {
                sh '''
                echo "Authenticating with Amazon ECR..."
                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Build Docker Image') {
           steps {
               sh '''
               echo "Current working directory: $(pwd)"
               ls -al
               cd dockops_ai_llm  # Navigate to the correct directory
               docker build -t $ECR_REPO_NAME:$IMAGE_TAG .
               '''
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh '''
                echo "Tagging Docker image..."
                docker tag dockops_ai_repo:$IMAGE_TAG 636167220663.dkr.ecr.us-east-1.amazonaws.com/dockops_ai_repo:$IMAGE_TAG
                '''
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh '''
                echo "Pushing Docker image to ECR..."
                docker push 636167220663.dkr.ecr.us-east-1.amazonaws.com/dockops_ai_repo:$IMAGE_TAG
                '''
            }
        }

        // New stage for Docker run
        stage('Run Docker Image') {
            steps {
                sh '''
                echo "Running Docker container on port 5000..."
                docker run -d -p 5000:5000 636167220663.dkr.ecr.us-east-1.amazonaws.com/dockops_ai_repo:$IMAGE_TAG
                '''
            }
        }
    }
}
