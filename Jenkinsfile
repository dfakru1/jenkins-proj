pipeline{
    agent any
    stages{
        stage('checkout'){
            steps{
                git branch : 'main',
                url:"https://github.com/dfakru1/jenkins-proj.git"
            }

        }
        // stage('Debug Python') {
        //     steps {
        //         sh '''
        //         which python3
        //         python3 --version
        //         which pip
        //         pip --version
        //         '''
        //     }
        // }
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
