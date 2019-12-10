from flask.cli import FlaskGroup
import sys
from app import create_app


'''
created a new FlaskGroup instance to extend the normal CLI with commands related to the Flask app
'''
# use app factory
app = create_app() 

cli = FlaskGroup(create_app=create_app)

@cli.command('version')
def getVersion():
    print("Reefer Container simulator v0.0.11 12/02") 

if __name__ == '__main__':
    cli()