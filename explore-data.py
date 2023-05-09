import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 

i = 0
year_counts = {} # key: year (int) --> value: ['n gv headlines','n other','total'] (list)
n_gv_headlines_idx = 0
n_other_idx = 1
total_idx = 2

#df = pd.DataFrame(columns = ['year', 'n gv headlines','n other','total','percent gv'])

with open('/data/madesai/articles_clean.jsonlist') as f, open('./gv-headlines.txt','w') as f2:
    
    for line in f:
        if i <1000:
            i+= 1

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
            pattern = re.compile(r"\b(gun)\b", re.IGNORECASE)
            pattern2 = r"\<shoot(?!.*\b(?:ball|lacrosse|hoop)\b)"
            pattern3 = r"\<shot(?!.*\b(?:ball|lacrosse|hoop)\b)"    
            headline_gv = False
            content_gv = False

            # if year in df['year'].values:
            #     df.loc[df['year'] == year, 'total'] += 1
            # else:
            #     new_row = {'year':year, 'n gv headlines':0,'n other':0,'total':1,'percent gv':0}
            #     df = pd.concat([df, pd.DataFrame([new_row])])
            #     print(year)
            if re.findall(pattern, headline) or re.findall(pattern2, headline) or re.findall(pattern3, headline):
                headline_gv = True
                # i += 1 
                f2.write(headline.replace(",", "")+','+str(year)+'\n')
                #df.loc[df['year'] == year, 'n gv headlines'] += 1
                if year in year_counts:
                    year_counts[year][n_gv_headlines_idx] += 1
                    year_counts[year][total_idx] += 1
                else:
                    year_counts[year]= [1,0,1] 
            else:
                #df.loc[df['year'] == year, 'n other'] += 1
                if year in year_counts:
                    year_counts[year][n_other_idx] += 1
                    year_counts[year][total_idx] += 1

                else:
                    year_counts[year] = [0,1,1]
f2.close()
df = pd.DataFrame.from_dict(year_counts, orient='index', columns=[ 'n gv headlines','n other','total'])
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'year'})


# add item to year_couts[year] with total articles and percent gv 
# key: year (int) --> value: [n gv headlines, n other, total articles, percent gv]
# no_date = year_counts.pop(3000,[0,0])
# no_date_gv = no_date[0]
# no_date_other = no_date[1]

for index, row in df.iterrows():
    percent = row['n gv headlines']/row['total']*100
    row['percent gv'] = percent

df.sort_values(by=['year'])
df.to_csv('gv-articles-by-year.csv')

#for y, counts in year_counts.items():
#    total = counts[0] + counts[1]
#    percent_gv = counts[0]/total * 100
#    year_counts[y].append(total)
#    year_counts[y].append(percent_gv)


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

