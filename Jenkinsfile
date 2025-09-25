pipeline {
    agent any
    
    environment {
        PROJECT_NAME = 'ticket-booking'
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        BACKUP_DIR = '/home/ubuntu/backups'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Environment Check') {
            steps {
                echo 'Checking environment...'
                sh 'docker --version'
                sh 'docker compose version'  // Changed from docker-compose
                sh 'ls -la'
            }
        }
        
        stage('Stop Current Services') {
            steps {
                echo 'Stopping current services...'
                script {
                    try {
                        sh 'docker compose -f ${DOCKER_COMPOSE_FILE} down'  // Changed syntax
                    } catch (Exception e) {
                        echo 'No running services to stop'
                    }
                }
            }
        }
        
        stage('Build Images') {
            steps {
                echo 'Building Docker images...'
                sh 'docker compose -f ${DOCKER_COMPOSE_FILE} build --no-cache'  // Changed syntax
            }
        }
        
        stage('Database Backup') {
            steps {
                echo 'Creating database backup...'
                script {
                    try {
                        sh """
                            mkdir -p ${BACKUP_DIR}
                            docker compose -f ${DOCKER_COMPOSE_FILE} exec -T db pg_dump -U \$POSTGRES_USER \$POSTGRES_DB > ${BACKUP_DIR}/backup_\$(date +%Y%m%d_%H%M%S).sql
                        """
                    } catch (Exception e) {
                        echo 'Database backup failed or no existing database'
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh 'docker compose -f ${DOCKER_COMPOSE_FILE} up -d'  // Changed syntax
                
                // Wait for services to be ready
                echo 'Waiting for services to start...'
                sleep 30
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health checks...'
                script {
                    // Check if containers are running
                    sh 'docker compose -f ${DOCKER_COMPOSE_FILE} ps'  // Changed syntax
                    
                    echo 'Checking container status...'
                    sh 'docker ps'
                    
                    echo 'Health checks completed!'
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up unused Docker resources...'
                sh 'docker system prune -f'
                sh 'docker image prune -f'
            }
        }
    }
    
    post {
        success {
            echo 'Deployment completed successfully!'
            sh 'docker compose -f ${DOCKER_COMPOSE_FILE} ps'  // Changed syntax
        }
        failure {
            echo 'Deployment failed!'
            script {
                try {
                    sh 'docker compose -f ${DOCKER_COMPOSE_FILE} down'  // Changed syntax
                    echo 'Services stopped due to deployment failure'
                } catch (Exception e) {
                    echo 'Failed to stop services'
                }
            }
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}