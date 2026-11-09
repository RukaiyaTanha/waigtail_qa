
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        BASE_URL = 'http://127.0.0.1:8000'
        ADMIN_URL = 'http://127.0.0.1:8000/admin/'

        BROWSER = 'chrome'
        HEADLESS = 'true'
        TIMEOUT = '10'
        PARENT_PAGE_ID = '60'
    }

    stages {

        stage('Check Python Environment') {
            steps {
                bat '''
                    echo Checking Python installation...
                    where py
                    py -3.10 --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    if not exist .venv\\Scripts\\python.exe (
                        py -3.10 -m venv .venv
                    )

                    .venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Check Wagtail Application') {
            steps {
                powershell '''
                    $url = "http://127.0.0.1:8000/admin/"

                    try {
                        $response = Invoke-WebRequest `
                            -Uri $url `
                            -UseBasicParsing `
                            -TimeoutSec 15

                        Write-Host "Wagtail application is reachable."
                        Write-Host "HTTP Status: $($response.StatusCode)"
                    }
                    catch {
                        Write-Error "Wagtail application is not reachable."
                        Write-Error "Check that the server is running at $url"
                        exit 1
                    }
                '''
            }
        }


        stage('Run Selenium Tests') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'wagtail-admin-credentials',
                        usernameVariable: 'ADMIN_USERNAME',
                        passwordVariable: 'ADMIN_PASSWORD'
                    )
                ]) {
                    bat '''
                        if not exist reports mkdir reports
                        if not exist screenshots mkdir screenshots

                        .venv\\Scripts\\python.exe -m pytest tests/ --junitxml=reports/junit.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'reports/**, screenshots/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'Wagtail QA Automation completed successfully.'
        }

        failure {
            echo 'Wagtail QA Automation failed. Check Console Output and test reports.'
        }
    }
}
