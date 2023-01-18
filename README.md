# AllTheatreJobs
A web scraping tool for collating all backstage technical theatre jobs. This runs on my raspberry Pi at home.

The aim of this code is to create listings of job advertisments from the following sources:
Curtain Call    --ACTIVE.  
The Stage       --WAS ACTIVE- My IP has been blocked and they aren't answering my calls.  
Arts Jobs       --ACTIVE.  

Anything still open with a closing date is reposted weekly. Anything without a closing date is only posted once.

This project involves: 
Web scraping.
Data collection, cleaning.
Data storage.
Accesible data access in Google Sheets

The process is:  
  Data scraping using Selenium in Python  
  Data is cleaned and filtered so we only save data we need and don't waste space. 
  Data storage in an SQL Database on my personal server.
  Data is uploaded via Google's API to a Google Sheets doc where anyone can access it in a semi-readible format.
  
Possible future additions to the setup could be:  
  Automated removal of entries which have been seen before (and forgotten to be taken down)  
  Automated removal of duplicate entries (same job on 2 different sites)  
  Automated filtering of data.  (Somewhat possible with the new more accessible Google Sheets file)
  Creation of pipeline for manual review of job ads. (Simple formatting checks,
  Automated formatting of approved jobs.  
  Post to twitter!
