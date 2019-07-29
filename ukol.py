import os
import requests
import xml.etree.ElementTree as ET

class Job:
    jmeno = ''
    url = ''
    def __init__(self, jmeno, url): 
        self.jmeno = jmeno
        self.url = url 

def getXML(url, soubor):
    try:
        r = requests.get(url)
        with open(soubor,'wb') as f:
            f.write(r.content)
        f.close()
    except:
        raise Exception('Chyba při stahování souboru '+ soubor)

def findJobs(soubor):
    try:
        strom = ET.parse(soubor)
        koren = strom.getroot()
        pole = []
        i = 0        
        for job in koren.findall('job'):
            if job.attrib["_class"] != 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject':
            # Filtr multibranch jobů. Každý build má vlastní log.
                jmeno = job.find('.//name').text
                url = job.find('.//url').text
                jobZaznam = Job(jmeno, url)
                pole.append(jobZaznam)
                print(url + 'lastBuild/api/xml')
                getXML(url + 'lastBuild/api/xml', 'xml/' + jmeno + '.xml')
                print(pole[i].jmeno, pole[i].url)
                print(i)
                i=i+1
    except:
        raise Exception('Chyba parsování souboru '+ soubor)

if os.path.isdir('./xml') == False:
    os.mkdir('xml')
url_jenkins = 'https://jenkins.mono-project.com/api/xml'
soubor_jenkins = 'xml/jenkins.xml'
getXML(url_jenkins,soubor_jenkins)
findJobs(soubor_jenkins)



