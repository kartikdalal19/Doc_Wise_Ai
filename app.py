import sys
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(
    0,
    os.path.join(BASE_DIR, "backend")
)


from backend.app import app


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=7860
    )