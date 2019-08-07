import multiprocessing

# Worker Processes
#workers = 2
#worker_class = 'sync'

# Logging
logfile = '/home/board/logs/index.log'
loglevel = 'info'
logconfig = None
socket_path = 'unix:/run/board_index/socket'
bind = socket_path