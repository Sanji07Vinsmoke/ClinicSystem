import json
import threading
import socket
import logging
from datetime import date, datetime
from Models.CheckUp import CheckUp
from Models.Doctor import Doctor
from Models.LaboratoryTest import Laboratory
from Models.Patient import Patient
from Models.Prescription import Prescription
from Models.Staff import Staff
from Models.Transaction import Transaction


# Custom JSON Encoder to handle date/datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


# Configure logging
logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_CONFIG = {
    "host": "localhost",
    "database": "ClinicSystem",
    "user": "postgres",
    "password": "sphinxclub012"
}

# Socket server setup
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5433


class SocketServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.running = False
        self.server_thread = None
        self.server_socket = None

    def _send_response(self, connection, data):
        """Helper method to send JSON responses with proper encoding"""
        try:
            response = json.dumps(data, cls=CustomJSONEncoder)
            connection.sendall(response.encode())
            logging.debug(f"Sent response: {response}")
        except Exception as e:
            logging.error(f"Failed to send response: {str(e)}")
            raise

    def handle_doctor_staff(self, connection, address):
        logging.info(f"New connection from {address}")
        print(f"Connected by {address}")

        db_methods = {
            # PATIENTS
            "CREATE_PATIENT": Patient.create_new_patient,
            "GET_PATIENT_BY_ID": Patient.get_patient_by_id,
            "GET_ALL_PATIENT": Patient.get_all_patients,

            # CHECKUPS
            "CREATE_CHECKUP": CheckUp.save_checkup,
            "GET_CHECKUP_DETAILS": CheckUp.get_checkup_details,
            "GET_PENDING_CHECKUP": CheckUp.get_pending_checkups,

            # TRANSACTIONS
            "CREATE_TRANSACTION": Transaction.add_transaction,
            "GET_ALL_TRANSACTION": Transaction.get_all_transaction,
        }

        try:
            connection.settimeout(30)
            while True:
                try:
                    # Receive data
                    raw_data = connection.recv(4096).decode().strip()
                    if not raw_data:
                        logging.warning(f"Client {address} disconnected")
                        break

                    logging.debug(f"Received from {address}: {raw_data}")

                    # Parse command
                    try:
                        data = json.loads(raw_data)
                        command = data.get('command')
                        args = data.get('args', {})
                    except json.JSONDecodeError:
                        # Fallback for legacy format
                        if " " in raw_data:
                            command, args_str = raw_data.split(maxsplit=1)
                            try:
                                args = json.loads(args_str)
                            except json.JSONDecodeError:
                                args = args_str
                        else:
                            command = raw_data
                            args = {}

                    if not command or command not in db_methods:
                        raise ValueError(f"Invalid command: {command}")

                    # Execute command
                    method = db_methods[command]
                    if isinstance(args, dict):
                        result = method(**args)
                    else:
                        result = method(args)

                    # Send success response
                    self._send_response(connection, result)

                except json.JSONDecodeError as e:
                    error_msg = f"Invalid data format: {str(e)}"
                    logging.error(error_msg)
                    self._send_response(connection, {
                        "status": "error",
                        "message": error_msg
                    })
                except Exception as e:
                    error_msg = f"Error processing {command}: {str(e)}"
                    logging.error(error_msg)
                    self._send_response(connection, {
                        "status": "error",
                        "message": error_msg
                    })

        except socket.timeout:
            logging.warning(f"Connection with {address} timed out")
        except Exception as e:
            logging.error(f"Error with {address}: {str(e)}")
        finally:
            connection.close()
            logging.info(f"Connection with {address} closed")

    def _run_server(self):
        """Main server loop"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)

            logging.info(f"Server started on {self.host}:{self.port}")
            print(f"Socket server running on {self.host}:{self.port}")

            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_doctor_staff,
                        args=(conn, addr),
                        daemon=True
                    )
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    logging.error(f"Error accepting connection: {str(e)}")
                    break

        except Exception as e:
            logging.critical(f"Server error: {str(e)}")
        finally:
            if self.server_socket:
                self.server_socket.close()
            logging.info("Server socket closed")

    def start(self):
        """Start the socket server in a background thread"""
        if not self.running:
            self.running = True
            self.server_thread = threading.Thread(
                target=self._run_server,
                daemon=True
            )
            self.server_thread.start()
            logging.info("Server started")

    def stop(self):
        """Stop the server gracefully"""
        if self.running:
            logging.info("Stopping server...")
            self.running = False

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
            except:
                pass

            self.server_thread.join(timeout=5)
            logging.info("Server stopped")