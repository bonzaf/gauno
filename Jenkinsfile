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
                git branch: 'main', url: 'https://github.com/yourusername/your-repo.git'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '${PYTHON} -m pip install -r requirements.txt'
            }
        }
        stage('Run Ansible Playbook') {
            environment {
                VAULT_PASSWORD = credentials('vault-password-id') // 'vault-password-id' - это ID ваших учетных данных в Jenkins
            }
            steps {
                ansiblePlaybook colorized: true, credentialsId: 'your-credentials-id', disableHostKeyChecking: true, installation: 'Ansible', inventory: 'ansible/inventory/hosts.yml', playbook: 'ansible/playbooks/rolePB_xr_intf.yml', extraVars: '--vault-password-file=<(echo ${VAULT_PASSWORD})'
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

