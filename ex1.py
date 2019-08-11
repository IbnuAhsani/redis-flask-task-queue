from flask import Flask, request
import redis
from rq import Queue
import time

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def background_task(n):

    delay = 2
    
    print("Task running")
    print("Simulating {} second delay".format(delay))

    time.sleep(delay)

    print(len(n))
    print("Task complete!")

    return len(n)

@app.route("/task")
def add_task():

    if request.args.get("n"):

        job = q.enqueue(background_task, request.args.get("n"))

        q_len =  len(q)

        return "Task {} added to queue at {}. {} tasks in the queue".format(job.id, job.enqueued_at, q_len)

    return "No value for n"

if __name__ == "__main__":

    app.run()