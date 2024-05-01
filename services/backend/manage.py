import os
from flask.cli import FlaskGroup
from project import app, db  # Update "your_application" with the appropriate module name

cli = FlaskGroup(app)

@cli.command("recreate_db")
def recreate_db():
    """Recreate the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database recreated.")

if __name__ == '__main__':
    cli()
