from flask import Flask, request
import redis
from rq import Queue
from time import sleep


app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def backgroundTask(n):
    delay = 2
    print("Task running")
    print("Simularing", delay, "second delay")

    sleep(2)

    print(len(n))
    print("Task complete")

    return len(n)

@app.route("/task")
def addTask():

    if request.args.get("n"):
        
        job = q.enqueue(backgroundTask, request.args.get("n"))
        q_len = len(q)

        return f"Task {job.id} added to queue at {job.enqueued_at} . {q_len} takes in the queue"

    return "No value for n"



