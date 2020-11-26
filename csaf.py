from app import create_app, db
from app.models.advisory import Advisory


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Advisory': Advisory
    }
