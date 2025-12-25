pipeline{
    agent any
    stages{
        stage('checkout'){
            steps{
                git branch : 'main',
                url:""
            }

        }
        stage("Install dependencies"){
            steps{
            sh 'pip install -r requirements.txt'
            }
        }
        stage('Run tests'){
            steps{
                sh 'pytest'
            }
        }
        stage('Docker build'){
            steps{
                sh 'docker build -t fast-api:1.0 .'
            }
        }
    }
    post {
        success{
            echo 'FastAPI CI pipeline completed successfully'
        }
    }
}
