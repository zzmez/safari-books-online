## Bot for creating safari books online account

### This bot is used to create a https://learning.oreilly.com/register account.

Since the safaribooksonline site accepts "." in the account names/emails, it is possible to abuse the same gmail address.  

The mail that is going to be used is  asd@asd.com  

It will use permutation with "+".  asd+random_chars@asd.com  
Example:  
```
asd@gmail.com
asd+asd@gmail.com
asd+ads@gmail.com
...
```

### Technologies used:  
- python
- selenium, firefox driver
- database SQLalchemy (for testing purposes)
- google drive (for DB backup)

## REQUIREMENTS: 
 - pip install selenium
# safari-books-online
