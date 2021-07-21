import time

# Test commit 2

class Job():
    def __init__(self, venue=None, location=None, job_title=None, link=None, deadline=None,
                 fee="Unknown", source = None, other_info = None):
        self.location = location
        self.job_title = job_title
        self.link = link
        self.deadline = deadline
        self.venue = venue
        self.fee = fee
        self.source = source
        self.other_info = other_info

def get_login_details():
    import json
    import os

    cwd = os.getcwd()
    file_name = "config.txt"
    d = os.path.join(cwd, file_name)

    f = open(file_name, "r")
    j = json.load(f)
    return j


def Web_Scraping():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver import ChromeOptions


    # driver = webdriver.Chrome(ChromeDriverManager().install()) # Not working

    from selenium.webdriver import Chrome
    print("Imported Chrome")
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 2 different ways to run. 1 for Windows, 1 for Ubuntu. This deals with the issue of chromedriver (not) being in PATH.

    from sys import platform
    print(f"Looks like we're running on {platform}")
    if "win" in platform:
        driver = Chrome(options = chrome_options,executable_path = r"C:\Users\PC\Downloads\chromedriver_win32\chromedriver.exe")
    elif "linux" in platform:
        driver = Chrome(options=chrome_options)
    else:
        print("Unknown platform")



    password = get_login_details()["password"]
    CCpassword = get_login_details()['CurtainCallPassword']
    email = get_login_details()["username"]
    fb_token = get_login_details()["fb_token"]

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

        # Login

        driver.get("https://www.curtaincallonline.com/sign-in/")

        time.sleep(1)

        driver.find_element_by_id("id_login").send_keys(email)
        driver.find_element_by_id("id_password").send_keys(CCpassword)
        driver.find_element_by_id("hs-eu-confirmation-button").click()
        driver.find_element_by_class_name("primaryAction").click()


        time.sleep(1)

        # Fetch data
        driver.get("https://www.curtaincallonline.com/find-jobs/")

        time.sleep(1)
        delay = 1
        try:
            p_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "result-block")))

        except TimeoutException:
            print("Loading took too much time!")
        #
        p_element = driver.find_elements_by_class_name("result-block")
        # print(p_element)
        results = []

        # We have to iterate through each of these while we have the page loaded, so we can get their links to more
        # info. This sort of 2 loops isn't very nice to look at but it is the most time + memory efficient as we avoid
        # unnecessary reloads.

        for job_listing in p_element:
            source = driver.find_element_by_link_text(job_listing.text.split("\n")[0]).get_attribute("href")
            # print(f"{venue=} {source=}")
            results.append(source)


        print(f"{len(results)} jobs from Curtain Call")



        # Iterate through each job listing, loading a new page each time.
        for job_listing in results:
            time.sleep(0.1)
            print(f"{job_listing}")
            driver.get(job_listing)

            role = driver.find_element_by_id("role")
            pay = driver.find_element_by_id("payment")
            extra_info = driver.find_element_by_id("job-details-about")

            role = role.text.split("\n")
            pay =  pay.text.split("\n")
            extra_info = extra_info.text.split("\n")

            job_title = role[0][9:]
            other_info = role[2][14:]
            employer = role[3][10:]
            fee = pay[0][15:]
            deadline = extra_info[2][18:]

            new_jobs.append(Job(venue= employer, job_title= job_title, link= job_listing, deadline= deadline, fee= fee, source= "Curtain Call", other_info= other_info))

    # Open Hire does not have a website or an API. They only send out emails. We'll have to scrape their mail sent out.
    def Open_Hire():
        pass

    # DONE Uses a login & password stored in enviroment variables.
    def The_Stage():
        print("Starting The Stage Jobs")
        # https://www.thestage.co.uk/jobs/theatre-vacancies This is ALL the vacancies on their website.

        driver.get("https://www.thestage.co.uk/jobs/theatre-vacancies")
        time.sleep(1)
        driver.find_element_by_class_name("ceb-wrapper").find_element_by_css_selector("button").click()
        p_elements = driver.find_elements_by_class_name("job-container")

        links = []
        # print("Finding all job ads on all pages.")

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

        print(f"{len(links)} jobs from The Stage")
        # print("Going through every individual job listing.")
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
            # print(info)
            job_title = info[0]
            venue = info[1]
            location = info[5]
            fee = info[3]
            deadline = info[8]
            other_info = info[6]



            new_jobs.append(Job(venue=venue, location=location, job_title=job_title, link=job_listing[:-1], deadline=deadline, fee=fee, source="The Stage Jobs", other_info=other_info))


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
                # print(f"Going to page {page}")
                driver.get(f"https://www.artsjobs.org.uk/arts-jobs-listings/?ne_jobs%5Bpage%5D={page}")
                p_elements = driver.find_element_by_class_name("aj-listing").find_elements_by_tag_name("li")

        except:
            print("Hit an error on artsjobs.org.uk This was almost certainly due reaching the end of the jobs listed "
                  "on the main pages. We'll now go through each one individually.")

        print(f"{len(all_links)} jobs from The Stage")
        # Poor site formatting & standardisation here. Not gonna be much data we can consistantly get.
        for c, url in enumerate(all_links):

            # print(f"link {c}")

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

            if len(info) != 6:
                print("Error. Not enough data found on page.")
                continue

            deadline = info[0].text[6:]
            location = info[1].text[8:]

            if "Unpaid" in info[3].text:
                fee = 0
            else:
                fee = info[3].text[11:]

            contact = info[5].text[7:]

            # print([venue,location,job_title,deadline,fee,contact])

            new_jobs.append(Job(venue= venue, location= location, job_title= job_title, link=url[:-1], deadline= deadline, fee=fee, source="ArtsJobs.org.uk", other_info=f"Contact: {contact}"))



        print("Finished ArtsJobs.org.uk")
        pass

    # Scrape 1 single Facebook group
    def Facebook():
        import facebook
        # https://www.facebook.com/groups/backstagetheatrejobs/
        from selenium.webdriver.common.action_chains import ActionChains

        # Using Selenium with Facebook has many flaws. Using the API would work far better.
        """
       # Use this code to create your own cookie file, logimg in manually in the browser.
        #river.get("https://www.facebook.com")
        time.sleep(60)
        pickle.dump(driver.get_cookies() ,open("cookies.pkl","wb"))


        # Login using cookies bucs Facebooks login system is a pain to navigate in html. (Presumably to discourage
        # bots like me.)
        driver.get("https://www.facebook.com/groups/backstagetheatrejobs/")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        # Occasionally this loads the wrong page, so I'm putting a 3 try loop in and then if it still won't work,
        # quitting with an error.
        def load_page():
            driver.get("https://www.facebook.com/groups/backstagetheatrejobs/")

            time.sleep(1)

            new_activity = driver.find_element_by_xpath("//*[contains(text(), 'New activity')]")
            new_activity.click()
            # print(new_activity.location)
        try:
            load_page()
            time.sleep(1)
        except:
            try:
                load_page()
                time.sleep(1)
            except:
                try:
                    time.sleep(5)
                    load_page()
                    time.sleep(1)
                except:
                    raise Exception("Tried to load page 3 times, failed 3 times. Quitting")

        # This didn't work but now it does. idk how or why but I'm not questioning it.
        most_recent = driver.find_element_by_xpath("//*[contains(text(), 'See most recent posts first')]")
        most_recent.click()

        # Wait a sec for different sort.
        time.sleep(1)


        job_listings = driver.find_element_by_css_selector('div[role="feed"]').find_elements_by_css_selector("*")


        # We need to hit every see more button

        for i in job_listings:
            body = i.find_element_by_css_selector('div[dir="auto"]')
            print(body.text)
            print("-------------------------")




        time.sleep(1000)
        """

        # If token has expired, get a new one using instructions here. Make sure to extend it.:
        # https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999
        # Must have admin perms in the group to do this.

        graph = facebook.GraphAPI(access_token=fb_token, version=3.1)

        # Test group id = 734740427307465
        # backstage theatre jobs id = 13011899629

        r = "/734740427307465/feed"
        events = graph.request(r)
        print(events)

        # \/ \/ \/ test data \/ \/ \/
        # events = {'data': [{'updated_time': '2021-07-02T11:34:47+0000', 'message': 'POSITION: Venue Technician (Stage Management and AV based) \nRATE OF PAY: £22030+ per annum \nDATES: Closing Date 2nd July, Interviews 7th and 8th of July\nLOCATION: Wellington College, Crowthorne, Berkshire\nDESCRIPTION: The College’s Technical team ensures the smooth running of all technical aspects of events that are held in several spaces across the college site, including a relatively new 900+ seated performing arts centre. We put on In-House shows, talks, assemblies, orchestral recitals, conferences and much more. Join us, and you could soon be playing a vital role within our friendly pro-active team. \nAPPLY TO: https://wellingtoncollege.postingpanda.uk/job/173067 for more information and application forms.', 'id': '734740427307465_935369337244572'}, {'updated_time': '2021-07-02T11:34:22+0000', 'message': 'Position: Stage & Flys Technician \nLocation: Grand Opera House Belfast\nSalary: £31,078\nContact Type: 42hrs average per week, Permanent \nClosing Date: 19th July 2021\nhttps://www.goh.co.uk/jobs/stage-flys-technician/', 'id': '734740427307465_935369167244589'}, {'updated_time': '2021-07-02T11:34:09+0000', 'message': 'Hi Everyone, \nLooking for a lighting technician for the following dates: \n1st July - load in - 7am call\n4th July - Load out - 9am call\nLocation - \nChichester \nFee -\n£250 per day \nPlease email me at josh@palmerlighting.co.uk if interested! \nThanks all', 'id': '734740427307465_935369073911265'}, {'updated_time': '2021-07-02T11:33:57+0000', 'message': "It's a really exciting time to join us at Glyndebourne!\nWe are currently offering a wide range of roles including;\nAssistant Stage Manager\nFinance Assistant\nSenior Marketing Manager\nLearning & Engagement Manager\nMembership Operations Assistant\nVideo on Demand Project Lead\n3 roles in our Costume Department\nand a Cover Security Guard\nTake a look below for more details!\nhttps://lnkd.in/dVG24Va\n#recruitment #recruiting #jobs #hiring #jobsearch #Glyndebourne #Glyndebournejobs #eastsussexjobs #sussexjobs #nowhiring", 'id': '734740427307465_935368963911276'}, {'updated_time': '2021-07-02T11:33:46+0000', 'message': 'Technician | Beck Theatre Hayes\n2 posts available \nClosing date: Fri 9 July 2021 at 12:00am\nSalary: £20,000 - £25,000 p/a (dependant on experience)\nPurpose of the role \nProvision as required of technical (stage, electrics, projection and/or sound) support for the preparation and performance of productions and events at The Beck Theatre, and of routine maintenance of buildings and equipment, so as to ensure the highest standards of artistic quality and customer service are offered to theatregoers and other users of The Beck Theatre, and thus support of the achievement of Beck Theatre’s business, service polices and targets.\nOur ideal candidate \nWe are looking to appoint a multi-skilled Technician to ensure a smooth-running, efficient and safe working environment for all staff and visiting companies, to assist with building maintenance and to strive to offer the best possible service to all users of The Beck Theatre. \nAbout HQ Theatres & Hospitality\nThe Beck Theatre is one 12 venues within HQ Theatres & Hospitality’s (HQT&H) current portfolio of regional theatres and concert halls. HQT&H currently manages 18 auditoria on behalf of local authorities, with capacities ranging from a 200 seat arts centre to a 2,400 seated/standing theatre. Last year HQT&H programmed a total of 2,354 shows which attracted attendances of over 1.5 million.\nHQ Theatres & Hospitality (HQT&H), the UK’s second-largest venue operator, is a division of Trafalgar Entertainment.\nPlease visit the website for job description and application form.', 'id': '734740427307465_935368873911285'}, {'updated_time': '2021-07-02T11:33:14+0000', 'message': "POSITION: Lighting / Stage Technicians\nRATE OF PAY: £12/hour\nDATES: \nSaturday 3rd July 2000-0000\nMonday 5th July 0900-2200\nLOCATION: Tara Theatre, Earlsfield, SW18 4ES\nDESCRIPTION: I am looking for a number of people to help with an upcoming production week. Ideally multi-talented individuals to assist with lighting and set fit-ups, a lighting focus and babysitting tech. \nPlease get in touch even if you can't do both days.\nAPPLY TO: technical@taratheatre.com", 'id': '734740427307465_935368617244644'}, {'updated_time': '2021-07-02T11:33:06+0000', 'message': "*Posting on behalf of someone else*\nIf you wish to post a job, please post in this format\nPOSITION: Stage Manager \nRATE OF PAY: 3 weeks @ £494 p/w + £100 day rate for 10th July \nRehearsals Dates:\nSat 10 Jul, 11:00 - 18:30\nMon 12 – Sat 17 Jul, 10:30 - 18:30\nTues 20 - Fri 23 Jul, 10:30 - 18:30\nShow Dates:\n8 Shows in Greenwich Park: 24, 25, 31 July and 01 Aug, 13:00 & 15:00\n3 Shows in Garrison Church (Woolwich): 29 Jul, 13:00 & 15:00 and 30 Jul, 15:00 pm\n1 Street intervention at General Gordon Square: 31 Jul, 11:00\nRehearsal location:\n2 outdoor places in Woolwich Arsenal = Garrison Church and Wellington Park\nhttps://www.stgeorgeswoolwich.org/\nhttps://www.google.com/.../data=!4m12!1m6!3m5!1s0x0...\nIndoors (if the weather doesn't allow us to be outside): at the Tramshed (Woolwich) in bubbles of 6\nShows location: Greenwich Park and Royal Arsenal (locations as above)\nTHE PROJECT: Commedia dell’Tramshed aims at reinventing Commedia with a company of emerging performers and presenting 11 outdoor shows in the borough of Greenwich. Working with the director and technical manager to rig, op, and strike simple sound at each location, creating the book, managing props and masks etc.\nAPPLY TO: andre@tramshed.org\nThanks, all!", 'id': '734740427307465_935368580577981'}, {'updated_time': '2021-07-02T11:32:45+0000', 'message': 'POSITION: Scenic Artist\nRATE OF PAY: $18-20/hr, plus full benefits package\nDATES: Full Time\nLOCATION: 3dx Scenic, Cincinnati OH\nDESCRIPTION: 3dx Scenic is looking for an experienced Scenic Artist to join our team and execute scenic finishes for a wide range of theme park, museum, and corporate projects in our Cincinnati fabrication shop.\nAn excellent candidate must be well-versed in theatrical and display paint methodologies and procedures and be able to work with a team of professionals of different disciplines to achieve the best results. The ideal candidate will have an analytical mind, great organizational skills, a critical eye for details and aesthetics, and a desire to contribute to the success of the team and organization.\nThe goal will be to ensure all projects exceed client expectations while closely following project specifications.\nResponsibilities Include\nPrepare various types of surfaces (wood, steel, dibond, fiberglass, etc) for painting.\nExecution of all scenic treatments using HVLP spray guns, brushes, rollers, sponges, etc for both interior and exterior conditions\nAssist in the creation of paint samples and touch-up kits\nMix and match paints, varnishes, lacquers, shellacs, stains, tints, and other coatings and finishes.\nRefinish and restore previously painted projects\nAssist in maintaining all scenic records (color cards, process sheets, recipes, labels, etc)\nMaintain the safety, order, and cleanliness of all paint areas and equipment\nMaintain strict quality control on a schedule\nWork under the direction of the Charge Artist and with other team members in a collaborative shop environment\nOther duties as assigned\nRequirements\nExperience with theatrical and display scenic practices and products\nStrong knowledge of faux finishing, 3D textures, sculpting, stenciling, color mixing and matching, layout, and scaling.\nPrior experience in a professional theatrical scene shop, event fabrication facility or equivalent\nProficiency with standard shop power tools and HVLP spray guns\nWork from design renders and reference photos\nWork on multiple projects concurrently with little supervision\nExcellent organizational and time-management skills\nAbility to work overtime with advanced notice and occasionally travel on installations to complete paint treatments\nAdditional Skills\nBasic Scenic Carpentry\nSculpting\nDigital Sculpting\nAutomotive Paint Experience\nVinyl Graphic Application\n\nPhysical Demands\nThis position is active and requires standing for 6-8 hours a day, talking, bending, kneeling, stooping, crawling, and climbing. Employees are regularly required to hear and talk. Specific vision abilities required by this position include close and distance vision, color vision, peripheral vision, depth perception, and the ability to focus. This position is in a large fabrication shop, where the employee will be exposed to noise, moving mechanical parts, and fumes and airborne particles. Participation in the Respiratory Protection Program and all other Safety and PPE Programs is mandatory.\nAPPLY TO: Please submit a resume, cover letter, and examples of work through the following website: ', 'id': '734740427307465_935368320578007'}, {'updated_time': '2021-07-02T11:32:26+0000', 'message': 'POSITION: Lighting Programmer - Sleepy Hollow\nRATE OF PAY: £1200 (8 days on site)\nDATES: 16th - 27th July. A production schedule is available upon request, Lx is currently scheduled on site for 8 days.\nLOCATION: Guildford School of Acting, Guildford\nDESCRIPTION: Lighting programmer. Console is ETC Eos Ti. Rig is generics, scrollers & movers. Sleepy Hollow is a musical theatre production for our MA Musical Theatre students. Some of the technical team are current students, some are freelancers. All the creatives are freelancers. LD is John Rainsforth Previous experience of programming EOS for a musical is desired. \nAPPLY TO: Sarah Sage, Technical Manager: s.sage@surrey.ac.uk', 'id': '734740427307465_935368113911361'}, {'updated_time': '2021-07-02T11:32:16+0000', 'message': 'URGENT!\nPOSITION:\nVan Driver\nRATE  OF PAY:\n£13 per hour\nDATES:\nFriday 2nd - Wednesday 7th 09:00-17:00\nLOCATION:\nBarking, East London.\nDESCRIPTION:\nWe are looking for someone to work with us over the next few days to assist with moving equipment around for a few events that we have.\nAPPLY  TO:\naaron@cmpm.co.uk', 'id': '734740427307465_935367973911375'}, {'updated_time': '2021-07-02T11:32:08+0000', 'message': 'POSITION: Full Time Venue Technician\nRATE OF PAY: £21k to £24k commensurate with skills and experience\nDATES: Closing Date 5pm on Friday 16th July, Interviews to be held Thursday 22nd July\nLOCATION: Cliffs Pavilion and Palace Theatre, Southend-On-Sea\nDESCRIPTION: We are delighted to offer this opportunity to join our highly skilled technical team at Southend Theatres.\nSouthend Theatres consists of The Cliffs Pavilion and the Palace Theatre.  The Cliffs Pavilion is a number one touring house, playing host to West End musicals, rock gigs and everything in between.  The Palace Theatre is a traditional Edwardian theatre hosting plays, children’s theatre, live music and much more.  This is an opportunity to become part of the team behind the success!\nAs a Southend Theatres technician, you will work with a variety of people delivering fantastic shows and events and supporting a variety of departments.  You will be involved in all technical aspects of stage and events presentation, ensuring high standards of professionalism and presentation.  You will have the opportunity to put your skills and experience to good use and to learn and develop further in your trade.\nThe successful candidate will have an in-depth working knowledge of lighting and sound rigging and operation, gets ins and get outs, building sets, hemp flying, and technical health and safety. An understanding of fire safety, security requirements, and event planning is desirable. \nA key requirement of this role is a genuine desire to contribute positively and pro-actively to the success that Southend Theatres’ enjoys year after year.  If you would like join the Southend team, we would love to hear from you.\nFor an Application Form and Job Description or an informal discussion about the role, please contact:  Michael Lewins, Technical Manager  01702 350456  michaell@southendtheatres.org.uk.  \nAPPLY TO: Complete the HQ Application Form available at https://hqtheatres.com/careers/technician-southend-2021 and submit with a covering letter to michaell@southendtheatres.org.uk. Tell us why you think you are suited to this role, why it interests you and how we’ll benefit from having you on board!', 'id': '734740427307465_935367897244716'}, {'updated_time': '2021-07-02T11:31:52+0000', 'message': 'Thank you all! I’ve have a lot of emails to go through today and will be taking no more applications. Thanks everyone for your quick response!\nURGENT!!!\nPOSITION: Lighting technician with ETC Ion knowledge\nRATE OF PAY: £12 per hour\nDATE: 3rd July - (This Saturday) - 08:00 - 22:00 with 2 x 1 hour breaks\nLOCATION: Artsdepot, London, N12\nDESCRIPTION: We are looking for someone to cover a shift at Artsdepot (the technician we had booked is having to isolate!) \nThe day will consist of working with a dance company to put on 2 shows, 1 show at 12:45 (45 mins) and a different show at 19:30 (2 hours with an interval). You will be working with the choreographers to come up with some basic lighting, using our general rig, for each show, programming on ETC Ion and operating the shows.\nIf you are interested please email me - jen.watson@artsdepot.co.uk', 'id': '734740427307465_935367757244730'}, {'updated_time': '2021-07-02T11:16:26+0000', 'message': 'test1', 'id': '734740427307465_935360570578782'}], 'paging': {'previous': 'https://graph.facebook.com/v11.0/734740427307465/feed?access_token=EAALfCQXiKlgBAKKV6R8IpKEPXD45fvGGi4lXPMylXeQdGWIaqSaImStdgf9FyVoUB9XAAQCaXlkPH0zwFeItT1i4LJCa3Tol4LEukLJJZBruihNeTPJZAMRArerGVJgk5hSYPlZC6V4EOR77GUVIDKZCjcdZC4WmmRMg906qpHGzeKaye4PQh&__previous=1&since=1625225687&until&__paging_token=enc_AdAZCnjV3aymhiOZC3htQZAOoA81ytTCGfKHZAUx2X2Bek1OMWHACF91WZCtFWjMPBWMqzf2v3lSeHFdT0NGeDlPpFZBJUiOI470ZBIUtXX36WxnAULAqcLzE1E7RhnDOJLTgu9B8U7gG5EuujhZBACyhomTvcs9', 'next': 'https://graph.facebook.com/v11.0/734740427307465/feed?access_token=EAALfCQXiKlgBAKKV6R8IpKEPXD45fvGGi4lXPMylXeQdGWIaqSaImStdgf9FyVoUB9XAAQCaXlkPH0zwFeItT1i4LJCa3Tol4LEukLJJZBruihNeTPJZAMRArerGVJgk5hSYPlZC6V4EOR77GUVIDKZCjcdZC4WmmRMg906qpHGzeKaye4PQh&until=1625224586&since&__paging_token=enc_AdBXkxmSdgvlAyZBeRFFjDoCXv6Pe93XCTJr29GZAwxEIlmbVLQTdgunYlxCn3B9m3OeXEiUQZClB7SBxbOSTHa9V6sYj3QVcnqbuUjFT2IqHOWl9c62ZBZAUSIdt1kL5zfqMbv0ZARgII3iNp2ZAyAAlTa2kEl&__previous'}}

        print(events.values())

        feed = events['data']
        print(feed[0].values())

        for post in feed:
            body = post['message'].lower()
            id = post['id']

            print(body.replace("\n","    "))
            lines = body.split("\n")
            variables ={"position":{"result":None,"terms": ["position:","position", "role","title","technician","lx","lighting","sound","stage manager","SM","ASM","DSM","AV"]},
                        "fee":{"result":None,"terms": ["rate of pay:","rate of pay" , "fee","salary", "pay"]},
                        "dates":{"result":None,"terms": ["dates:", "date","times", "hours","permanent", "call"]},
                        "location":{"result":None,"terms": ["location:","location" ,"address"]},
                        "desc":{"result":None,"terms": ["description"]},
                        "contact":{"result":None,"terms": ["apply to:","apply to",".co.uk",".com",".org","www."]}
                        }

            skip = False
            vars_found = 0
            for c, line in enumerate(lines):
                # print(line)
                if skip:
                    skip = False
                    continue
                for keyword, keyvalue in variables.items():

                    if keyvalue["result"] != None:
                        # skips this keyword since we've already found it.
                        continue

                    terms = keyvalue["terms"]
                    # print(term)
                    for term in terms:
                        l = len(term)
                        # print(keyword["term"],line[:l])
                        if term in line:
                            vars_found += 1
                            # print(f"Matched {term}")
                            if len(line) > l and line[:l] == term:
                                # If length of line is more than length of string we are searching for
                                variables[keyword]["result"] = line[l+1:]
                                break
                            elif len(line) > l:
                                variables[keyword]["result"] = line
                                break
                            else:
                                # if not, then 99% chance that result is in the next line.
                                # Skip the next line.
                                variables[keyword]["result"] = lines[c+1]
                                skip = True
                                break



            print("Came up with:")
            print(variables)
            print("\n")

            if vars_found > 3 and variables["contact"]["result"] != None:
                link = "https://www.facebook.com/" + id
                new_jobs.append(Job(venue=variables['location'], job_title=variables['position'], link=link, deadline=variables['dates'], fee=variables['fee'], source="https://www.facebook.com/groups/backstagetheatrejobs/", other_info=variables['contact']))


            print("------------------------------------------------")
            print("\n")

        pass


    # Choose which to run.
    Curtain_Call()
    # The_Stage()
    # Arts_Jobs()
    # Facebook()

    # Ensure we quit at the end, no matter what happens previously.
    driver.quit()


    return new_jobs



def store_data(data):
    import pandas
    df1 = pandas.DataFrame([x.__dict__ for x in data])

    pandas.set_option('display.max_columns', 500)

    # print(df1)
    try:
        df1.to_csv("JobsData.csv", index=False)
    except:
        print("Error recording all these jobs")
        time.sleep(30)
        df1.to_csv("JobsData.csv", index=False)

    import mysql.connector

    sqlUsername = get_login_details()["sqlUsername"]
    sqlPassword = get_login_details()["sqlPassword"]

    mydb = mysql.connector.connect(
        host="localhost",
        user=sqlUsername,
        password=sqlPassword,
        database="TheatreJobs"
    )


    mycursor = mydb.cursor()

    import datetime
    date = datetime.date.today().strftime(("%d_%M_%Y"))

    tableName = f"{date}_JOBS"

    df1.to_sql(tableName, con=mydb,if_exists='replace',index=False)

    mycursor.execute(f'SELECT * FROM {tableName}')

    for row in mycursor.fetchall():
        print(row)

    mydb.close()

    # Test commit 3


store_data(Web_Scraping())
# Filtering
# Upload to Google docs
