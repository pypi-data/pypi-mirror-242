import requests, re, pytz
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def Render_World(world):
    result = {
        "World":None,
        "Create":{
            "DateTime":None,
            "Date":None,
            "Time":None,
            "Timezone":None
        },
        "Modify":{
            "DateTime":None,
            "Date":None,
            "Time":None,
            "Timezone":None
        },
        "Epoch":{
            "Create":None,
            "Modify":None
        }
    }

    def epoch_time(matches):
        date_time = datetime.fromisoformat(matches[0])
        utc_date_time = date_time.astimezone(pytz.utc)
        return int((utc_date_time - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
    def worldtime(time,type):
        dt = datetime.fromisoformat(time)
        result[type]["DateTime"] = time
        result[type]["Date"] = str(dt.date())
        result[type]["Time"] = str(dt.time())
        result[type]["Timezone"] = str(dt.tzinfo)
    Website = requests.get(f"https://s3.amazonaws.com/world.growtopiagame.com/{world.lower()}.png", stream=True)  
    if Website.status_code == 200:
        try:       
            isi = str(Website.content).split('x00%tEXt')
            pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})"
            create = re.findall(pattern, isi[1])
            modify = re.findall(pattern, isi[2])
            if create:
                worldtime(create[0], "Create")
                result["Epoch"]["Create"] = epoch_time(create)
            if modify:
                worldtime(modify[0], "Modify")
                result["Epoch"]["Modify"] = epoch_time(modify)
            result["World"] = world.upper()
            return result
        except:
            return({"Error":"We managed to reach the web but we dont know exactly whats the problem","Error Code": "2"})
    elif Website.status_code == 403:
        return({"Error":f"Access Denied or the world is not exist","Error Code": Website.status_code})
    else:
        return({"Error":f"It looks like we can't reach the web! Error code {Website.status_code}","Error Code": Website.status_code})

def GameData():
    Result = {
        "Online_User": "",
        "WOTDLink" : "",
        "WOTDName" : "",
        "GTTime" : "",
        "GTDate" : ""
    }
    Website = requests.get(f"https://www.growtopiagame.com/detail")
    if Website.status_code == 200:
        try:
            Website = Website.json()
            Result["Online_User"] = Website["online_user"]
            Result["WOTDLink"] = Website["world_day_images"]["full_size"] 
            Result["WOTDName"] = ((Result["WOTDLink"].replace('https://www.growtopiagame.com/worlds/','')).replace('.png','')).upper()
            Result["GTTime"] = datetime.now(timezone('UTC')).astimezone(timezone('America/New_York')).strftime("%X")
            Result["GTDate"] = datetime.now(timezone('UTC')).astimezone(timezone('America/New_York')).strftime("%x")
            return(Result)
        except:
            return({"Error":"We managed to reach growtopiagame.com but we dont know exactly whats the problem","Error Code": "2"})
    else:
        return({"Error":f"It looks like we can't reach growtopiagame.com! Error code {Website.status_code}","Error Code": Website.status_code})

def ItemData(NameItem, Region = "en", **kwargs):
    def body(HTMLResult,NameItem):
        def checking(Result):
            check = 0
            for fix in Result.keys():
                theresult = Result[fix]
                if check == 3:
                    Result[fix] = theresult.split(" - ")
                if check == 8:
                    Result[fix] = theresult.split(" ")
                if check == 7:
                    restore = []
                    for number in theresult.split(" "):
                        input = ""
                        for number2 in number:
                            if number2.isdigit():
                                input = input+number2
                        if input != "":
                            restore.append(input)
                    Result[fix] = {
                            "Fist":restore[0],
                            "Pickaxe":restore[1],
                            "Restore":restore[2]
                    }
                if check == 9:
                    time = []
                    growtime = {}
                    for number in theresult.split(" "):
                        input = ""
                        for number2 in number:
                            if number2.isdigit():
                                input = input+number2
                        if input != "":
                            time.append(input)
                    format = ["Month","Week","Day","Hour","Minute","Second"]
                    i = 0
                    while i != len(time):
                        growtime[format[((len(format))-1)-i]] = time[((len(time))-1)-i]
                        i+=1
                    Result[fix] = growtime

                if check == 10:
                    gems = []
                    if len(theresult.split(" - ")) == 1:
                        gems.append(theresult.split(" - ")[0])
                        gems.append(theresult.split(" - ")[0])
                    else:
                        gems.append(theresult.split(" - ")[0])
                        gems.append(theresult.split(" - ")[1])                        
                    Result[fix] = {
                            "Max":gems[1],
                            "Min":gems[0]
                        }                                
                check +=1
        wordcheck = None
        Result = {}
        if len(HTMLResult.select(".gtw-card")) == 1:
            result2 = {}
            Properties = HTMLResult.find_all('div',  class_= "card-text")
            Data = HTMLResult.select(".card-field")
            Rarity = BeautifulSoup((str((HTMLResult.find('small'))).replace("(Rarity: ", "")).replace(")", ""), "html.parser").text
            PropertiesResult = []
            for add in Properties:
                hum = BeautifulSoup(str(add).replace("<br/>", "--split--"), "html.parser")
                PropertiesResult.append(hum.text)
            result2.update({"Description": PropertiesResult[0].strip()})
            result2.update({"Properties": (PropertiesResult[1].strip()).split("--split--")})
            try:
                result2.update({"Rarity": int(Rarity)})
            except:
                result2.update({"Rarity": "None"})
            DataResult = []
            for typ in Data:
                mus = BeautifulSoup((str(typ).replace("</tr>", ",")).replace("</th>", ","), "html.parser")
                DataResult = (((mus.text).split(",")))
            res = 0 
            while res <= (len(DataResult)-3):
                result2.update({DataResult[res].strip(): DataResult[res+1].strip()})
                res = res+2
            checking(result2)
            try:
                ItemTitle = ((((HTMLResult.find('span', class_= "mw-headline")).small).decompose()).get_text(strip=True)).replace(u'\xa0', u' ')
            except:    
                ItemTitle = (HTMLResult.find('span', class_= "mw-headline").get_text(strip=True)).replace(u'\xa0', u' ')
            result2["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{ItemTitle}".replace(' ','_')
            Result[ItemTitle] = result2
            wordcheck = True
        elif len(HTMLResult.select(".gtw-card")) > 1:
            for HTMLResultTabber in HTMLResult.select(".gtw-card"):   
                Result2 = {}   
                PropertiesResult = []
                Properties = HTMLResultTabber.find_all('div',  class_= "card-text")
                Data = HTMLResultTabber.select(".card-field")
                Rarity = BeautifulSoup((str((HTMLResultTabber.find('small'))).replace("(Rarity: ","")).replace(")", ""), "html.parser").text
                for add in Properties:
                    hum = BeautifulSoup(str(add).replace("<br/>", "--split--"), "html.parser")
                    PropertiesResult.append(hum.text)
                Result2.update({"Description": PropertiesResult[0].strip()})
                Result2.update({"Properties": (PropertiesResult[1].strip()).split("--split--")})
                try:
                    Result2.update({"Rarity": int(Rarity)})
                except:
                    Result2.update({"Rarity": "None"})
                DataResult = []
                for typ in Data:
                    mus = BeautifulSoup((str(typ).replace("</tr>", ",")).replace("</th>", ","), "html.parser")
                    DataResult = (mus.get_text(" ",strip=True)).split(",")
                res = 0 
                while res <= (len(DataResult)-3):
                    Result2.update({DataResult[res].strip(): DataResult[res+1].strip()})
                    res = res+2  
                checking(Result2)
                try:
                    ItemTitle = ((((HTMLResultTabber.find('span', class_= "mw-headline")).small).decompose()).get_text(strip=True)).replace(u'\xa0', u' ')
                except:    
                    ItemTitle = (HTMLResultTabber.find('span', class_= "mw-headline").get_text(strip=True)).replace(u'\xa0', u' ')
                Result[ItemTitle] = Result2
                Result[ItemTitle]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{ItemTitle}".replace(' ','_')
                wordcheck = False
        if wordcheck == False:
            NameItem = NameItem.lower()
            word = []
            Result2 = {}
            for item in Result.keys():
                if NameItem in item.lower():
                    word.append(item)
            for item2 in word:
                Result2[item2] = Result[item2]
            if len(Result2) == 1:
                for item3 in Result2.keys():
                    return Result2[item3]
            else:
                return Result2
        elif wordcheck == True:
            return Result
        else:
            return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
    #====================================================================Main Program=============================================================================
    try:
        ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+NameItem).text, "html.parser")
        if ItemPage.select(".gtw-card") == []:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/"+Region+"/api/v1/SearchSuggestions/List?query="+NameItem).json()
            try:
                ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+ItemFinder["items"][0]["title"]).text, "html.parser")
            except:
                return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
        FinalResult = body(ItemPage,NameItem)
        if kwargs.get("ResultOnly") == True and len(FinalResult.keys()) == 1:
            return FinalResult[NameItem]
        return FinalResult
    except:
        return({"Error": "It looks like we can't reach fandom.com "+Region+"! Try again later","Error Code": "1"})

def ItemRecipe(NameItem, Region = "en", **kwargs):
    def body(HTMLResult,NameItem):
        def Insert(this,Recipe):
            if this in Recipe.keys():
                Recipe[this].append([])
                for meh in item.select('td'):
                    meh = ((meh.get_text(' ',strip=True)).replace('"',"'"))
                    Recipe[this][1].append(meh.replace(u'\xa0', u''))                 
            else:
                Recipe[this] = [[]]
                for meh in item.select('td'):
                    meh = ((meh.get_text(' ',strip=True)).replace('"',"'"))
                    Recipe[this][0].append(meh.replace(u'\xa0', u'')) 

        def Insert2(this,Recipe):
            if this in Recipe[meh].keys():
                Recipe[meh][this].append([])
                for the in mes.select('td'):
                    the = ((the.get_text(' ',strip=True)).replace('"',"'"))
                    Recipe[meh][this][1].append(the.replace(u'\xa0', u''))                    
            else:
                Recipe[meh][this] = [[]]
                for the in mes.select('td'):
                    the = ((the.get_text(' ',strip=True)).replace('"',"'"))
                    Recipe[meh][this][0].append(the.replace(u'\xa0', u'')) 

        def Title(itemish):
            try:
                ItemTitle = ((((itemish.find('span', class_= "mw-headline")).small).decompose()).get_text(strip=True)).replace(u'\xa0', u' ')
            except:    
                ItemTitle = (itemish.find('span', class_= "mw-headline").get_text(strip=True)).replace(u'\xa0', u' ')
            return ItemTitle
        fortabber = HTMLResult.select_one(".tabber.wds-tabber")
        require = []
        Result = {}
        wordcheck = None
        if len(HTMLResult.select(".gtw-card")) == 1:
            ws = 0
            count = 0
            Recipe = {}
            for item in HTMLResult.select(".content"):
                if item.select(".content") == []:
                    if not count in require:
                        Insert(((item.find('th')).text).strip(), Recipe)
                    ws += 1
                else:
                    meh = ((item.find('th')).text).strip()
                    Recipe[meh] = {}
                    for mes in item.select(".content"):
                        Insert2(((mes.find('th')).text).strip(), Recipe)
                        ws += 1
                        require.append(ws)
                count +=1
            Result[Title(HTMLResult)] = Recipe
            Result[Title(HTMLResult)]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{Title(HTMLResult)}".replace(' ','_')
            wordcheck = True
        else:
            for itemish in fortabber.select(".wds-tab__content"):
                ws = 0
                count = 0
                Recipe = {}
                if itemish.select(".content") == []:
                    for item in itemish.select(".content"):
                        if item.select(".content") == []:
                            if not count in require: 
                                Insert(((item.find('th')).text).strip(), Recipe)
                            ws += 1
                        else:
                            meh = ((item.find('th')).text).strip()
                            Recipe[meh] = {}
                            for mes in item.select(".content"):
                                Insert2(((mes.find('th')).text).strip(), Recipe)
                                ws += 1
                                require.append(ws)
                        count +=1
                    Result[Title(itemish)] = Recipe
                    Result[Title(itemish)]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{Title(itemish)}".replace(' ','_')
                else:
                    for item in itemish.select(".content"):
                        if item.select(".content") == []:
                            if not count in require: 
                                Insert(((item.find('th')).text).strip(), Recipe) 
                            ws += 1
                        else:
                            meh = ((item.find('th')).text).strip()
                            Recipe[meh] = {}
                            for mes in item.select(".content"):
                                Insert2(((mes.find('th')).text).strip(), Recipe) 
                                ws += 1
                                require.append(ws)
                        count +=1
                    Result[Title(itemish)] = Recipe
                    Result[Title(itemish)]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{Title(itemish)}".replace(' ','_')
            wordcheck = False
        if wordcheck == False:
            NameItem = NameItem.lower()
            word = []
            Result2 = {}
            for item in Result.keys():
                if NameItem in item.lower():
                    word.append(item)
            for item2 in word:
                Result2[item2] = Result[item2]
            if len(Result2) == 1:
                for item3 in Result2.keys():
                    return Result2[item3]
            else:
                return Result2
        elif wordcheck == True:
            return Result
        else:
            return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
    #====================================================================Main Program=============================================================================
    try:
        ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+NameItem).text, "html.parser")
        if ItemPage.select(".gtw-card") == []:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/"+Region+"/api/v1/SearchSuggestions/List?query="+NameItem).json()
            try:
                ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+ItemFinder["items"][0]["title"]).text, "html.parser")
            except:
                return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
        FinalResult = body(ItemPage,NameItem)
        if kwargs.get("ResultOnly") == True and len(FinalResult.keys()) == 1:
            return FinalResult[NameItem]
        return FinalResult
    except:
        return({"Error": "It looks like we can't reach fandom.com "+Region+"! Try again later","Error Code": "1"})

def ItemSprite(NameItem, Region = "en", **kwargs):
    def body(HTMLResult,NameItem,Region):
        wordcheck = None
        Result = {}  
        if len(HTMLResult.select(".gtw-card")) == 1:
            Data = {
                "Item" :"",
                "Tree" :"",
                "Seed" :""
            }  
            images = HTMLResult.find('div', {"class": "gtw-card"})
            Data["Item"]= (images.find('div', {"class": "card-header"})).img['src']
            Data["Tree"] = (((((((images.find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).img['src']
            Data["Seed"] = (images.find('td', {"class": "seedColor"})).img['src']
            try:
                ItemTitle = ((((HTMLResult.find('span', class_= "mw-headline")).small).decompose()).get_text(strip=True)).replace(u'\xa0', u' ')
            except:    
                ItemTitle = (HTMLResult.find('span', class_= "mw-headline").get_text(strip=True)).replace(u'\xa0', u' ')
            Result[ItemTitle] = Data
            Result[ItemTitle]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{ItemTitle}".replace(' ','_')
            wordcheck = True
        else:
            for HTMLResultTabber in HTMLResult.select(".wds-tab__content"):
                Data = {
                    "Item" :"",
                    "Tree" :"",
                    "Seed" :""
                }  
                images = HTMLResultTabber.find('div', {"class": "gtw-card"})
                Data["Item"]= (images.find('div', {"class": "card-header"})).img['src']
                Data["Tree"] = (((((((images.find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).find_next('td')).img['src']
                Data["Seed"] = (images.find('td', {"class": "seedColor"})).img['src']
                try:
                    ItemTitle = ((((HTMLResultTabber.find('span', class_= "mw-headline")).small).decompose()).get_text(strip=True)).replace(u'\xa0', u' ')
                except:    
                    ItemTitle = (HTMLResultTabber.find('span', class_= "mw-headline").get_text(strip=True)).replace(u'\xa0', u' ')
                Result[ItemTitle] = Data
                Result[ItemTitle]["Link"] = f"https://growtopia.fandom.com/{Region}/wiki/{ItemTitle}".replace(' ','_')
            wordcheck = False
        if wordcheck == False:
            NameItem = NameItem.lower()
            word = []
            Result2 = {}
            for item in Result.keys():
                if NameItem in item.lower():
                    word.append(item)
            for item2 in word:
                Result2[item2] = Result[item2]
            if len(Result2) == 1:
                for item3 in Result2.keys():
                    return Result2[item3]
            else:
                return Result2
        elif wordcheck == True:
            return Result
        else:
            return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
    #====================================================================Main Program=============================================================================
    try:
        ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+NameItem).text, "html.parser")
        if ItemPage.select(".gtw-card") == []:
            ItemFinder = requests.get(f"https://growtopia.fandom.com/"+Region+"/api/v1/SearchSuggestions/List?query="+NameItem).json()
            try:
                ItemPage = BeautifulSoup(requests.get("https://growtopia.fandom.com/"+Region+"/"+"wiki/"+ItemFinder["items"][0]["title"]).text, "html.parser")
            except:
                return {"Error": "Sorry! I can't find "+NameItem+" in Growtopia Fandom "+Region,"Error Code": "2"}
        FinalResult = body(ItemPage,NameItem,Region)
        if kwargs.get("ResultOnly") == True and len(FinalResult.keys()) == 1:
            return FinalResult[NameItem]
        return FinalResult
    except:
        return({"Error": "It looks like we can't reach fandom.com "+Region+"! Try again later","Error Code": "1"})  