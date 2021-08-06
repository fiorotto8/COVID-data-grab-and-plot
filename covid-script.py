#git clone https://github.com/CSSEGISandData/COVID-19.git
#Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered
#USUALLY THE FILE OF A CERTAIN DAY IS UPLOADED IN THE MORNING OF THE DAY AFTER (TIME ZONE+DELAY?)
import ROOT
import tqdm
import pandas as pd
import os
import datetime
import subprocess
import sys
import fnmatch
import numpy as np
import math as m
import git

def d_to_s(date):
    return str(date.strftime("%m-%d"))


#Update initialized repository
repo = git.Repo('./COVID-19')
# List remotes
print('Remotes:')
for remote in repo.remotes:
    print(f'- {remote.name} {remote.url}')
# Pull from remote repo
print(repo.remotes.origin.pull())


#In order to calculate the death probability the death number has to be STRICTLY higher that this value (and the confirmed cases have to be different to zero!)
DeathCut=20
#In order to perform the plot and the fit the confirmed case has to be STRICTLY higher that this value
ConfirmedCut=100

countries=["China","Italy","Iran","UK","France","Germany","US","Canada","Spain","Russia","Brazil","Korea, South","Taiwan","Singapore","Thailand","Switzerland","Serbia","Norway","Sweden","Netherlands","Denmark","Japan","Belgium","Austria","Qatar","Malaysia","Greece","Finland","Baharain","Israel","Czechia","Slovenia","Portugal","Iceland","Ireland","Romania","Estonia","India","Poland","Egypt","Kuwait","Iraq","Lebanon","San Marino","Indonesia","Turkey","Ecuador","Saudi Arabia","Peru","South Africa","Mexico","Slovakia","Colombia","Bulgaria","Argentina","Uruguay","Hungary","Ukraine","Albania","Malta","Senegal","Kenya","Congo","Namibia","Madagascar"]
main=ROOT.TFile("./COVID-19/COVID_data.root","RECREATE")#root file creation
#global
#########
Tconf=[]
Tdeath=[]
Treco=[]
Tabsolute=[]
#########
totC=[]
totD=[]
totR=[]
#########
DC=[]
DD=[]
DR=[]
#########
ass=[]
########
prob=[]
########
path="./COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
#col_list=["Province/State","Country/Region", "Last Update", "Confirmed", "Deaths", "Recovered"]
"""
days=["01-22","01-23","01-24","01-25","01-26","01-27","01-28","01-29","01-30","01-31","02-01","02-02","02-03","02-04","02-05","02-06","02-07","02-08","02-09","02-10","02-11","02-12","02-13","02-14","02-15","02-16","02-17","02-18","02-19","02-20","02-21","02-22","02-23","02-24","02-25","02-26","02-27","02-28","02-29","03-01","03-02","03-03","03-04","03-05","03-06","03-07","03-08","03-09","03-10","03-11","03-12","03-13","03-14","03-15","03-16","03-17","03-18","03-19","03-20","03-21","03-22","03-23","03-24","03-25","03-26","03-27","03-28","03-29","03-30","03-31","04-01","04-02","04-03","04-04","04-05","04-06","04-07","04-08","04-09","04-10","04-11","04-12","04-13","04-14","04-15","04-16","04-17","04-18","04-19","04-20","04-21","04-22","04-23","04-24","04-25","04-26","04-27","04-28","04-29","04-30","05-01","05-02","05-03","05-04","05-05","05-06","05-07","05-08","05-09","05-10","05-11","05-12","05-13","05-14","05-15","05-16","05-17","05-18","05-19","05-20","05-21","05-22","05-23","05-24","05-25","05-26","05-27","05-28","05-29","05-30","05-31","06-01","06-02","06-03","06-04","06-05","06-06","06-07","06-08","06-09","06-10","06-11","06-12","06-13","06-14","06-15","06-16","06-17","06-18","06-19","06-20","06-21","06-22","06-23","06-24","06-25","06-26","06-27","06-28","06-29","06-30","07-01","07-02","07-03","07-04","07-05","07-06","07-07","07-08","07-09","07-10","07-11","07-12","07-13","07-14","07-15","07-16","07-17","07-18","07-19","07-20","07-21","07-22","07-23","07-24","07-25","07-26","07-27","07-28","07-29","07-30","07-31","08-01","08-02","08-03","08-04","08-05","08-06","08-07","08-08","08-09","08-10","08-11","08-12","08-13","08-14","08-15","08-16","08-17","08-18","08-19","08-20","08-21","08-22","08-23","08-24","08-25","08-26","08-27","08-28","08-29","08-30","08-31","09-01","09-02","09-03","09-04","09-05","09-06","09-07","09-08","09-09","09-10","09-11","09-12","09-13","09-14","09-15","09-16","09-17","09-18","09-19","09-20","09-21","09-22","09-23","09-24","09-25","09-26","09-27","09-28","09-29","09-30","10-01","10-02","10-03","10-04","10-05","10-06","10-07","10-08","10-09","10-10","10-11","10-12","10-13","10-14","10-15","10-16","10-17","10-18","10-19","10-20","10-21","10-22","10-23","10-24","10-25","10-26","10-27","10-28","10-29","10-30","10-31","11-01","11-02","11-03","11-04","11-05","11-06","11-07","11-08","11-09","11-10","11-11","11-12","11-13","11-14","11-15","11-16","11-17","11-18","11-19","11-20","11-21","11-22","11-23","11-24","11-25","11-26","11-27","11-28","11-29","11-30","12-01","12-02","12-03","12-04","12-05","12-06","12-07","12-08","12-09","12-10","12-11","12-12","12-13","12-14","12-15","12-16","12-17","12-18","12-19","12-20","12-21","12-22","12-23","12-24","12-25","12-26","12-27","12-28","12-29","12-30","12-31","01-01","01-02","01-03","01-04","01-05","01-06","01-07","01-08","01-09","01-10","01-11","01-12","01-13","01-14","01-15","01-16","01-17","01-18","01-19","01-20","01-21","01-22","01-23","01-24","01-25","01-26","01-27","01-28","01-29","01-30","01-31","02-01","02-02","02-03","02-04","02-05","02-06","02-07","02-08","02-09","02-10","02-11","02-12","02-13","02-14","02-15","02-16","02-17","02-18","02-19","02-20","02-21","02-22","02-23","02-24","02-25","02-26","02-27","02-28","03-01","03-02","03-03","03-04","03-05","03-06","03-07","03-08","03-09","03-10","03-11","03-12","03-13","03-14","03-15","03-16","03-17","03-18","03-19","03-20","03-21","03-22","03-23","03-24","03-25","03-26","03-27","03-28","03-29","03-30","03-31","04-01","04-02","04-03","04-04","04-05","04-06","04-07","04-08","04-09","04-10","04-11","04-12","04-13","04-14","04-15","04-16","04-17","04-18","04-19","04-20","04-21","04-22","04-23","04-24","04-25","04-26","04-27","04-28","04-29","04-30","05-01","05-02","05-03","05-04","05-05","05-06","05-07","05-08","05-09","05-10","05-11","05-12","05-13","05-14","05-15","05-16","05-17","05-18","05-19","05-20","05-21","05-22","05-23","05-24","05-25","05-26","05-27","05-28","05-29","05-30","05-31","06-01","06-02","06-03","06-04","06-06","06-06","06-07","06-08","06-09","06-10","06-11","06-12","06-13","06-14","06-15","06-16","06-17","06-18","06-19","06-20","06-21","06-22","06-23","06-24","06-25","06-26","06-27","06-28","06-29","06-30","07-01","07-02","07-03","07-04","07-05","07-06","07-07","07-08","07-09","07-10","07-11","07-12","07-13","07-14","07-15","07-16","07-17","07-18","07-19","07-20","07-21","07-22","07-23","07-24","07-25","07-26","07-27","07-28","07-29","07-30","07-31","08-01","08-02","08-03","08-04"]
"""
#Start and stop dates
start_string="2020-01-22"
end_string=str((datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

#convert the start and stop string to the start and stop datetime
start = datetime.datetime.strptime(start_string, '%Y-%m-%d')
end = datetime.datetime.strptime(end_string, '%Y-%m-%d')

diff=end - start
files_num=diff.days+1
print("There are",files_num, "files")

#create the datetimes of all the files involved
days = [ d_to_s(start + datetime.timedelta(days=x))  for x in range(files_num)]

"""
for x in range(len(days)):
    print(x, days[x])
"""

print("Countries considered: " +str(len(countries)))
print("Days passed from 22/01: "+str(len(days)-1))
#print("Number of files in the dataset: "+str(len(days)))
print("China complete lockdown started 02-13-2020, day #22")
print("Italy complete lockdown started 03-10-2020, day #48")
print("2021 starts at day #345")

for q in tqdm.tqdm(range (0,len(countries))):
    main.cd()
    #####################################
    country=countries[q]
    icut=0#cut over the first days#######
    fcut=0#cut over the final days#######
    #####################################
    main.mkdir(country.replace(" ",""))
    main.cd(country.replace(" ",""))



    #global lists
    df=[]
    #Important variables
    daysPas=list(range(0,len(days)))
    #########
    confirmed=[]
    deaths=[]
    recovered=[]
    #########
    DeltaC=[]
    DeltaD=[]
    DeltaR=[]
    #########
    assolute=[]
    #########
    #Exponential fit function
    Exponential=ROOT.TF1("Exponential","exp((x-[0])/[1])",np.array(icut+1,dtype="d"),np.array(len(days)-fcut,dtype="d"))
    Exponential.SetParNames("Shift","Mean Time")
    Exponential.SetParameters(30,5)
    #Logistic fit function
    Logistic=ROOT.TF1("Logistic","[0]/(1+exp(-(x-[1])/[2]))",np.array(icut+1,dtype="d"),np.array(len(days)-fcut,dtype="d"))
    Logistic.SetParNames("Plateau","Midpoint","Rise time")
    Logistic.SetParameters(80000,20,10)

    ##################################################################################################################################################################
    #gathering data
    for a in range(0,len(days)):#this for runs over the data files
            #quei cretini hanno cambiato il formato delle colonne ad un certo punto
            #print(a)
            if a<=59:
                col_list=["Province/State","Country/Region", "Last Update", "Confirmed", "Deaths", "Recovered"]
                country_col="Country/Region"
            if a>59:
                col_list=["FIPS","Admin2","Province_State","Country_Region","Last_Update","Lat","Long_","Confirmed","Deaths","Recovered","Active","Combined_Key"]
                country_col="Country_Region"

            if a<345:
                df.append( pd.read_csv(str(path)+"/"+str(days[a])+"-2020.csv", usecols=col_list) )
            if a>=345:
                df.append( pd.read_csv(str(path)+"/"+str(days[a])+"-2021.csv", usecols=col_list) )
            #Replace the NAN with 0
            df[a] = df[a].replace(np.nan, 0)
            #print(df[a])#this contain all the data!
            totC.append(sum(df[a]["Confirmed"]))
            #print(str(a)+"    "+str(totC[a]))
            totD.append(sum(df[a]["Deaths"]))
            totR.append(sum(df[a]["Recovered"]))
            Ctemp=0#have to be resetted for every file
            Dtemp=0#they sum the occorrencies over all the provicnes
            Rtemp=0
            for b in range(0,len(df[a][country_col])):#this for runs over the single file
                if df[a][country_col][b]==country:
                    #print(df[a]["Province/State"][b])
                    #print(a)
                    #print(country+" è presente il giorno: "+days[a]+" linea "+str(b)+" su "+str(len(df[a][country_col]))+" linee totali")
                    Ctemp=Ctemp+df[a]["Confirmed"][b]
                    Dtemp=Dtemp+df[a]["Deaths"][b]
                    Rtemp=Rtemp+df[a]["Recovered"][b]

    ##################################################################################################################################################################
    #CORRECTION IN CHINA DATASETS
                if country=="China":#this take into account the fact that "Mainland China" became just "China" after some files
                    if df[a][country_col][b]=="Mainland China":
                        Ctemp=Ctemp+df[a]["Confirmed"][b]
                        Dtemp=Dtemp+df[a]["Deaths"][b]
                        Rtemp=Rtemp+df[a]["Recovered"][b]
    #CORRECTION IN UK DATASETS
                if country=="UK":#this take into account the fact that "Mainland China" became just "China" after some files
                    if df[a][country_col][b]=="United Kingdom":
                        Ctemp=Ctemp+df[a]["Confirmed"][b]
                        Dtemp=Dtemp+df[a]["Deaths"][b]
                        Rtemp=Rtemp+df[a]["Recovered"][b]
    #CORRECTION IN South Korea DATASETS
                if country=="Korea, South":#this take into account the fact that "Mainland China" became just "China" after some files
                    if df[a][country_col][b]=="South Korea":
                        Ctemp=Ctemp+df[a]["Confirmed"][b]
                        Dtemp=Dtemp+df[a]["Deaths"][b]
                        Rtemp=Rtemp+df[a]["Recovered"][b]
    #CORRECTION IN Taiwan DATASETS
                if country=="Taiwan":#this take into account the fact that "Mainland China" became just "China" after some files
                    if df[a][country_col][b]=="Taiwan*":
                        Ctemp=Ctemp+df[a]["Confirmed"][b]
                        Dtemp=Dtemp+df[a]["Deaths"][b]
                        Rtemp=Rtemp+df[a]["Recovered"][b]
    ##################################################################################################################################################################
            confirmed.append(Ctemp)
            deaths.append(Dtemp)
            recovered.append(Rtemp)
            #print(str(a)+"   "+str(confirmed[a]))
            #print(days[a])
    ##################################################################################################################################################################

    ##################################################################################################################################################################
    #CORRECTION IN IRAN DATASETS
    if country=="Iran":#this take into account the fact that in day 48 the Iran data are zero: average is made
        confirmed[48]=(confirmed[47]+confirmed[49])/2
        deaths[48]=(deaths[47]+deaths[49])/2
        recovered[48]=(recovered[47]+recovered[49])/2
    #CORRECTION IN IRAN DATASETS
    if country=="Russia":#this take into account the fact that in day 48 the Russia data are zero: average is made
        confirmed[48]=(confirmed[47]+confirmed[49])/2
        deaths[48]=(deaths[47]+deaths[49])/2
        recovered[48]=(recovered[47]+recovered[49])/2
    #CORRECTION IN South kKOREA DATASETS
    if country=="Korea, South":#this take into account the fact that in day 48 the South Korea data are zero: average is made
        confirmed[48]=(confirmed[47]+confirmed[49])/2
        deaths[48]=(deaths[47]+deaths[49])/2
        recovered[48]=(recovered[47]+recovered[49])/2
    #CORRECTION IN TAIWAN DATASETS
    if country=="Taiwan":#this take into account the fact that in day 48 the South Korea data are zero: average is made
        confirmed[48]=(confirmed[47]+confirmed[49])/2
        deaths[48]=(deaths[47]+deaths[49])/2
        recovered[48]=(recovered[47]+recovered[49])/2
    ##################################################################################################################################################################


    #insert zero when the country is not found
    ####################################################
    for q in range(0,len(daysPas)-len(confirmed)):
        confirmed.insert(0,0)
        deaths.insert(0,0)
        recovered.insert(0,0)
    ####################################################

    #apply cut in time
    ############################
    if icut>0:
        confirmed=confirmed[icut:]
        deaths=deaths[icut:]
        recovered=recovered[icut:]
        daysPas=daysPas[icut:]
    if fcut>0:
        confirmed=confirmed[:-fcut]
        deaths=deaths[:-fcut]
        recovered=recovered[:-fcut]
        daysPas=daysPas[:-fcut]
    #############################

    #####################################
    #Calculating Single day variations
    DeltaC.append(0)
    DeltaD.append(0)
    DeltaR.append(0)
    for k in range(0,len(daysPas)-1):
        DeltaC.append(confirmed[k+1]-confirmed[k])
        DeltaD.append(deaths[k+1]-deaths[k])
        DeltaR.append(recovered[k+1]-recovered[k])
    #######################################

#####################################################
    #Calculating CONFIRMED-DEATH-RECOVERED
    for k in range(0,len(daysPas)):
        assolute.append(confirmed[k]-deaths[k]-recovered[k])
        #print(str(assolute[k])+"   "+str(confirmed[k])+"   "+str(deaths[k])+"   "+str(recovered[k]))
#####################################################


    #Death probability country & globally
    if confirmed[len(days)-1]!=0 and deaths[len(days)-1]>DeathCut:
        countryProb=deaths[len(days)-1]/confirmed[len(days)-1]
        prob.append(countryProb)


    #convert list in arrays
    x=np.array(daysPas,dtype="d")
    n=len(daysPas)
    nn=len(days)
    xx=x


    #############################
    #PLOTS and FITS in the root file
    #########################################################################################################################################################
    if confirmed[len(days)-1]>ConfirmedCut:
        #RAW DATA
        #Confirmed cases in Country
        conf = ROOT.TGraphErrors(n,x,np.array(confirmed,dtype="d"))
        conf.SetMarkerColor(4)#blue
        conf.SetMarkerStyle(22)#triangle
        conf.SetMarkerSize(1)
        conf.SetTitle(country+" Confirmed Cases")
        conf.GetXaxis().SetTitle("Days from the 22/01/2020")
        conf.SetName("Confirmed Cases")
        conf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #conf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Tconf.append(Exponential.GetParameter(1))
        #print(Exponential.GetParameter(1))
        conf.Write()

        #Death cases in country
        death = ROOT.TGraphErrors(n,x,np.array(deaths,dtype="d"))
        death.SetMarkerColor(4)#blue
        death.SetMarkerStyle(22)
        death.SetMarkerSize(1)
        death.SetTitle(country+" Death Cases")
        death.GetXaxis().SetTitle("Days from the 22/01/2020")
        death.SetName("Death Cases")
        death.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #death.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Tdeath.append(Exponential.GetParameter(1))
        death.Write()

        #Recovered cases in counrty
        reco = ROOT.TGraphErrors(n,x,np.array(recovered,dtype="d"))
        reco.SetMarkerColor(4)#blue
        reco.SetMarkerStyle(22)#triangle
        reco.SetMarkerSize(1)
        reco.SetTitle(country+" Recovered Cases")
        reco.GetXaxis().SetTitle("Days from the 22/01/2020")
        reco.SetName("Recovered Cases")
        reco.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #reco.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Treco.append(Exponential.GetParameter(1))
        reco.Write()
        #########################################################################################################################################################


        #########################################################################################################################################################
        #CONFIRMED-DEATH-RECOVERED
        conf = ROOT.TGraphErrors(n,x,np.array(assolute,dtype="d"))
        conf.SetMarkerColor(4)#blue
        conf.SetMarkerStyle(22)#triangle
        conf.SetMarkerSize(1)
        conf.SetTitle(country+" Absolute Confirmed Cases")
        conf.GetXaxis().SetTitle("Days from the 22/01/2020")
        conf.SetName("Absolute Confirmed Cases")
        conf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #conf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Tabsolute.append(Exponential.GetParameter(1))
        #print(Exponential.GetParameter(1))
        conf.Write()
        #########################################################################################################################################################


    #####################################################################################################
        #Death probability per Country
        if confirmed[len(days)-1]!=0 and deaths[len(days)-1]>DeathCut:
            countryProbHist=ROOT.TH1D(country+" Death Probability",country+" Death Probability",100,0,0.1)
            countryProbHist.Fill(countryProb)
            countryProbHist.Write()
    #####################################################################################################


        #########################################################################################################################################################
        #VARIATIONS
        #Confirmed cases in Country
        Sconf = ROOT.TGraphErrors(n,x,np.array(DeltaC,dtype="d"))
        Sconf.SetMarkerColor(4)#blue
        Sconf.SetMarkerStyle(22)#triangle
        Sconf.SetMarkerSize(1)
        Sconf.SetTitle(country+" Variation in Confirmed Cases")
        Sconf.GetXaxis().SetTitle("Days from the 22/01/2020")
        Sconf.SetName("Single day Variation Confirmed")
        Sconf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #Sconf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Sconf.Write()

        #Death cases in country
        Sdeath = ROOT.TGraphErrors(n,x,np.array(DeltaD,dtype="d"))
        Sdeath.SetMarkerColor(4)#blue
        Sdeath.SetMarkerStyle(22)
        Sdeath.SetMarkerSize(1)
        Sdeath.SetTitle(country+" Variation in Death Cases")
        Sdeath.GetXaxis().SetTitle("Days from the 22/01/2020")
        Sdeath.SetName("Single day Variation Death")
        Sdeath.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #Sdeath.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Sdeath.Write()

        #Recovered cases in counrty
        Sreco = ROOT.TGraphErrors(n,x,np.array(DeltaR,dtype="d"))
        Sreco.SetMarkerColor(4)#blue
        Sreco.SetMarkerStyle(22)#triangle
        Sreco.SetMarkerSize(1)
        Sreco.SetTitle(country+" Variation in Recovered Cases")
        Sreco.GetXaxis().SetTitle("Days from the 22/01/2020")
        Sreco.SetName("Single day Variation Recovered")
        Sreco.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        #Sreco.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
        Sreco.Write()
        #########################################################################################################################################################


                                        ################# EXIT THE FOR CYCLE #################


main.cd()

print("Last day inserted: "+str(days[len(days)-1])+"-2020")
print("Countries which passed the Confirmed Probability cut: "+str(len(Tconf)))
print("Countries which passed the Death Probability cut: "+str(len(prob)))


#############################################################################################################################################################
#####################################
#Calculating Global Single day variations
DC.append(0)
DD.append(0)
DR.append(0)
for k in range(0,len(daysPas)):
    DC.append(totC[k+1]-totC[k])
    DD.append(totD[k+1]-totD[k])
    DR.append(totR[k+1]-totR[k])
#####################################

#############################################################################################################################################################
    #Calculating CONFIRMED-DEATH-CONFIRMED
for k in range(0,len(daysPas)):
    ass.append(totC[k]-totD[k]-totR[k])
    #print(k)
    #print(str(assolute[k])+"   "+str(confirmed[k])+"   "+str(deaths[k])+"   "+str(recovered[k]))
#############################################################################################################################################################


#############################################################################################################################################################
#RAW DATA
#Confirmed cases GLOBALLY
conf = ROOT.TGraphErrors(nn,xx,np.array(totC,dtype="d"))
conf.SetMarkerColor(4)#blue
conf.SetMarkerStyle(22)#triangle
conf.SetMarkerSize(1)
conf.SetTitle("Global Confirmed Cases")
conf.GetXaxis().SetTitle("Days from the 22/01/2020")
conf.SetName("Confirmed Cases")
conf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#conf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
conf.Write()

#Death cases GLOBALLY
death = ROOT.TGraphErrors(nn,xx,np.array(totD,dtype="d"))
death.SetMarkerColor(4)#blue
death.SetMarkerStyle(22)
death.SetMarkerSize(1)
death.SetTitle("Global Death Cases")
death.GetXaxis().SetTitle("Days from the 22/01/2020")
death.SetName("Death Cases")
death.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#death.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
death.Write()

#Recovered cases GLOBALLY
reco = ROOT.TGraphErrors(nn,xx,np.array(totR,dtype="d"))
reco.SetMarkerColor(4)#blue
reco.SetMarkerStyle(22)#triangle
reco.SetMarkerSize(1)
reco.SetTitle("Global Recovered Cases")
reco.GetXaxis().SetTitle("Days from the 22/01/2020")
reco.SetName("Recovered Cases")
reco.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#reco.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
reco.Write()
#############################################################################################################################################################


#############################################################################################################################################################
#CONFIRMED-DEATH-RECOVERED#############################################################
#Confirmed cases GLOBALLY
conf = ROOT.TGraphErrors(n,xx,np.array(ass,dtype="d"))
conf.SetMarkerColor(4)#blue
conf.SetMarkerStyle(22)#triangle
conf.SetMarkerSize(1)
conf.SetTitle(country+" Absolute Confirmed Cases")
conf.GetXaxis().SetTitle("Days from the 22/01/2020")
conf.SetName("Absolute Confirmed Cases")
conf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#conf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
Tconf.append(Exponential.GetParameter(1))
#print(Exponential.GetParameter(1))
conf.Write()
#############################################################################################################################################################


#############################################################################################################################################################
#VARIATIONS
#Confirmed cases GLOBALLY
Sconf = ROOT.TGraphErrors(nn,xx,np.array(DC,dtype="d"))
Sconf.SetMarkerColor(4)#blue
Sconf.SetMarkerStyle(22)#triangle
Sconf.SetMarkerSize(1)
Sconf.SetTitle("Variations Global Confirmed Cases")
Sconf.GetXaxis().SetTitle("Days from the 22/01/2020")
Sconf.SetName("Variations Confirmed Cases")
Sconf.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#Sconf.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
Sconf.Write()

#Death cases GLOBALLY
Sdeath = ROOT.TGraphErrors(nn,xx,np.array(DD,dtype="d"))
Sdeath.SetMarkerColor(4)#blue
Sdeath.SetMarkerStyle(22)
Sdeath.SetMarkerSize(1)
Sdeath.SetTitle("Variations Global Death Cases")
Sdeath.GetXaxis().SetTitle("Days from the 22/01/2020")
Sdeath.SetName("Variations Death Cases")
Sdeath.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#Sdeath.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
Sdeath.Write()

#Recovered cases GLOBALLY
Sreco = ROOT.TGraphErrors(nn,xx,np.array(DR,dtype="d"))
Sreco.SetMarkerColor(4)#blue
Sreco.SetMarkerStyle(22)#triangle
Sreco.SetMarkerSize(1)
Sreco.SetTitle("Variations Global Recovered Cases")
Sreco.GetXaxis().SetTitle("Days from the 22/01/2020")
Sreco.SetName("Variations Recovered Cases")
Sreco.Fit("Exponential","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
#Sreco.Fit("Logistic","RQ","",np.array(icut+1,dtype="d"),np.array(n-fcut,dtype="d"))
Sreco.Write()
#############################################################################################################################################################


#############################################################################################################################################################
#Daths probabilities histogram
DeathProb=ROOT.TH1D("Death Probabilities","Death Probabilities",10,0,0.1)
for h in range(0,len(prob)):
    DeathProb.Fill(prob[h])
DeathProb.Write()
#############################################################################################################################################################


#############################################################################################################################################################
#MEAN TIMES HISTOGRAMS
TC=ROOT.TH1D("Confirmed Mean Times Histogram","Confirmed Mean Times Histogram",10,1,9)
for h in range(0,len(Tconf)):
    TC.Fill(Tconf[h])
TC.Write()

TD=ROOT.TH1D("Death Mean Times Histogram","Death Mean Times Histogram",10,1,9)
for h in range(0,len(Tdeath)):
    TD.Fill(Tdeath[h])
TD.Write()

TR=ROOT.TH1D("Recovered Mean Times Histogram","Recovered Mean Times Histogram",10,1,9)
for h in range(0,len(Treco)):
    TR.Fill(Treco[h])
TR.Write()

TABS=ROOT.TH1D("Absolute Confirmed Mean Times Histogram","Absolute Confirmed Mean Times Histogram",10,1,9)
for h in range(0,len(Tabsolute)):
    TABS.Fill(Tabsolute[h])
TABS.Write()
#############################################################################################################################################################


main.Close()
#ROOT.gApplication.Run()#this is needed to keep the canvas on screen, it maintains the code running after the end
#####################################################################################################
