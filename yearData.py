# coding: utf8

import pandas as pd
import numpy as np
from datetime import date, timedelta
import os
from random import randint
import colorsys
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation

todrop = ['TD', 'YD', 'Daily', '%± YD', '%± LW', 'Theaters', 'Avg','Days', 'New This Day', 'Estimated']

class dataera :

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.directory = '/home/daata/Documents/Data Science/dataera/Popular Movies/' + str(start_date.year)


    def daterange(self):
        for n in range(int ((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)

    def get(self, day):
        df = pd.read_html('https://www.boxofficemojo.com/date/' + day.strftime('%Y-%m-%d')+ '/', na_values=["-"], header = 0)[0]
        df.drop(columns = todrop, axis = 1, inplace = True )
        df.dropna(axis = 0, inplace=True)
        df['time'] = np.repeat(day.strftime("%Y-%m-%d") ,len(df))
        df.columns = ['name','value','group','time']
        df['value'] = df.value.apply(lambda x: x.replace('$',''))
        df['value'] = df.value.apply(lambda x: x.replace(',',''))
        df['value'] = df['value'].astype(int)
        return df

    def period(self):
        day = self.start_date
        data = self.get(day)
        i = 0
        while day != self.end_date + timedelta(1):
            i += 1
            df = self.get(day)
            data = data.append(df, ignore_index=True)
            day += timedelta(1)
        self.count = i
        clors = []
        for nm in range(len(data['group'].unique().tolist())):
                clors.append('#' + '%06X' % randint(0, 0xFFFFFF))
        self.groups = data.set_index('name')['group'].to_dict()
        self.ncolors = dict(zip(data['group'].unique(), clors))
        return data

    def draw_barchart(self,day):
        dff = self.get(day).sort_values(by='value', ascending=True).tail(10)
        ax.clear()
        ax.barh(dff['name'], dff['value'], color=[self.ncolors[x] for x in dff['group']], alpha = 0.75, tick_label='$')
        dx = dff['value'].max() / 200
        for i, (value, name) in enumerate(zip(dff['value'], dff['name'])):
            ax.text(value-dx, i,     name,      color = '#DFDFDF'  ,   size=14, weight=600, ha='right', va='bottom')
            ax.text(value-dx, i-.25, self.groups[name], size=10, color='#DFDFDF', ha='right', va='baseline')
            ax.text(value+dx, i,     f'{value:,.0f}' ,  size=14, ha='left',  va='center')
        ax.text(1, 0.1, str(day), transform=ax.transAxes, color='#DFDFDF', size=35, ha='right', weight=800)
        ax.text(0, 1.06, 'Total Gross in $', transform=ax.transAxes, color='#DFDFDF',size=12)
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#B5B5B5', labelsize=12)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
        ax.set_axisbelow(True)
        ax.text(0, 1.15, 'Highest grossing movies of ' + str(year),
                transform=ax.transAxes, color = '#DFDFDF', size=24, weight=600, ha='left', va='top')
        ax.text(1, 0, 'by @dataera; credits @pratapvardhan @jburnmurdoch', transform=ax.transAxes, color='#DFDFDF', ha='right',
                bbox=dict(facecolor='#3A3A3A', alpha=0.4, edgecolor='white'))
        plt.box(False)

    def createFolder(self):
        try:
	           if not os.path.exists(self.directory):
		                 os.makedirs(self.directory)
        except OSError:
            print('Error: Creating directory. ' +  self.directory)

    def description(self):
        f= open(self.directory +'/'+ str(self.start_date.year)+'.txt',"w+")
        df = self.period()
        x = df['value'].max()
        y = df.index[df['value'] == x]
        y = y[0]
        f.write('In this dataset, we handled ' + str(len(df)) + ' movie observations between ' + str(self.start_date) + ' and ' + str(self.end_date) + '\n' + 'What film had the biggest box office gross in ' + str(self.start_date.year) + '?' + '\n' + str(df['name'][y]) + ' distributed by ' + str(df['group'][y]) + ' had made $' + f'{x:,}' + '\n' + 'Here is the list of movie names you will see in this video' + '\n' +str(df['name'].unique().tolist()) )

year = 1997
while year != 1996 :
    p = dataera(date(year, 1, 1), date(year,12,31))
    p.createFolder()
    p.description()
    fig, ax = plt.subplots(figsize=(15, 8))
    animator = animation.FuncAnimation(fig, p.draw_barchart, frames = dataera(p.start_date - timedelta(1) , p.end_date + timedelta(4)).daterange(), save_count = p.count + 4)
    animator.save(p.directory + '/' + str(p.start_date)+ 'to' + str(p.end_date)+'.mp4', fps = 1, bitrate = 1800, savefig_kwargs={'facecolor':'#3A3A3A'})
    year -= 1
