# set the runtime language. Python workers use "python"
runtime "python"
name "user_info"
full_remote_build true
pip "pymongo"
pip "requests"
pip "iron-mq"
# exec is the file that will be executed:
exec "pyworker.py"