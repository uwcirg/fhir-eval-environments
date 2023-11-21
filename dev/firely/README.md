# Firely Server
Configuration required to deploy a review version of Firely server

## Setup
Copy the default env files:

    for file in *.default; do
        cp "$file" "${file%%.default}"
    done

Copy the `.env` file default:

    cp default.env .env

Modify any `.env` files as necessary. Lines that are not commented-out are required, commented lines are optional.

## Deploy
To pull the latest configured docker images, and re-deploy services as necessary, run the following command:

    docker-compose pull && docker-compose up --detach

Note that the firely app may fail to connect to the database when both are started at the same time.

### Licensing
Firely server will not accept requests without a valid product license. Populate the file

    /license/firelyserver-license.json

with a valid `.json` license.

### Trial License
To get a firely server trial license, complete the following steps:

1. Visit the [Firely Server license page](https://fire.ly/firely-server-trial/) and enter the required information
2. Open the email from Firely and download the license file
3. Move the license to `/license/firelyserver-license.json` in the deployment location
4. Run `docker-compose restart firely` to update the service

