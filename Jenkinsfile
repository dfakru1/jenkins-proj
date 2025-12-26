pipeline{
    agent any
    environment{
        IMAGE_ID ="$BUILD_NUMBER"
        DOCKER_IMAGE= "dfakru/sample"
    }
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

        // stage('Install Docker') {
        //     steps {
        //         sh '''
        //         # Check if docker exists
        //         if ! command -v docker &> /dev/null
        //         then
        //             echo "Installing Docker..."
        //             sudo apt update
        //             sudo apt install -y docker.io
        //             sudo usermod -aG docker $USER
        //             sudo systemctl enable docker
        //             sudo systemctl start docker
        //         else
        //             echo "Docker already installed"
        //         fi

        //         # Verify docker
        //         docker --version
        //         '''
        //     }
        // }
        stage('Docker build'){
            steps{
                sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_ID} .'
                sh 'docker tag ${DOCKER_IMAGE}:${IMAGE_ID} ${DOCKER_IMAGE}:latest'
            }
        }
        stage('Docker Push'){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'eb21ea8d-789f-4eb7-a889-6a75dd97154d',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'

                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${DOCKER_IMAGE}:${IMAGE_ID}
                    docker push ${DOCKER_IMAGE}:latest
                    docker logout
                    '''
                }
            }
        }
        stage('Sonarqube Scan'){
            steps{
                withSonarQubeEnv('sonarqube'){
                    sh '''
                    sonar-scanner \
                        -Dsonar.projectkey=jenkins-proj \
                        -Dsonar.sources=. \
                        -Dsonar.language=py \
                        -Dsonar.python.version=3.12

                    '''
                }
            }
        }
    }


    post {
        success{
            echo 'FastAPI CI pipeline completed successfully'
        }
    }
}
