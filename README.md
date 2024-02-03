# Rocket Club Graphical Interface

## Description
This web-based GUI is designed for the Rocket Club to easily visualize and analyze rocket flight data. Users can plot graphs based on CSV data, view flight profiles, motor thrust, and stability over time.

## Features
- Import CSV data files.
- Plot various graphs: Flight Profile, Motor Thrust, Stability vs Time.
- Interactive data visualization.
- User-friendly web interface.

## Setting up a virtual environment

To ensure a consistent environment for all users, it's recommended to use a virtual environment. Here's how to set it up:

1. Install virtualenv: `pip install virtualenv`
2. Create a virtual environment: `virtualenv venv`
3. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On Unix or MacOS: `source venv/bin/activate`
- GitBash on Windows: `source venv/Scripts/activate`
6. Once the virtual environment is activated, install the required packages: `pip install -r requirements.txt`
- If on Windows you must install the following package manually with: `pip install waitress`

## How to Use - OnRead

1. On Linux ```gunicorn mysite.wsgi:application``` to locally run the server
2. On Windows ```waitress-serve --listen=127.0.0.1:8080 mysite.wsgi:application``` to locally run the server

## Examples
[Include screenshots or examples of the tool in use]

## Contributing
We welcome contributions! Please read our contribution guidelines.

## Credits
Thanks to [contributors names] and [third-party libraries used].

## Contact
For support or queries, contact us at [email].

## License



