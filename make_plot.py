import pandas as pd
import matplotlib.pyplot as plt


def plot_articles_by_year(path_to_csv): # this works for gv-articles-by-year.csv
    df = pd.read_csv(path_to_csv)

    # Extract the rows with year values between 1999 and 2019
    start_year = 1999
    end_year = 2019
    data = df[(df['years'] >= start_year) & (df['years'] <= end_year)].sort_values(by='years')

    year = data['years']
    n_gv = data['n gv headlines']
    total = data['percent gv']

    fig, ax = plt.subplots()
    #ax.plot(year, n_gv, label='gun violence headlines')
    ax.plot(year, total, label='total headlines')
    ax.set_xlabel('year')
    ax.set_ylabel('percent headlines')
    ax.set_title('Percent gun violence headlines')
    #ax.legend()


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


def plot_headline_types(path_to_file):
    data = path_to_file.readlines()
    

    for d in data:
        line = d.strip().split(",")
        year = line[0]
        school_type = line[1]


def box_plot(data, title, out_file):
    fig = plt.figure(figsize =(10, 7))
    plt.boxplot(data)
    plt.title(title)
    fig.savefig(out_file, dpi=300)


def multiple_box_plot(data_dict, title, outfile, colors = ['#0000FF', '#00FF00','#FFFF00', '#FF00FF']):
    # data_dict is dictionary of data to title
    data = data_dict.values()
    labels = data_dict.keys()
    colors = colors[:len(data)]
    
    fig = plt.figure(figsize =(10,7))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data, patch_artist = True,
                notch ='True', vert = 0)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='#8B008B',
                    linewidth = 1.5,
                    linestyle =":")
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='#8B008B',
                linewidth = 2)
    
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='red',
                linewidth = 3)
        
    for flier in bp['fliers']:
        flier.set(marker ='D',
                color ='#e7298a',
                alpha = 0.5)
    ax.set_yticklabels(labels)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.title(title)
    fig.savefig(outfile)


    

    
    
    
    
    





