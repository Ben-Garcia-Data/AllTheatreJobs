# AllTheatreJobs
A web scraping tool for collating all backstage technical theatre jobs. I have put this code onto the backburner now jobs are more abundant, I am busier and it is stably running on my server.

The aim of this code is to create listings of job advertisments from the following sources:  
Mandy           --(Not happening due to legal issues).  
Curtain Call    --ACTIVE.  
Open Hire       --Open Hire has no fixed formatting, API or website, so they are a little harder to do.  
The Stage       --(The Stage was working but has blocked me and won't answer any emails, so they are out).  
Arts Jobs       --ACTIVE.  
Facebook        --(Backstage Theatre Jobs group)  (Group has been inactive).


Then post this list of job ads onto twitter (by Tom Lightbody) with the following details:
location, job title, link, and closing date/time

E.G.

LONDON: @NegEarthLights are looking for a MOVING LIGHT TECHNICIAN: https://twitter.com/NegEarthLights/status/1407743713837789191?s=20. Deadline Unknown
{location} {twitter_handle] are looking for a {job_title}: {link}. {Deadline}

Anything still open with a closing date is reposted weekly. Anything without a closing date is only posted once.


This project involves: 
Web scraping.
Data collection, cleaning.
Data storage.
Accesible data access in Google Sheets

The current setup is:  
  Data scraping using Selenium in Python  
  Data is cleaned and filtered.  
  Data storage in an SQL Database on my personal server.
  Data is uploaded via Google's API to a Google Sheets doc where anyone can access it in a semi-readible format.
  
Possible future additions to the setup could be:  
  Automated removal of entries which have been seen before (and forgotten to be taken down)  
  Automated removal of duplicate entries (same job on 2 different sites)  
  Automated filtering of data.  (Somewhat possible with the new more accessible Google Sheets file)
  Creation of pipeline for manual review of job ads. (Simple formatting checks,
  Automated formatting of approved jobs.  
  Post to twitter!
