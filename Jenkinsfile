node{
    stage("Git Clone"){
        sh 'git clone https://github.com/NickMakeThing/DevOps-SimpleBlog.git'
    }
    stage('Docker build'){
        sh 'cat /proc/sys/kernel/random/uuid > random_string'
        sh 'cat random_string'
        sh 'docker build -t "nicksegal/devops-nicksblog":$(cat random_string) .' 
        sh 'docker images'
    }
    stage("Login"){
        withCredentials([string(credentialsId: 'DOCKER_PASSWORD', variable: 'PASSWORD')]){
            sh 'docker login -u nicksegal -p $PASSWORD'
        }
    }
    stage('Push Docker Image') {
        sh 'docker push nicksegal/devops-nicksblog:$(cat random_string)'
    }
    stage('Pull Image to Cluster'){
        sh '''
        export KUBECONFIG=/home/ubuntu/Downloads/kubeconfig.yaml;
        kubectl set image pod/nicksblog-pod nicksblog-container=nicksegal/devops-nicksblog:$(cat random_string)
        '''
        sh 'rm -rf *'
    }
}
