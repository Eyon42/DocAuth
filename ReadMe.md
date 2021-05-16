The purposes of this project are:
- Give me practice with building an entire site.
- Be a good portfolio piece
- Maybe become a product

# Basic Idea

## Problem:
A user (Individual or Institution) has a file, which can be a contract, certificate, code, etc. But he wants other people to get the file and be able to verify that it is the same file, totally unchanged.

## Solution:
We take the SHA256 hash of the file and put it into a database. The database entry is associated to the user's profile.

When someone gets the file and needs to verify that the file has not been modified or changed they can take the SHA256 hash of the file and check agains the database to see if said file is present. If the hash is found in the database, then it is confirmed that the file is indeed unmodified.

## Implentation
- Backend Framework: Flask
- Database: SQLite3 (SQLAlchemy allows me to easyly change this later)
- Frontend Framework: TBD (Will make the API first)
- Desktop client: Python CLI
- API: REST API
- Hashing function: SHA256

## Security risks
- Someone accessing the database
- Payload interception
- Modified client (This is more of a social engineering trouble)
- Hash colision(Hahahahash)
- 

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

## Things I need to figure out
- How to structure a REST API
- Add TLS
- Authentication
- Database security
- Database optimization.

## Decisions
- Do I keep record of verifications? (Ip addresses, devices, etc. or maybe just a count)- Keep a record
- Should I allow duplicated files in the database?(same hash)- Nope

# To-do
- Add user search and get user
- Test user features
- Create database and marshmallow schema for verification
- Implement verification functionality
- Test verification functionality