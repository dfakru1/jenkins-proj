pipeline{
    agent any
    environment{
        IMAGE_ID ="$BUILD_NUMBER"
        DOCKER_IMAGE= "dfakru/sample"
    }
    // tools {
    //     sonarScanner 'sonar-scanner'
    // }
    // tools {
    //     sonarRunner 'sonar-scanner'
    // }
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
                pytest --cov=backend --cov-report=xml:coverage.xml
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
        stage('Sonarqube Scan') {
            steps {
                script {
                    docker.image('sonarsource/sonar-scanner-cli:latest').inside("-v $WORKSPACE:/usr/src") {
                        withSonarQubeEnv('sonarqube') {
                            sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=jenkins-proj \
                                -Dsonar.sources=. \
                                -Dsonar.language=py \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.python.version=3.12
                            '''
                        }
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Docker build'){
            steps{
                sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_ID} .'
                sh 'docker tag ${DOCKER_IMAGE}:${IMAGE_ID} ${DOCKER_IMAGE}:latest'
            }
        }
        stage('Docker Push'){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
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

    }


    post {
        success {
            echo "✅ Coverage reported to SonarQube. Quality Gate passed."
        }
        failure {
            echo "❌ Quality Gate failed or tests failed."
        }
    }
}
