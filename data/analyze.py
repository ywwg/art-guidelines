import json
import pylab
import scipy

def process_json():
    json_data = open("art-grant-data.json").read()
    data = json.loads(json_data)
    return data["root"]

def requested_histogram(input_array):
    processed_array = [entry["requested"] for entry in data if entry["requested"]]
    n, bins, patches = pylab.hist(processed_array, range(0,1800,100))
    #(mu, sigma) = scipy.stats.norm.fit(processed_array)
    pylab.xlim(0,1800)
    pylab.xlabel("Funding Requested")
    pylab.ylabel("Frequency")
    pylab.title("Firefly Creativity Grant \n Requested Grants 2010 - 2014")
    pylab.grid(True)
    pylab.show()


def awarded_histogram(input_array):
    processed_array = [entry["awarded"] for entry in data if entry["awarded"]]
    pylab.hist(processed_array, range(0,1800,100))
    pylab.xlim(0,1800)
    pylab.xlabel("Funding Awarded")
    pylab.ylabel("Frequency")
    pylab.title("Firefly Creativity Grant \n Awarded Grants 2010 - 2014")
    pylab.grid(True)
    pylab.show()
        
data = process_json()
awarded_histogram(data)
