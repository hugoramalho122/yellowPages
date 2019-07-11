pipeline{
    agent any
    stages{
        stage("Git-Checkout"){
            steps{
                git credentialsId: '9cb0b698-da96-47e2-b253-7d3e004cc56d', url: 'https://github.com/hugoramalho122/yellowPages.git'
                echo "Polling from github"
                
            }
        }
        stage("Sonarqube"){
            environment {
                scannerHome = tool 'SonarQubeScannerLocal'
            }
            steps {
                withSonarQubeEnv('SonarQubeLocal') {
                    sh "${scannerHome}/bin/sonar-scanner -Dsonar.host.url=${SONAR_HOST_URL}  -Dsonar.login=admin -Dsonar.password=admin -Dsonar.projectKey=teste -Dsonar.sources=."
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }


    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}