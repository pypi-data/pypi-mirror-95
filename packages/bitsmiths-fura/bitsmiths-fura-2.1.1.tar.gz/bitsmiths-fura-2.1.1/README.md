# BITSMITHS FURA #

*Fura* stands for **Function-User-Role-Authenticator**. This is the Bitsmiths common security package. It's main purpose is to
create roles, functions for various *users* in a system and track the access, logins, and provide a way for user to reset and
change their details/passwords.

Before we get started, *Fura* uses the concept of `site_id` on all if its a relational tables. A *Site* is a grouping of users and
their respective role functions. If you had to store multiple client or product login credentials, but keep them securely separate
you do that by creating multiple *sites* in the database.

The main features that *Fura* provides are:

- Site based users, roles and functions.
- The ability to dynamically added new roles and functions to users on the fly through the database.
- User login access, auditing of login, log-off, password reset attempts, and more.
- A way to authenticate user role functions and audit access attempts to various levels.
- To be combined with `mettle-braze` so you can use *Fura* for all your server-side authentication requirements.
- Send *magic urls*, *password resets* correspondence via `bitsmiths-loco` to users. Currently support *email* and *sms*.
- Provide a method to grant temporary elevated access to users.
- Provide a way for users to login via temporary tokens, passwords or ssh-keys.

This product has a dependency on:

- Mettle (`bitsmiths-mettle`)
- Bitsmiths Library (`bitsmiths-lib`)
- Bitsmiths Auditing (`bitsmiths-audit`)
- Bitsmiths Loquacious Correspondence (`bitsmiths-loco`)


**Note** that we package the generated Mettle code in this package, which means that the Mettle version required in this module is important.

## Tables & Setup ##

*Fura* is designed to use a relational database with a schema/namespace of `fura` in your database. You will need to create this schema manually.
It requires several other relational database tables.

The package provides the SQL code to create these tables. There are two ways to access the table creation SQL.

1. You can run `bs-fura -g postgresql` at the command line, this will print all the SQL to `stdout`.
2. You can import the bs_fura module and get the SQL as shown below:

```python

import bs_fura

print(bs_fura.get_table_sql('postgresql'))

```

**Note!** Currently only *postgresql* SQL is added to the package. If you want us to support another database let
us know and we will put it into the development pipeline.

### Table Configuration ###

TODO - Complete this section.

## Library Objects ##

TODO - Complete this section.
