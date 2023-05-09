# Turfie

A simple web application made to manage the so called "turfjes", a dutch student phenomenon to keep track of the number of drinks a person has to drink until he has made his faults good.

## Stack
The tech stack used in this application is
- [Flask](https://flask.palletsprojects.com/en/2.3.x/) as the web framework
- [Tortoise ORM](https://tortoise.github.io/) for DB management / as ORM framework
- [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) for template rendering
- [Poetry](https://python-poetry.org/) package manager

## Run the application
1. Install the requirements: `poetry install`
2. Enter the Poetry env: `poetry shell`
3. Change to project directory: `cd turfie`
4. Run the Flask application: `flask run` (if Flask not in path: `python -m flask run`)
5. Go to `127.0.0.1:5000` and use the application

## Some notes
This application is meant as a side project and is by no means ready for production use. The DB for instance is not safe for SQL injections and the forms are not validated with a CSRF token.
The interface of the application works well on a desktop browser, but at the current state it is unusable on a mobile device with the screen size of a smartphone.
Code quality is bad, you can even call it spaghetticode if you want.

## Contributing
If you want to improve the application or you have spotted a bug, fork the repo and create pull request.
For sensitive information you can contact me at [R.V.Gardishyan@student.tudelft.nl](mailto:R.V.Gardishyan@student.tudelft.nl)
