import re
class GoogleTimeString:
	def __init__(self,time):
		# regular expression that separates all "words"
		time_list = re.findall(r"[\w']+", time)
		self.year = str(time_list[0])
		self.month = str(time_list[1])
		self.day = str(time_list[2])

	def __repr__(self):
		return self.year+"-"+self.month+"-"+self.day


