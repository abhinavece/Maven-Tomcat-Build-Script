'''
Improvemnets could be done - 
#1. Exit if Maven module throws and error - FIXED

#2. Open localhost webpage and refresh it after 10 seconds - DONE

#3. user input whether build GWT module.

'''

import os, time, subprocess, psutil, signal, webbrowser

localhost_url= 'http://localhost:8080/cmslite/api/lite/dummyGet'

def build_maven_modules():
	os.chdir('/Users/abhinav.singh1/development/cms-ecovillage/cms/cms.commons/cms-commons-build')
	print(os.getcwd())

	build_command = 'mvn clean install -DskipTests'

	com_var = subprocess.call(build_command, shell=True)
	print("***************** ", com_var)
	time.sleep(2)

	if com_var > 0:
		sys.exit()

	os.chdir('/Users/abhinav.singh1/development/cms-ecovillage/cms/cms.next/cms-build')

	next_var = subprocess.call(build_command, shell=True)
	print("***************** ", next_var)
	time.sleep(2)

	if(next_var >0):
		sys.exit()

def fetch_process_and_kill(app_name):
	p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
	out, err = p.communicate()

	for line in out.splitlines():
		# print(str(line))
		if str(app_name) in str(line):
			pid = int(line.split(None, 1)[0])
			print(" -------  Killed already running tomcat pid: --------", pid)
			os.kill(pid, signal.SIGKILL)

def kill_process(pid):
	if(int(pid) > 0):
		killPidCmd = "kill -9 {0}".format(pid)
		print(killPidCmd)
		try:
			# return_code = subprocess.call([killPidCmd], shell=True)
			# print("mypid >>>>>>>>>>> ", mypid)
			return_code = subprocess.Popen([killPidCmd], shell=True)
			print("Killed already running tomcat pid: ", pid, "return_code ::: ", return_code.communicate())
			time.sleep(2)
		except:
			print('Problem occured during killing pid: {0}'.format(pid))


def check_tomcat_running_and_kill_process():
	grepCmd = "ps -aef | grep catalina"

	grepResults = subprocess.check_output([grepCmd], shell=True).split()
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$. ", grepResults)

	# return;
	if(len(grepResults) > 24) :
		tomcat_pid1 = int(grepResults[24])
		tomcat_pid2 = int(grepResults[1])

		print(">>>>>>>>>>>> ", tomcat_pid1, " ::::::: ", tomcat_pid2)
		kill_process(tomcat_pid2)
		# kill_process(tomcat_pid1) #Breaks the code and exits with error code: Killed : 9 
		print("*********** DONE ***********")
	else:
		print("tomcat is not already running... ")
		time.sleep(2)

def start_tomcat_jpda_and_show_logs():
	os.chdir('/Users/abhinav.singh1/apache-tomcat-8.5.42/bin')

	tomcat_start_command = './catalina.sh jpda start'
	tomcat_logs = 'tail -f -n 100 ../logs/catalina.out'

	subprocess.Popen(tomcat_start_command, shell=True)

	subprocess.Popen(tomcat_logs, shell=True)

	time.sleep(15)
	webbrowser.open(localhost_url)


# Executing functions
build_maven_modules()

print("Checking if TOMCAT is already running ... ")
# Check if Tomcat is already running, kill the process with its ID - 
fetch_process_and_kill('tomcat')
time.sleep(2)

print("****************  Starting Tomcat *****************")
time.sleep(2)

start_tomcat_jpda_and_show_logs()



