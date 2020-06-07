#!/usr/bin/env python3

import socket, sys, os, logging, json, pickle, uuid
import server_for_given_traversal as serv
from json import JSONDecodeError
from subprocess import run, PIPE

# Including functions from parent directory
sys.path.append('../')

# Initialize base logging level
logging.basicConfig(level=logging.DEBUG)

# Declaring the Graph global variable
def make_global(graph):
    global user_graph
    user_graph = graph

# Create a unique session id for the client
def create_session_id():
    uid = uuid.uuid1()
    logging.debug("Unique Session ID: %s", uid)
    response_str = "Your session ID is " + str(uid)
    return response_str

# creates the server socket and binds it to the given address
def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    logging.info('Starting server on %s:%s' % server_address)
    sock.bind(server_address)
    return sock, server_address


# receives a message from the client in the form of a list of jsons
def receive_message(connection):
    data = pickle.loads(connection.recv(512))
    return data


def perform_lab(nodes):
    graph = init_nodes(nodes[1:])
    make_global(graph)
    init_edges(nodes[1:])
    return "created your labrinyth"

def init_nodes(edge_list):
    node_set = set()
    for entry in edge_list:
        print(entry)
        from_node = entry['from']
        to_node = entry['to']
        node_set.add(from_node)
        node_set.add(to_node)
    return serv.Graph(node_set)


def init_edges(edge_list):
    for entry in edge_list:
        from_node = entry['from']
        to_node = entry['to']
        user_graph.add_edge(from_node, to_node)

def perform_add(json):
    color = json[1]
    node = json[2]
    add_value = user_graph.add_token(node, color)
    return str(json)


def perform_move(json):
    color = json[1]
    node = json[2]
    move_value = user_graph.can_reach(color, node)
    return_message = "[\"the response to\", " + json + ", is " \
    + str(move_value) + "]"
    return return_message

def query_request(json_list_requests):
    return_message = "["
    for json in json_list_requests:
        action = json[0]
        if action == "lab":
            return_message = return_message + perform_lab(json)
        elif action == "add":
            return_message = return_message + perform_add(json)
        elif action == "move":
            return_message = return_message + perform_move(json)
        else:
            return "The requested action is not able to be performed" \
            + " by the server"
    return return_message + "]"

# sets up the server and handles the client
def initialize_server():
    user_name = "Colin"
    sock, server_address = create_socket()

    # Listen for incoming connections
    sock.listen()

    while True:
        # Waiting for a new connection
        logging.info("Waiting for a connection...")
        connection, client_address = sock.accept()

        try:
            logging.info('Connection from: %s:%s', client_address[0], \
            client_address[1])

            user_name = pickle.loads(connection.recv(512))
            connection.sendall(pickle.dumps(create_session_id()))

            # Communicate with the client
            while True:
                data = receive_message(connection)
                server_message = query_request(data)
                connection.sendall(pickle.dumps(server_message))

        finally:
            # Close connection
            logging.info('Closing connection')
            connection.close()


if __name__ == '__main__':
    initialize_server()
