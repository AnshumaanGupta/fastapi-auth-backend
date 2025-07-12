#!/bin/bash

# Server management script for Backend Authentication API

case "$1" in
    start)
        echo "🚀 Starting Backend Authentication API..."
        systemctl start backendauth
        systemctl status backendauth
        ;;
    stop)
        echo "🛑 Stopping Backend Authentication API..."
        systemctl stop backendauth
        ;;
    restart)
        echo "🔄 Restarting Backend Authentication API..."
        systemctl restart backendauth
        systemctl status backendauth
        ;;
    status)
        echo "📊 Backend Authentication API Status:"
        systemctl status backendauth
        ;;
    logs)
        echo "📝 Backend Authentication API Logs:"
        journalctl -u backendauth -f
        ;;
    test)
        echo "🧪 Testing API endpoints..."
        python3 test_api.py
        ;;
    update)
        echo "🔄 Updating application..."
        systemctl stop backendauth
        # Files should be uploaded via SCP before running this
        source venv/bin/activate
        pip install -r requirements.txt
        systemctl start backendauth
        systemctl status backendauth
        ;;
    setup-db)
        echo "🗄️ Setting up database..."
        source venv/bin/activate
        python3 setup_database.py
        ;;
    *)
        echo "Backend Authentication API Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|test|update|setup-db}"
        echo ""
        echo "Commands:"
        echo "  start     - Start the API service"
        echo "  stop      - Stop the API service"
        echo "  restart   - Restart the API service"
        echo "  status    - Show service status"
        echo "  logs      - Show live logs"
        echo "  test      - Test API endpoints"
        echo "  update    - Update and restart service"
        echo "  setup-db  - Initialize database tables"
        exit 1
        ;;
esac

exit 0
