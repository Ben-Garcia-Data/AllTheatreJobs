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

For the web scraping, data comparison & collation, Python feels like the best tool.
For the formatting, review & storage, could we use Google Sheets? Much more accessible as a front end tool.
Google sheets would also be good as a manual Entry tool (using google forms)
Perhaps we do all our data collection with Python, then just submit a Google Form via Python to get our data to Google Sheets?

Google sheets would need to have AppsScript to highlight potential duplicates for manual review.


TO DO:

Mandy
Open Hire emails
Arts Jobs (Neaten up 1 line of code)
Twitter?
Facebook

Google Sheets Upload
Apps Script Filtering ect
