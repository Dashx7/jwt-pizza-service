# Peer Pen Test - Josh Wiseman, Matheus Plinta

# Self attack

## Matheus Plinta
- After reviewing my source code, I found two exploitable vulnerabilities.

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 11, 2025                                                          |
| Target         | pizza.matheusplinta.com                                               |
| Classification | SQL Injection                                                             |
| Severity       | 3                                                                      |
| Description    | SQL injection in the updateUser endpoint, able to arbitrarily change information in the user table. |
| Images         | [SQL Injection vulnerability image](1.jpeg) |
| Corrections    | Change query to use parameters instead of directly passing the arguments in the query string. |

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 11, 2025                                                          |
| Target         | pizza.matheusplinta.com                                               |
| Classification | Known Security Issue                                                          |
| Severity       | 2                                                                      |
| Description    | Database initialization function creates a known default admin user that can be exploited. |
| Images         | [Security issue vulnerability image](2.jpeg) |
| Corrections    | Ensured to run init.js to create a different user other than the default one in the GitHub Actions pipeline. |


## Josh Wiseman
- After searching through my own source, I was able to identity two main weaknesses.

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 12, 2025                                                          |
| Target         | pizza.joshwiseman.click                                               |
| Classification | SQL Injection                                                              |
| Severity       | 3                                                                      |
| Description    | SQL injection, was able to change someone else information without proper admin authentication.         |
| Corrections    | Sanitized the inputs to the update user API                                                 |

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 11, 2025                                                          |
| Target         | pizza.joshwiseman.click                                               |
| Classification | Known Security Issue                                                              |
| Severity       | 2                                                                      |
| Description    | By using known generics from the script one could log into the a@jwt.com admin         |
| Corrections    | Changed script to prevent known / generic default admin, and changed the current admin       |


# Peer attack records
## Josh attacking Mat:
|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 14, 2025                                                          |
| Target         | pizza.matheusplinta.com                                                |
| Classification | SQL Injection                                                              |
| Severity       | 3                                                                      |
| Description    | SQL injection, was able to change Mat's users without proper admin authentication.         |
| Corrections    | After letting me hit the vulnerable endpoint he switched it out for the hardened code stopping the attack                                                |

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 14, 2025                                                          |
| Target         | pizza.matheusplinta.com                                               |
| Classification | Known Security Issue                                                              |
| Severity       | 2                                                                      |
| Description    | Was able to use known generics from the script I logged into a@jwt.com admin         |
| Corrections    | After hitting the user, he altered the admins' info       |

## Mat attacking Josh:
|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 14, 2025                                                          |
| Target         | pizza.matheusplinta.com                                                |
| Classification | SQL Injection                                                              |
| Severity       | 3                                                                      |
| Description    | SQL injection, was able to change Josh's admin user to have an attacker-chosen password. [Script](penetrationScript.py)         |
| Images         | [SQL injection attack image](4.jpeg) |
| Corrections    | Josh implemented SQL sanitization by using parameters in the query, stopping me in my tracks.  |

|  Item           | Result                                                                 |
|----------------|------------------------------------------------------------------------|
| Date           | April 14, 2025                                                          |
| Target         | pizza.matheusplinta.com                                               |
| Classification | Known Security Issue                                                              |
| Severity       | 2                                                                      |
| Description    | Logged in using the default user a@jwt.com with its default password from the class instructions. [Script](penetrationScript.py) |
| Images         | [Default credentials attack image](3.jpeg) |
| Corrections    | Changed the default user in the initialization script to use different credentials. |


Combined summary of learnings

After running through the pen testing we learned a few things
- Sanitizing SQL is critical. Not using ? in SQL queries just gives the attack free reigns to first look at the dumped stack, and then to be able to get information from or destroy the database
- Be mindful of how much your system is known. Having public code (or shared code in our case) means that it very simple for white box hacking. Although it is security through obfuscation, not letting hackers see source code makes black box testing much harder
- XSS only works if the information is treated as innerHTML, document.write(), or eval(), and doesn't work when interpreted as just plaintext
- Pen testing is hard. Without having consistent practice it can be difficult to break into applications.
