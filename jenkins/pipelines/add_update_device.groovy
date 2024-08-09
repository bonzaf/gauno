pipeline {
    agent any

    stages {
        stage('Setup Virtual Environment') {
            steps {
                script {
                    sh '''
                    #!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r /root/gauno/python/scripts/requirements.txt
                    '''
                }
            }
        }

        stage('Collect Configuration') {
            steps {
                script {
                    sh '''
                    #!/bin/bash
                    source venv/bin/activate
                    python3 /root/gauno/python/scripts/collect_conf.py /root/gauno/python/input_data/inventory_data.yaml /root/gauno/python/input_data/collect_new_dev.yaml
                    '''
                }
            }
        }

        stage('Parse Configuration') {
            steps {
                script {
                    def collectedFiles = sh(script: "ls /root/gauno/python/collected_data", returnStdout: true).trim().split('\n')
                    for (file in collectedFiles) {
                        def filePath = "/root/gauno/python/collected_data/${file}"
                        sh """
                        #!/bin/bash
                        source venv/bin/activate
                        python3 /root/gauno/python/scripts/parse_xrconf.py ${filePath}
                        """
                    }
                }
            }
        }

        stage('Upload to NetBox') {
            steps {
                script {
                    def parsedFiles = sh(script: "ls /root/gauno/python/parsed_data", returnStdout: true).trim().split('\n')
                    for (file in parsedFiles) {
                        def filePath = "/root/gauno/python/parsed_data/${file}"
                        sh """
                        #!/bin/bash
                        source venv/bin/activate
                        python3 /root/gauno/python/scripts/add_dev_netbox.py /root/gauno/python/input_data/inventory_data.yaml ${filePath}
                        """
                    }
                }
            }
        }

        stage('Sync with GitHub') {
            steps {
                script {
                    sh '''
                    #!/bin/bash
                    cd /root/gauno
                    git add .
                    git commit -m "Automated update of configuration data"
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

