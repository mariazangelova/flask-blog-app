# Blog

## Features

* Registration & Login
* See all posts with pagination
* See post details
* Select category
* Search bar
* Add a post
* Delete a post
* Profile page
* Change password or email

## Technology

### Python3, HTML5, Bootstrap, CSS, JavaScript
### SQLAlchemy & SQLite

| Tables        |
| ------------- |
| User          |
| Post          |
| Category      |
| categories_table   |


### Flask & Docker

Run the following command to create the docker image from current directory:

```bash
docker image build -t blog-app .
```
Run the docker container:

```bash
docker run -p 5001:5000 -d blog-app
```
Navigate to http://localhost:5001 in a browser to see the results.
