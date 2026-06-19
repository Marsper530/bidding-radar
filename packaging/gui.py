"""
Bidding Radar GUI - pywebview-based desktop app
領標雷達桌面版 - 雙擊即可使用
"""
import os
import sys
import threading
import time
import webview

# Resolve bundled resources path
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
INDEX_HTML = os.path.join(FRONTEND_DIR, 'index.html')


def start_backend():
    """Start FastAPI backend in background thread."""
    import uvicorn
    from backend.main import app

    # Determine port
    port = find_free_port()

    # Store port for frontend to use
    with open(os.path.join(BASE_DIR, 'port.txt'), 'w') as f:
        f.write(str(port))

    uvicorn.run(app, host='127.0.0.1', port=port, log_level='error')


def find_free_port(start=14000, end=15000):
    import socket
    for port in range(start, end):
        try:
            s = socket.socket()
            s.bind(('127.0.0.1', port))
            s.close()
            return port
        except OSError:
            continue
    raise RuntimeError('No free port found')


def main():
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Wait for backend to be ready
    time.sleep(2)

    # Read the port
    port_file = os.path.join(BASE_DIR, 'port.txt')
    if os.path.exists(port_file):
        with open(port_file) as f:
            port = f.read().strip()
    else:
        port = find_free_port()

    # Load the frontend via backend proxy
    url = f'http://localhost:{port}'

    window = webview.create_window(
        title='領標雷達 - Bidding Radar',
        url=url,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        text_select_enabled=True,
    )

    webview.start(debug=False)


if __name__ == '__main__':
    main()
