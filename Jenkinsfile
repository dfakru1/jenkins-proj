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
                sudo apt update && sudo apt install -y python3-venv python3-pip python3-full
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
        stage('Install Docker') {
            steps {
                sh '''
                # Check if docker exists
                if ! command -v docker &> /dev/null
                then
                    echo "Installing Docker..."
                    sudo apt update
                    sudo apt install -y docker.io
                    sudo usermod -aG docker $USER
                    sudo systemctl enable docker
                    sudo systemctl start docker
                else
                    echo "Docker already installed"
                fi

                # Verify docker
                docker --version
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
