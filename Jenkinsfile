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
        stage('Deploy') {
            steps {
                sh '''
                echo "Deploying application..."

                docker stop app || true
                docker rm app || true

                docker pull ${DOCKER_IMAGE}:latest

                docker run -d \
                --name app \
                -p 8000:8000 \
                --restart unless-stopped \
                ${DOCKER_IMAGE}:latest
                '''
            }
        }


    }


    post {
        success {
            echo "✅ Coverage reported to SonarQube. Quality Gate passed."
            
            emailext(
                subject: "✅ Jenkins Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <p>Build <b>SUCCESS</b></p>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Branch:</b> ${env.BRANCH_NAME}</p>
                    <p><a href="${env.BUILD_URL}">View Build</a></p>
                """,
                mimeType: 'text/html',
                to: "${MAIL_RECIPIENTS}",
                from: "Jenkins CI <${MAIL_FROM_EMAIL}>",
                attachmentsPattern: 'coverage.xml,pytest-report.xml',
                attachLog: true
            )
        }
        failure {
            echo "❌ Quality Gate failed or tests failed."
            
            emailext(
                subject: "❌ Jenkins Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <p>Build <b>FAILED</b></p>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Branch:</b> ${env.BRANCH_NAME}</p>
                    <p><a href="${env.BUILD_URL}">View Build Logs</a></p>
                """,
                mimeType: 'text/html',
                to: "${MAIL_RECIPIENTS}",
                from: "Jenkins CI <${MAIL_FROM_EMAIL}>",
                attachLog: true
            )
        }
        always {
            archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
  }
}
}
