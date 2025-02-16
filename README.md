
dgango cheetsheet:
1. to run server: python manage.py runserver
2. to create new app: python manage.py startapp appname

steps for rest api:
1. install drf
2. setup models
3. setup serializaers
4. set up views
5. set up - urls
6. test api

#to do
--> add read only permissions for api for unauthenticated users, that way only admin will be creating the api
-->turn off browsable api

------------------------------------BACKENDDETAILS---------------------------------
1. Contact Us Form
- [ ] Contact us section form:
    - [ ] Name
    - [ ] Email
    - [ ] Company name
    - [ ] Phone number
    - [ ] Message/inquiry
    - [ ] Product interest
    - [ ] Trigger event for firing mail in Vinson derma with relevant details ——> no need to make any models for this


Tables

1. Category
- id:primary key
- type:skincare,haircare etc
- description: 
- isActive: true/false

2.Product
-id
-name:
-descr: descr of the product
-attributes: json field for display certain fields in tabular manner in 
-category: fk to category table
-image:
-is_featured:
-created_at:

3.Clients
-id: pk
-name: name of client
-descr: descr required if any
-logo/image: image of client if present
-isActive: false/true

4.Faq
-id: pk
-que: question
-ans: answer of corresponding que
-isActive: boolean

5.Testimonials
-id
-customer name:
-feedback:
-created_at:

6.Tags
-id/slug
-name


7.BlogPost:
-id/slug
-title:
-content
-tags: one to many fields
-image
-created_at
-updated_at

