pipeline {

	agent {
		docker {
			image 'python:3'
			reuseNode true
		}
	}

    environment { 
        CI = 'true'
    }

    stages {
		//Build basic requirements
		stage ('Initial Build') {
			steps {
				echo 'Hi, im Bob the builder. Let us build this DaBestTeam up!'
				sh "pip install -r requirements.txt"
				sh "apt-get -qq update && apt-get -qq install ssh default-jre  default-jdk -y "
			}
		}
		
		//Build Browsers
		stage ('Setup Browsers') {
			steps {
				// Chrome
				echo 'Performing Chrome Setup Stage...'
				sh 'apt update'
				sh 'apt --fix-broken -y install'
				sh 'apt install wget'
				sh 'apt-get install -fy gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils libgbm1'
				sh 'wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
				sh 'dpkg --install google-chrome-stable_current_amd64.deb; apt-get -fy install'
				
				// Firefox
				echo 'Performing FireFox Setup Stage...'
				sh 'apt-get install -y firefox-esr'
			}
		}
			
		stage ('Unit Testing, Integration Testing, and Selenium Testing') {
			parallel {
				stage('OWASP Dependency Checker') {
					steps {
							//implement lab06
							dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'dabestteam_check'
							//uncomment the below commands if theres false positive
							//dependencyCheck additionalArguments: '--format HTML --format XML' --suppression suppression.xml, odcInstallation: 'dabestteam_check'
						}
				}
				
			   stage('Unit Testing') {
				  steps {
					//implement trycatcherror here
					  echo 'Testing Phase'
						sh "export JENKINS_NODE_COOKIE=dontKillMe"
					  sh "coverage run -m pytest -k 'not test_Selenium.py'"
						echo 'Coverage Report'
						sh "coverage report"
					}
				}

				
				
				stage('Selenium Testing') {
					steps {
						sh 'pytest test/test_Selenium.py -vv --disable-warnings'
					}
				}
			}
		}

		// Helps to transfer file from Jenkins_home to Nginx WebRoot
		stage('SSH Transfer') {
			steps {
				echo 'Publishing from workspace to Nginx webroot...'
				sshPublisher(
					continueOnError: false, failOnError: true,
					publishers: [
						sshPublisherDesc(
							configName: 'dabestteam_nginx',
							verbose: true,
							transfers: [
								sshTransfer(
									cleanRemote: false,
									excludes: 'dabestteam.ini, wsgi.py, /__pycache__/**, /jenkins/**,README.md,3203_configurationlog.txt, Jenkinsfile, Dockerfile, google-chrome-stable_current_amd64.deb, startup_ps.ps1, geckodriver.log',
									sourceFiles: '**',
									remoteDirectory: ''
								)
							]
						)
					
					]
				)
			}
		}
		
		stage('Deploy') {
			when{
				expression {
					currentBuild.result == null || currentBuild.result == 'SUCCESS'
				}
			}
			steps{
				echo 'Minions out there deploying... Please wait... Their legs abit short'
				echo 'Build Succeded. One step closer to getting A'
				echo 'Harder part is doing the CD of CICD...'
				echo 'testing'
				
				echo '###Access Remote Server to restart services###'
				withCredentials([sshUserPrivateKey(credentialsId: 'sshAccess', keyFileVariable: 'sshkey', usernameVariable: 'team-19'), string(credentialsId: 'you_know_can_liao', variable: 'SECRET')]) {
						sh ('ssh -i $sshkey -o StrictHostKeyChecking=no team-19@139.59.252.115  "pip install -r /var/www/dabestteam/requirements.txt"')
						sh ('ssh -i $sshkey -o StrictHostKeyChecking=no team-19@139.59.252.115  "sudo systemctl restart dabestteam.service"')
				}
			}
		}
    } 
	post {
		success {
			echo "${env.BUILD_URL} has result: SUCCESS"
			echo '+++Cleaning Workspace+++'
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
			cleanWs()
		}
		failure {
			echo "${env.BUILD_URL} has result: FAIL"
			echo '---Cleaning Workspace---'
			cleanWs()
		}
	}
}
