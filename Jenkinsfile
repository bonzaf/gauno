pipeline {
    agent any

    environment {
        ANSIBLE_CONFIG = "${WORKSPACE}/ansible.cfg"
        VIRTUAL_ENV = "${WORKSPACE}/venv"
        PYTHON = "${VIRTUAL_ENV}/bin/python"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/bonzaf/gauno.git'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
		sh '${WORKSPACE}/venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Ansible Playbook') {
            environment {
                VAULT_PASSWORD = credentials('290f0e1c-a844-4983-99c9-5dcb0d21c2e0') // 'vault-password-id' - это ID ваших учетных данных в Jenkins
            }
            steps {
                script {
                    // Create a temporary file to store the vault password
                    def vaultPasswordFile = "${WORKSPACE}/vault_password.txt"
                    writeFile file: vaultPasswordFile, text: VAULT_PASSWORD
                    sh "chmod 600 ${vaultPasswordFile}"
                    
                    ansiblePlaybook(
                        colorized: true,
                        credentialsId: '290f0e1c-a844-4983-99c9-5dcb0d21c2e0',
                        disableHostKeyChecking: true,
                        installation: 'Ansible',
                        inventory: 'ansible/inventory/hosts.yml',
                        playbook: 'ansible/playbooks/rolePB_xr_intf.yml',
                        extraVars: [
                            "ansible_vault_password_file": vaultPasswordFile
                        ]
                    )
                }
            }
        }
        stage('Update NetBox') {
            steps {
                sh '${PYTHON} netbox/scripts/update_netbox.py'
            }
        }
    }
    post {
        success {
            script {
                // Merge changes to master branch
                sh 'git checkout master'
                sh 'git merge main'
                sh 'git push origin master'
            }
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}

