pipeline{
    agent any
    stages{
        stage('checkout'){
            steps{
                git branch : 'main',
                url:"https://github.com/dfakru1/jenkins-proj.git"
            }

        }
        stage("Install dependencies"){
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run tests'){
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }
        stage('Docker build'){
            steps{
                sh 'docker build -t sample:1.0 .'
            }
        }
    }
    post {
        success{
            echo 'FastAPI CI pipeline completed successfully'
        }
    }
}
