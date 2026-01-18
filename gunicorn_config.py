import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "C:/GeniusGsm/logs/access.log"
errorlog = "C:/GeniusGsm/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "geniusgsm"

# SSL
# keyfile = "/etc/letsencrypt/live/geniusgsm.com/privkey.pem"
# certfile = "/etc/letsencrypt/live/geniusgsm.com/fullchain.pem"

# Server hooks
def on_starting(server):
    pass

def when_ready(server):
    pass

def on_exit(server):
    pass
