import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('gv-articles-by-year.csv')

# Extract the rows with year values between 1999 and 2019
start_year = 1999
end_year = 2019
data = df[(df['years'] >= start_year) & (df['years'] <= end_year)].sort_values(by='years')

year = data['years']
n_gv = data['n gv headlines']
total = data['total']

fig, ax = plt.subplots()
ax.plot(year, n_gv, label='gun violence headlines')
#ax.plot(year, total, label='total headlines')
ax.set_xlabel('Year')
ax.set_ylabel('n headlines')
ax.set_title('Gun Violence headlines')
ax.legend()


ax.set_ylim(ymin=0)
ax.set_xlim(xmin=1999,xmax=2019)
ax.set_xticks(range(1999, 2020,2))
#ax.set_yticks(range(0, int(max(total))+1))

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:}".format(int(x))))

# Add major and minor tick lines
ax.yaxis.grid(which='major', linestyle='-', linewidth='0.5', color='grey', alpha=0.8)
ax.yaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='grey', alpha=0.4)
ax.xaxis.grid(which='major', linestyle='-', linewidth='0.5', color='grey', alpha=0.8)
ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='grey', alpha=0.4)

# Adjust the layout to add white space
fig.tight_layout(pad=2)

# Save the plot
fig.savefig('gun-violence-headlines-by-year.png', dpi=300)


