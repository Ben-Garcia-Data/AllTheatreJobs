# AllTheatreJobs
A web scraping tool for collating all backstage technical theatre jobs.

The aim of this code is to create listings of job advertisments from the following sources:
Mandy
Curtain Call
Open Hire
The Stage
Arts Jobs
Twitter
Facebook (Backstage Theatre Jobs group)
Manual Entry

Remove multiple entries & manual review.


Then post this list of job ads onto twitter (by Tom Lightbody) with the following details:
location, job title, link, and closing date/time

E.G.

LONDON: @NegEarthLights are looking for a MOVING LIGHT TECHNICIAN: https://twitter.com/NegEarthLights/status/1407743713837789191?s=20. Deadline Unknown
{location} {twitter_handle] are looking for a {job_title}: {link}. {Deadline}

Anything still open with a closing date is reposted weekly. Anything without a closing date is only posted once.


The steps will be:
Web scraping
Data collection, comparison, cleaning.
Automatic fortmatting
Manual review
Manual posting

The current setup is:
  Data scraping using Selenium in Python
  Data is cleaned and filtered.
  Data storage in an SQL Database on my personal server.
  
Future additions to the setup will be:
  Automated removal of entries which have been seen before
  Automated removal of duplicate entries (same job on 2 different sites)
  Upload data to more accesible location
  Automated filtering of data.
  Manual review of data.
  Automated formatting of approved entries.
  Post to twitter! (Manually)



TO DO:

Mandy
Open Hire emails
Twitter?
Facebook # Code is written. It just needs the permission of the gorup owners.

Google Sheets Upload
Apps Script Filtering ect
