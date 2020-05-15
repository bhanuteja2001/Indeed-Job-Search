from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString1 = request.form['content-1'].replace(" ","+")
            searchString2 = request.form['content-2']

            url = "https://www.indeed.co.in/jobs?q=" + searchString1 + '&l=' + searchString2
            print(url)
            uClient = uReq(url)
            Page = uClient.read()
            uClient.close()
            Page_html = bs(Page, "html.parser")
            bigboxes = Page_html.findAll("div", {"class": "jobsearch-SerpJobCard"})
            del bigboxes[0:3]
            #Bbox = bigboxes[0]
            #print(bigboxes)
            #commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            filename = searchString1 + ".csv"
            fw = open(filename, "w")
            headers = "Location, Company_name, Role, Salary, Summary, Link \n"
            fw.write(headers)
            reviews = []
            for box in bigboxes:
                try:
                    Company_name = box.div.find_all('span', {'class': 'company'})[0].text

                except:
                    Company_name = 'No Name'

                try:

                    Role = box.find_all('a',{'class':'jobtitle turnstileLink'})[0].text


                except:
                    Role = 'No Role'

                try:
                    Salary = box.find_all('span', {'class': 'salaryText'})[0].text

                except:
                    Salary = 'No Salary Heading'

                try:

                    Summary = box.find_all('div', {'class': 'summary'})[0].text

                except:
                    Summary = 'No Summary Heading'

                try:
                    Location = box.div.find_all('span', {'class': 'location accessible-contrast-color-location'})[0].text

                except:
                    Location = 'No Location'

                try:
                    Link = 'https://www.indeed.co.in' + box.a['href']

                except:
                    Link = 'No URL'

                mydict = {"Location": Location, "Company_name": Company_name, "Role": Role, "Summary": Summary,
                          "Salary": Salary,'Link':Link}
                print(mydict)
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
	#app.run(debug=True)