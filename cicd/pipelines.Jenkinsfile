pipeline {
    agent any

	environment {
    	CI_REGISTRY='registry.gitlab.com'
		CI_REGISTRY_IMAGE='registry.gitlab.com/iharijoana/deepface-rest:latest'
    }

    stages {
		stage('Build image') {
		    steps {
				sh 'echo "Build image...."'
				sh 'echo "CI_REGISTRY_IMAGE=${CI_REGISTRY_IMAGE}"'
				sh 'docker login -u jenkins-ci -p ${CI_BUILD_TOKEN} ${CI_REGISTRY}'
				sh 'docker pull ${CI_REGISTRY_IMAGE} || true'
				sh """
                    docker build --cache-from ${CI_REGISTRY_IMAGE} -t ${CI_REGISTRY_IMAGE} .
				"""
			}
		}
		stage('Push image') {
			steps {
			    sh 'echo "Push image...."'
				sh 'docker push ${CI_REGISTRY_IMAGE}'
			    sh 'docker logout ${CI_REGISTRY}'
		    }
		}
		stage('Deploy App') {
		    steps {
    		    sshPublisher(
					publishers: [
						sshPublisherDesc(
							configName: 'facematching_server', 
							transfers: [
								sshTransfer(
									cleanRemote: false, 
									excludes: '', 
									execCommand: 'docker-compose -f docker-compose.yml pull && docker-compose -f docker-compose.yml up -d --force-recreate', 
									execTimeout: 120000, 
									flatten: false, 
									makeEmptyDirs: false, 
									noDefaultExcludes: false, 
									patternSeparator: '[, ]+', 
									remoteDirectory: '', 
									remoteDirectorySDF: false, 
									removePrefix: 'cicd/', 
									sourceFiles: 'cicd/docker-compose.yml'
								)
							], 
							usePromotionTimestamp: false, 
							useWorkspaceInPromotion: false, 
							verbose: true
						)
					]
				)
		    }
		}
    }
}