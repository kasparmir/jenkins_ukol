import os
import requests
import xml.etree.ElementTree as ET
import math
import sys

class Job:
    jmeno = ''
    url = ''
    stav = ''
    minuty = ''
    autori = []
    def __init__(self, jmeno, url, result, minuty, autori): 
        self.jmeno = jmeno
        self.url = url 
        self.result = result
        self.minuty = minuty
        self.autori = autori

def getXML(url, soubor):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(soubor,'wb') as f:
                f.write(r.content)
                f.close()
        else:
            print(url + ' není možné stáhnout.')
    except:
        raise Exception('Chyba při stahování souboru '+ soubor)
    return r.status_code

def findJobs(soubor):
    try:
        strom = ET.parse(soubor)
        koren = strom.getroot()
        pole = []
        i = 0        
        for job in koren.findall('job'):
            if job.attrib["_class"] != 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject':

                jmeno = job.find('.//name').text
                url = job.find('.//url').text
                stahni = getXML(url + 'lastBuild/api/xml', 'xml/' + jmeno + '.xml')
                if stahni == 200:
                    jobZaznam = Job(jmeno, url, '', '', None)
                    pole.append(jobZaznam)
                    print(url + 'lastBuild/api/xml')
        return pole
    except:
        raise Exception('Chyba parsování souboru '+ soubor)
    return pole

def parseJob(job, i):
    try:
        print ('xml/' + job.jmeno + '.xml')
        strom = ET.parse('xml/' + job.jmeno + '.xml')
        koren = strom.getroot()
        try:
             job.result = koren.find('.//result').text
        except:
             print ('Chybí výsledek sestavení...')
        try:
             minuty = koren.find('.//action/executingTimeMillis').text
             minuty = math.ceil(float(float(minuty)/float(1000*60))%60)
             job.minuty = minuty
        except:
             print ('Chybí informace o době běhu...')
        changeSet = koren.find('changeSet')
        autori = []
        if changeSet is not None:
            for polozka in changeSet.findall('item'):
                try:
                    autor = polozka.find('.//authorEmail').text
                    if autor not in autori:
                        autori.append(autor)
                except:
                    print('Chybí email autora...')
        job.autori = autori
    except:
        raise Exception('Chyba při parsování souboru '+ job.jmeno + '.xml')
    return job


try:
    tempDir = sys.argv[1]
except:
    tempDir = '/tmp/jenkins_parser'
if os.path.isdir(tempDir) == False:
    os.mkdir(tempDir)
if os.path.isdir('./xml') == False:
    os.mkdir('xml')
url_jenkins = 'https://jenkins.mono-project.com/api/xml'
soubor_jenkins = 'xml/jenkins.xml'
getXML(url_jenkins,soubor_jenkins)
joby = findJobs(soubor_jenkins)
i = 0
for job in joby:
    job_novy = parseJob(job, i)
    joby[i] = job_novy
    i = i+1
for job in joby:
    if job.result == 'FAILURE':
        try:
            with open(tempDir + '/' + job.jmeno + '.txt','w') as f:
                f.write('Název: ' + job.jmeno + "\n")
                f.write('Běžel minut: ' + str(job.minuty) + "\n")
                f.write('Změny provedli: ' + "\n")
# U některých jobů není uvedeno
                for item in job.autori:
                    f.write("%s\n" % item)
                f.close()
        except:
            raise Exception('Chyba při zápisu do souboru '+ jmeno + '.txt')
