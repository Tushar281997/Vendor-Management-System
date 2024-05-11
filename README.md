Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

**How to Setup Repo:**

1. Clone this repo & cd Vendor-Management-System 
2. Create Virtualenv and activate
3. Install all the required libraries using -> `pip install -r requirements.txt`
4. Run command 'python manage.py makemigrations'
5. Run command 'python manage.py migrate'
6. Run command 'python manage.py runserver', and your django application will start working
<img width="1602" alt="Screenshot 2024-05-11 at 5 52 16 PM" src="https://github.com/Tushar281997/Vendor-Management-System/assets/78564584/7b8ec132-f2cb-4c02-ad5b-1e77a4f472a7">


**To use the Database you need to create a superuser follow to below steps**

1. cd Vendor-Management-System 
2. Use the command 'python manage.py createsuperuser' to create a super user
3. Promt will be generated for asking user details like, user, email, password
4. Provide all the details and save the password
5. hit the api http://127.0.0.1:8000/admin
6. Try to login using the creds you created for super user
<img width="1788" alt="Screenshot 2024-05-11 at 5 51 12 PM" src="https://github.com/Tushar281997/Vendor-Management-System/assets/78564584/fd5f86b2-01bc-4b2d-a4ea-c8260737ced5">
   

**Test Suites**

1. Export the variable like this : `export DJANGO_SETTINGS_MODULE=vendormanagement.settings`
2. cd Vendor-Management-System/vendorapp
3. Run command 'pytest tests.py'
<img width="1596" alt="Screenshot 2024-05-11 at 5 48 36 PM" src="https://github.com/Tushar281997/Vendor-Management-System/assets/78564584/f6784cb4-6c68-459a-b000-93e326b39af8">




**The api documentation for the same is published here:**

https://documenter.getpostman.com/view/14536159/2sA3JM8N2H

**Attaching the postman collection for the reference**

[VManagement.postman_collection.json](https://github.com/Tushar281997/Vendor-Management-System/files/15282775/VManagement.postman_collection.json)
