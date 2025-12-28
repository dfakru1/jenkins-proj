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

        stage('Sonarqube Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=jenkins-proj \
                        -Dsonar.sources=. \
                        -Dsonar.exclusions=venv/** \
                        -Dsonar.language=py \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.python.version=3.12
                    """
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
