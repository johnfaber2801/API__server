# Pokemon Card Tracker Web Server API Documentation

## [Github repository](https://github.com/johnfaber2801/API__server)

## [Github Project board](https://github.com/users/johnfaber2801/projects/3/views/1?layout=roadmap)

## ERD

Table of Contents

- Pokemon Card Tracker Web Server API Documentation.

## R1 and R2 Problem Identification and Justification

Problem to solve with the Pokémon Card Tracker is to provide collectors with a tracker for managing and organizing their collections. Collectors face challenges in keeping track of their items, especially in keeping with details such as type, rarity, set, condition, quantity, purchased price, market price, and grading for each card.
Collectors struggle to organize and manage their collections efficiently, particularly when dealing with many items. The tracker provides an organized way to input, store, and update information about each card.
Collectors value the privacy and security of their collections, especially if they own rare or valuable items. By requiring user accounts, the tracker ensures that each collector's data is private and can only be accessed by the account owner.
Offering features such as adding, viewing, updating, and removing cards encourages user engagement. The tracker provides a dynamic and interactive platform for collectors to enthusiastically manage and enjoy their hobby and enhance the overall experience of collecting by providing a secure, accessible, and user-friendly solution for managing Pokémon card collections.

## R3 Justification of the Database System

The Pokémon Card Project relies on PostgreSQL, a Relational Database Management System (RDBMS) and object-relational database system following the relational model. In this model data in the database is structured in tables, each table has rows and columns, rows contain records or data instances, and columns or attributes define the properties of the data stores in the table. Tables contain primary and foreign keys; primary key refers to a unique identifier in a table that ensures no duplication of rows, foreign keys establish a link between two tables, the foreign key in one table corresponds to the primary key in another. (Grosu. A,2023) (S. Elizabeth, 2023)
This relational database suits the project as data can be carefully organized into tables with well-defined relationships, for example, an user can have one or many Pokémon cards (one to many), also it complies with ACID (Atomicity, Consistency, Isolation, Durability), ensuring data integrity and consistency even in the situation of failures. (Grosu. A,2023)
Data stored in Pokemon_db has a consistent structure and has clear relationships such as the relationship between user, cards, and grading. In addition, domain integrity is achieved through primary and foreign keys, normalisation, and data validation rules.
The decision to leverage PostgreSQL aligns with the goal of making the Pokémon Card Project accessible to a wide audience of collectors, including those who may be entering the hobby with limited financial resources. By using an open-source RDBMS like PostgreSQL, the project aspires encourage a community to collecting and sharing information about Pokémon cards.

### Drawbacks

Drawbacks of PostgreSQL include slower query processing over terabytes of data. In comparison to NoSQL databases as Cassandra, where flexible schemas enable querying with only the necessary attributes, PostgreSQL has established schemas. This means that a query must navigate the entire schema, leading to higher processing times. (Hevo Data Inc, 2022).
Scalability will be another drawback in the scenario where PostgreSQL have incoming data in very high volumes as RDMS are built with one server and scale only will be vertically by increasing capacity with CPU, RAM, or storage. Cassandra scale horizontally, facilitating addition of serves or nodes to increase load. Horizontal scaling is faster and cheaper than vertical scaling. (Hevo Data Inc, 2022).
Cassandra schemas are flexible, its dynamic data structure facilitates the addition of new fields without schema migrations. PostgreSQL is stricter, requiring schemas migrations for new fields. (DataStax, 2023)
Cassandra shines at handling large volumes of unstructured or semi-structured data, particularly in terms of write throughput and scalability. PostgreSQL drawback handling large volumes of unstructured or semi-structured data can impact query performance. (DataStax, 2023)
PostgreSQL benefits of full ACID transaction support, ensuring data consistency and integrity. Cassandra supports lightweight transactions, but it's not designed for applications requiring strong ACID guarantees. For applications requirements of a strict transactional consistency, PostgreSQL is a better choice for our application. ( DataStax, 2023)

## R4  Identify and discuss the key functionalities and benefits of an ORM

Object-relational mapper (ORM) brings an object-oriented layer between relational databases and object-oriented programming (OOP) without having to write SQL queries. OOP uses objects within classes to model and organize code, and relational databases organize data into tables with rows and columns. This project will utilize SQLAlchemy, a widely adopted Python SQL toolkit and ORM, offering application developers comprehensive control and adaptability relating to SQL functionality. (Liang, 2021).
The advantages of using an ORM lies in productivity, achieved through the simplification of database interactions. By employing Python objects and methods, developers can perform operations on the database without the need to write SQL queries directly. Built-in CRUD methods further enhance this efficiency, streamlining the process of managing Pokemon cards within the tracker. Entities (user, cards, purchases) are represented as python objects, The ORM leverages relationships to establish connections and associations between these entities, facilitating the coherent representation and interaction of data. (Liang, 2021).
Another benefit of ORMs is the facilitation of unit testing. Since the ORM code is fully tested, developers can concentrate more on ensuring the achievement of the business logic rather than constantly modifying database operations and testing data-access code. Another advantage of ORMs is migrations, involve managing changes to the database schema over time while preserving existing data, which its ideal whether the project evolve or not. (Liang, 2021) (Barnse,2007)
ORMs offers Schema management that helps defining structure and organization of the database. where developers define the data model in code, and the ORM system generates the corresponding database schema. Additionally, ORM integrates with version control systems, ensuring that changes to the ORM are effectively tracked. This integration facilitates collaboration and ability to roll back changes when necessary. (Barnse,2007)

## R5 Document all endpoints for your API

1. /register

- HTTP Request Verb: **POST**

- Required data: email, username, password

- Expected JSON response Data: Expected '201 CREATED' response with return of data excluding 'password','id','cards',and 'is_admin'.

- Authentication methods: Bcrypt will hash the password and store the hashed password in the database.

- Description: Allows new users to register. Details will be stored in the database.

![Register](./docs/Register%20route.png)

2. /Login user

- HTTP method: **POST**

- Required data: email, password

- Expected JSON response Data: Expected '200 OK' response with return of data including JWT token, user: email, user_id, and username.

- Authentication methods: email, password mandatory fields, bcrypt will match the password enterred with the password in database, jwt will create a JWT access token attached to the logged in user.

- Description: Allows users to login. in order to add, view, update, and delete pokemon cards.

![Log in](./docs/log%20in%20route.png)

3. /Create a Pokemon Card

- HTTP method: **POST**

- Required data: name(nullable= False), type(nullable= False), set, condition(nullable= False), quantity(nullable= False), purchased_price, market_price. The default value is null for the rest.

- Expected JSON response data: Expected '201 CREATED' response with return of data including pokemon card details.

- Authentication methods: JWT (required and identity) in order to create a new Pokemon Card with user_id assigned accordignly.

- Description: Allows existing users to add a new Pokemon Card. Details will be stored in the database.

![create pokemon card](./docs/created%20card%20route.png)

4./ add grading to an existing Pokemon Card

- HTTP method: **POST**

- Required data: score, graded_by, certification

- Expected JSON response data: Expected '201 CREATED' response with return of data including pokemon card name, certification, graded_by, grading_id, and score.

- Authentication methods: JWT (required and identity) to create a grading for an existing Pokemon Card of the user.

- Description: Allow users to add grading details to an existing Pokemon Card if required.

1[graded added](./docs/grading%20added%20to%20existing%20card%20route.png)