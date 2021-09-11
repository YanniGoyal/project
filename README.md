> It is a website in which the user have to login and then he/she can talk with each other with their Own id/username and password
> Here you can add channel and can do private chat with freinds by login
> It send you message on your phone number when you are offline but don't forget while entering phone number , add country code in starting ilike  +91XXXXXXXXXX for india

I have used bcrypt for hashed password in which this is the format:

__Example:__ $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy

Where:
  $2a$: The hash algorithm identifier (bcrypt)
  10: Cost factor (210 i.e. 1,024 rounds)
  N9qo8uLOickgx2ZMRZoMye: 16-byte (128-bit) salt, Radix-64 encoded as 22 characters
  IjZAgcfl7p92ldGxad68LJZdL17lhWy: 24-byte (192-bit) hash, Radix-64 encoded as 31 characters
