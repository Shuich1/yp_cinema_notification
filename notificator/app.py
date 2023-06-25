from flask import Flask, current_app
from src.config import settings
from src.utils.app_factory import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from src.time_action import on_time
import atexit

app = create_app(settings)


@app.route("/")
def index():
    return "Hello to Flask!"


def start_scheduler():
    sched = BackgroundScheduler(daemon=True)

    def send_by_time():
        app.logger.INFO("Executing sending by time")
        with app.app_context():  # Because we use flask
            try:
                on_time()
            except Exception as e:
                app.logger.error(f"Error in scheduler: {str(e)}")

    sched.add_job(send_by_time, "interval", minutes=1)
    sched.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: sched.shutdown())


if __name__ == "__main__":
    start_scheduler()  # <- Scheduler starts here
    app.run(use_reloader=False)  # Important to use use_reloader=False else the scheduler task will run twice.
