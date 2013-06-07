
class InvestmentModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	investor = db.Column(db.String(80))
	image_url = db.Column(db.string(100))

	def __init__(self, investor, image_url):
		"""
		"""

	def __repr__(self):
		return "<Investment %r>" % self.investor
