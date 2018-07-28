from server import app
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(host='172.18.41.219', port=sys.argv[1])
    else:
        app.run(host='172.18.41.219', port=80)
