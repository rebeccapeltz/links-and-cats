# final-project

## Data
There is a many to many relationship between links and categories.  To bootstrap the data you can run these scripts in this order.
1. create.py  Create the database  This script will drop all tables before creating
2. data/populate_user.py  Create a user
3. data/import_categories.py  Import categories from categories.csv
4. data/populate_links.py Add links their categories

If you want to manually delete data from tables, open a SQL window (pgAdmin 4)
`delete from delete from link_category`
`delete from categories`
`delete from links`
`delete from users`



## Create Database
1. Navigate to https://www.heroku.com/, and create an account if you don’t already have one.
1. On Heroku’s Dashboard, click “New” and choose “Create new app.”
Give your app a name, and click “Create app.”
1. On your app’s “Overview” page, click the “Configure Add-ons” button.
1. In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
1. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
1. Now, click the “Heroku Postgres :: Database” link.
1. You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. 