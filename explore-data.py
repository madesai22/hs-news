import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 


year_counts = {} # key: year (int) --> value: ['n gv headlines','n other','total'] (list)
n_gv_headlines_idx = 0
n_other_idx = 1
total_idx = 2

#df = pd.DataFrame(columns = ['year', 'n gv headlines','n other','total','percent gv'])
new_headlines = 0
with open('/data/madesai/articles_clean.jsonlist') as f, open('./gv-headlines.csv','w') as f2:
    
    for line in f:
            

            data = json.loads(line)
            headline = data['headline']
            content = data['content']
            if data['date']:
            # try:
            #     year = datetime.strptime(data['date'], "%B %d, %Y").year
            # except:
                year_pattern = r"(19[1-9][0-9]|20[0-9][0-9])"

                year_string  = re.findall(year_pattern, data['date'])
                if year_string:
                    year  = int(year_string[0])
                else:
                    year = 3000
            else:
                year = 3000
            
            bullet_and_march = re.findall(r"\bMarch for Our Lives\b|\bbullet\b|\bStudents Demand Action\b|\bNational School Walkout\b|\bsecond amendment\b|\bNRA\b|\bNever Again MSD\b",headline, re.IGNORECASE)
            

            gun_match = re.findall(r"\b(gun)\b", headline, re.IGNORECASE)
            sports_pattern = r"ball|lacrosse|score|point|film|movie|hoop|win|soccer|hockey|polo|champ|game|varsity|lax|trophy|sweep|flu|vaccin|photo|star|playoff|competition|finals"
            sports_match = re.findall(sports_pattern, headline, re.IGNORECASE)
            shooting_match = re.findall(r"\b(?!(?:shot[\s-]?put(?:t)?(?:ter)?\b))(?:shoot|shot)\w*\b", headline, re.IGNORECASE)
            long_shot_match = re.findall(r"(\blong\s+shot\b)|(call\s+the\s+shot\b)", headline, re.IGNORECASE)
            shooter_likely = re.findall(r"\b(?:active|mass|school)\s+(?:shoot|shot)\w*\b", headline, re.IGNORECASE)


            #pattern = re.compile(r"\b(gun)\b", re.IGNORECASE)
            #pattern2 = r"^(?!.*ball|lacrosse|hoop|varsity|win|soccer|point|).*shoot.*$" 
            #pattern3 = r"^(?!.*ball|lacrosse|hoop|varsity|win|soccer|point).*shot.*$"     
            headline_gv = False
            content_gv = False

            if gun_match or shooter_likely or (shooting_match and not sports_match and not long_shot_match):

                #print(headline)

                f2.write(headline.replace(",", "")+','+str(year)+'\n')
                #df.loc[df['year'] == year, 'n gv headlines'] += 1
                if year in year_counts:
                    year_counts[year][n_gv_headlines_idx] += 1
                    year_counts[year][total_idx] += 1
                else:
                    year_counts[year]= [1,0,1] 
            
            else:
                if bullet_and_march:
                    print(headline)
                    new_headlines +=1

                if year in year_counts:
                    year_counts[year][n_other_idx] += 1
                    year_counts[year][total_idx] += 1

                else:
                    year_counts[year] = [0,1,1]
            
f2.close()
df = pd.DataFrame.from_dict(year_counts, orient='index', columns=[ 'n gv headlines','n other','total'])
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'years'})


print(new_headlines)
percent_list = []
for index, row in df.iterrows():
    percent_list.append(row['n gv headlines']/row['total']*100)
df['percent gv'] = percent_list

    #row['percent gv'] = percent

df.sort_values(by=['years'])
df.to_csv('gv-articles-by-year.csv')



#print(year_counts)
#print("missing year for "+str(no_date_gv)+" articles with gun violence.")
#print("missing year for "+str(no_date_other)+" other articles.")
    
# percentage plot
#years = list(year_counts.keys())
#pcent = [sublist[3] for sublist in year_counts.values()]
#plt.bar(years, pcent)
plt.bar(df['years'],df['percent gv'])
plt.xlabel("Year")
plt.ylabel("Percent gun violence stories")
plt.savefig('percent-gv.png')
plt.close()

# total articles
#total_articles = [sublist[2] for sublist in year_counts.values()] 
#print(len(years),len(total_articles))
#gv_articles = [sublist[0] for sublist in year_counts.values()]
#plt.plot(years, total_articles, label = 'total articles')
#plt.plot(years, gv_articles, label = 'gun violence articles')
plt.plot(df['years'],df['total'], label = 'total articles')
plt.plot(df['years'],df['n gv headlines'],label = 'gun violence articles')
plt.legend()
plt.xlabel("Year")
plt.ylabel("Number of articles")
plt.savefig('n-gv.png')
plt.close()

