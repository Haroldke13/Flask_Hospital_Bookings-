import os
from flask import current_app

class Config:
	SECRET_KEY= os.getenv('SECRET_KEY', 'do_not_show_this_to_anyone_100')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hosi_mgmt_ssm.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	

