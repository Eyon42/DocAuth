# The purpose of this project

This is my "Toy Product". It's here to help me learn how it's like to build and manage a full software project. Also, this is currently my main portfolio piece showcasing how I work.

## Current state of the project:
- Backend REST API in Flask
  - User authentication with jwt
  - SQLite database with SQLAlchemy and migrations
  - Marshmallow Schemas for easier validation and serialization
  - Basic API endpoints
- Tests with pytest
- POSTman setup for manual API testing during developement (Not in the repo)
- Source control with Git

## Future goals:
- Celery workers for background tasks. (I'm going to build my own verification system for email and phone(Only telegram))
- Frontend with Vue.js
- Switch to PostgreSQL or another database.
- Docker Containers
- Simple Deployment on cloud
- CI/CD
- See what else can be improved

# Product description

## Problem:
A user (Individual or Institution) has a file, which can be a contract, certificate, code, etc. But he wants other people to get the file and be able to verify that it is the same file, totally unchanged.

## Solution:
We take the SHA256 hash of the file and put it into a database. The database entry is associated to the user's profile.

When someone gets the file and needs to verify that the file has not been modified or changed they can take the SHA256 hash of the file and check agains the database to see if said file is present. If the hash is found in the database, then it is confirmed that the file is indeed unmodified.

## Implentation
- Backend Framework: Flask
- Database: SQLite3 (SQLAlchemy allows me to easily change this later)
- Frontend Framework: Vue.js
- Desktop client: Python CLI
- API: REST API
- Hashing function: SHA256

## Features
- The file is never sent. The hash is calculated by the client to save network and server processing resources. (The client needs to be secure)
- Each profile has many levels of Identity certification they can archieve.
  - Email verification
  - Phone verification
  - Webpage Ownership
  - Gov. Id
  - Photo verification
  - Phone Interview
  - Physical Interview
  - Etc.
- If there's a hit in the database, the file's owner's data and level of verification will be displayed.
- Additional functionality for multi-party files can be added. This would be useful for thing like contracts, where registering the file with both profiles can be considerated as an equivalent to physically signing the contract.

## Business model
- Make institutions pay for increased levels of verification.
- Serve extra security as a service(And possibly legal accountability).
- Private databases
- Extra functions such as individual profiles associated with an institution

# Developement Notes

## General TO-DO
- Implement verification functionality
- Testing
  - Verification functionality
  - User features
  - Admin permission
  - Performance profiling on tests. The file tests are taking too long
  - Figure out how to add pytest fixtures for celery workers and the RabbitMQ instances (Maybe for that just leave the docker container running)
  - Test celery tasks
- Add check for signer-whitelist when signing
- Add option to hide verification data (While showing status)
- Continue API documentation.(Seach for a way to generate it automatically)
- Implement logging
- Begin general project documentation

## Verification methods:
For now these are the current verification methods to implement
### Automatic (Via celery workers)
- Email: send mail with ver-link
- Phone: Available as a telegram bot (No sms for now)
- Website: Meta tag
### Manual (Via admin page)
- Phone interview
- Video call (Zoom, Meet, Skype)

## Performance issues:
Files operations seem to take a long time on tests. I thought it could be the hash function, but my pc can compute about half a million per second of those.