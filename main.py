"""

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

"""
import time

class Job():
    def __init__(self, venue=None, location=None, twitter_handle=None, job_title=None, link=None, deadline=None,
                 fee="Unknown", source = None, other_info = None):
        self.location = location
        self.twitter_handle = twitter_handle
        self.job_title = job_title
        self.link = link
        self.deadline = deadline
        self.venue = venue
        self.fee = fee
        self.source = source
        self.other_info = other_info


def Web_Scraping():
    from selenium import webdriver


    def get_login_details():
        import json
        import os

        cwd = os.getcwd()
        file_name = "config.txt"
        d = os.path.join(cwd, file_name)


        f = open(file_name,"r")
        j = json.load(f)
        return j

    password = get_login_details()["password"]
    email = get_login_details()["username"]

    driver = webdriver.Chrome()

    new_jobs = []

    # new_jobs.append(Job(venue= , location= , job_title= , link= , deadline= , fee= , source= , other_info= ))

    def Mandy():
        # Unlimited premium using dupe accounts?

        """
        Mandy rules:

        https://www.mandy.com/uk/terms-and-conditions#5

        3.4. Intellectual property and your use of content
        You may not copy, modify, distribute or commercially exploit any content (other than content provided by you) in any form or in any media, except that you may retrieve and display content on your computer and print and/or store one copy of individual pages for your internal, personal use.

        5.1. Restrictions on commercial use
        Unless you register and create a profile with us as a service provider or subscribe for our advertising Service (and pay the applicable fees) (see PART B below), you may not use the Site or any Service (including any email or communication service) to advertise, solicit or promote any products or services.


        5.2. Prohibition on unlawful use of content
        You may not make any unlawful or unauthorised use of any content, including:

        distributing to third parties any audition or casting information obtained on a Site;
        ((I mean, technical stuff is neither audition or casting infomation...))


        Summary: DO NOT link back to Mandy and then you have sourced the info from an external site, since Mandy
        allow us to follow links on their site and cannot control our use of data on other sites, we basically have
        to take all info from external sites.
        """
        pass

    # DONE
    def Curtain_Call():
        print("Starting Curtain Call")
        # https://www.curtaincallonline.com/find-jobs/
        # Curtain call does not give any fees, deadlines (sometimes put into other) or general locations.

        # Fetch data
        driver.get("https://www.curtaincallonline.com/find-jobs/")
        p_element = driver.find_elements_by_class_name("result-block")


        # print(p_element)
        results = []

        # We have to iterate through each of these while we have the page loaded, so we can get their links to more
        # info. This sort of 2 loops isn't very nice to look at but it is the most time + memory efficient as we avoid
        # unnecessary reloads.

        for job_listing in p_element:
            info = job_listing.text.split("\n")
            venue = info[1]
            source = driver.find_element_by_link_text(info[0]).get_attribute("href")
            print(f"{venue=} {source=}")
            results.append([venue,source])

        # Iterate through each job listing, loading a new page each time.
        for job_listing in results:
            driver.get(job_listing[1])
            info = driver.find_elements_by_class_name("block")[1].text.split("\n")

            venue = job_listing[0]
            job_title = info[0][info[0].find(": ") + 2:]
            link = driver.current_url
            source = "Curtain Call"
            other_info =f"{info[5]}, {info[3]}"

            new_jobs.append(Job(venue= venue, job_title= job_title, link= link, source= source, other_info= other_info))

        # Close the driver
        driver.close()

    # Open Hire does not have a website or an API. They only send out emails. We'll have to scrape their mail sent out.
    def Open_Hire():
        pass

    # DONE Uses a login & password stored in enviroment variables.
    def The_Stage():
        print("Starting The Stage Jobs")
        # https://www.thestage.co.uk/jobs/theatre-vacancies This is ALL the vacancies on their website.

        driver.get("https://www.thestage.co.uk/jobs/theatre-vacancies")
        driver.find_element_by_class_name("ceb-wrapper").find_element_by_css_selector("button").click()
        p_elements = driver.find_elements_by_class_name("job-container")

        links = []
        print("Finding all job ads on all pages.")

        def add_links(elements):

            for i in elements:
                # print(i.text)
                link = i.find_element_by_link_text("Apply").get_property("href")
                # print(link)
                links.append(link)

        page = 1
        add_links(p_elements)
        # Iterate through every page of job ads. There will always be 1 job ad on each page bcus of the 'hot job' top
        # listing.
        while len(p_elements) > 1:
            if page != 1:
                # Skips the first loop. This is so that if there were only 1 job listed on the site we wouldn't skip it.
                add_links(p_elements)
            page += 1
            driver.get(f"https://www.thestage.co.uk/jobs/theatre-vacancies?page={page}")
            p_elements = driver.find_elements_by_class_name("job-container")[1:] # The first item in the list will
            # always (I think always)

        print("Going through every individual job listing.")
        for c, job_listing in enumerate(links):
            driver.get(job_listing)
            if c == 0:

                # Wait for cookies button to open, then selects basic cookies.
                time.sleep(1)
                driver.find_element_by_id("aos-Cookie-Modal-Accept").click()

                # Put in our username and password to the login
                time.sleep(1)
                e = driver.find_element_by_id("aoLogin-email")
                e.send_keys(email)
                e = driver.find_element_by_id("aoLogin-password")
                e.send_keys(password)

                driver.find_element_by_id("aoLogin-Login").click()


            info = driver.find_element_by_class_name("job-result-preview").text.split("\n")
            print(info)
            job_title = info[0]
            venue = info[1]
            location = info[5]
            fee = info[3]
            deadline = info[8]
            other_info = info[6]



            new_jobs.append(Job(venue=venue, location=location, job_title=job_title, link=job_listing, deadline=deadline, fee=fee, source="The Stage Jobs", other_info=other_info))


        driver.close()
        pass

    # Functionally complete, altho could use a little neatening up in 1 place.
    def Arts_Jobs():
        print("Starting Arts Council (Artsjobs.org.uk)")
        # https://www.artsjobs.org.uk/arts-jobs-listings/?ne_jobs%5Bpage%5D=={page}
        #
        # This site has a few animated things coming in
        # and out so we got a few sleeps just to be sure those items have animated out of our way.
        # The actual job pages also have very little in the way of formatting. :(

        page = 1
        driver.get(f"https://www.artsjobs.org.uk/arts-jobs-listings/?ne_jobs%5Bpage%5D={page}")
        time.sleep(0.5)
        driver.find_element_by_id("ccc-reject-settings").click()
        time.sleep(0.2)

        # use to select "Theatre" as the artform (Not needed & not working)
        # checkboxes = driver.find_elements_by_class_name("formCheckbox")
        # checkboxes[10].click()
        # print(checkboxes[10].get_property("input"))

        # Arts council has put their search stuff in a form, of which Selenium can see all of APART from the Submit
        # button, which is rather essential. Some sorta hacky solution needed.
        # \/ \/ \/ Proof Selenium can't find the button \/ \/ \/
        # submit_button = driver.find_element_by_css_selector("body") # This is everything in the document
        # print(submit_button.text)

        # This clicks the Submit button. It's invisible to selenium for some reason but exists enough to be clicked.
        driver.find_element_by_id("maincol").find_elements_by_css_selector("*")[-2].click()
        time.sleep(0.1)
        p_elements = driver.find_element_by_class_name("aj-listing").find_elements_by_tag_name("li")

        all_links = []

        print("Cycling through all the pages of job entires.")
        try:
            # Would be better to replace with try with the while and a test to check if I can go to the next page.
            # Maybe look for the "next" element?

            while len(p_elements) > 0:
                for i in p_elements:
                    link = i.find_element_by_tag_name("a").get_attribute("href")
                    # print(link)
                    all_links.append(link)
                page += 1
                print(f"Going to page {page}")
                driver.get(f"https://www.artsjobs.org.uk/arts-jobs-listings/?ne_jobs%5Bpage%5D={page}")
                p_elements = driver.find_element_by_class_name("aj-listing").find_elements_by_tag_name("li")

        except:
            print("Hit an error on artsjobs.org.uk This was almost certainly due reaching the end of the jobs listed "
                  "on the main pages. We'll now go through each one individually.")


        # Poor site formatting & standardisation here. Not gonna be much data we can consistantly get.
        for c, url in enumerate(all_links):
            print("Job # ")
            driver.get(url)
            try:
                title = driver.find_element_by_tag_name("h2").text.split(",")
                if len(title) != 2:
                    assert AttributeError #Some have 3 + commas, which just causes issues.
                job_title = title[0]
                venue = title[1]
            except:
                title = driver.find_element_by_tag_name("h2").text
                job_title = title
                venue = None

            info = driver.find_element_by_class_name("aj-post-single").find_elements_by_tag_name("li")

            deadline = info[0].text[6:]
            location = info[1].text[8:]

            if "Unpaid" in info[3].text:
                fee = 0
            else:
                fee = info[3].text[11:]

            contact = info[5].text[7:]

            # print([venue,location,job_title,deadline,fee,contact])

            new_jobs.append(Job(venue= venue, location= location, job_title= job_title, link=url, deadline= deadline, fee=fee, source="ArtsJobs.org.uk", other_info=f"Contact: {contact}"))



        print("Finished ArtsJobs.org.uk")
        pass

    # Search twitter for keywords?
    def Twitter():
        pass

    # Scrape 1 single Facebook group
    def Facebook():
        pass

    # Uses google sheets. Not done in Python.
    def Manual_Entry():
        pass

    # Curtain_Call()
    # The_Stage()
    # Arts_Jobs()

    # Ensure we quit at the end, no matter what happens previously.
    driver.quit()

    for job in new_jobs:
        print(job.__dict__)

Web_Scraping()
# Filtering
# Upload to Google docs