import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import seaborn as sns

def plot_bcf(output_path,parser):
    '''Function to plot the requested sections from the bcf-stats file.'''

    if parser.sn or parser.ALL: # Check if this section has been requested by the user

        path=os.path.join(output_path,r'SN\SN.txt') # Path to the file that needs to be used to make the plot
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=9)) # Open file as a pandas dataframe
        
        '''Extract the columns to be plot'''
        values=df.value.iloc[[3,5]] 
        labels=df.key.iloc[[3,5]]
        values_sites=list(df.value.iloc[[1,7,8]])
        values_sites[0]=values_sites[0]-values_sites[1]-values_sites[2]
        values_sites[1]=values_sites[1]-values_sites[2]

        '''This creates a Pieplot showing the percentages of SNPs vs. Indels'''
        fig1,ax1= plt.subplots() # Create an empty figure and axes
        ax1.pie(values, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90)
        ax1.axis('equal') # Set the aspect ratio to be equal
        ax1.set_title('Distribution of variants') # Set Title
        fig1.savefig(os.path.join(output_path,'SN','Distribution_of_Variants_PiePlot.png'),format='png') # Save figure in the appropriate subfolder

        '''This creates a Pieplot showing the distribution of sites '''
        fig1,ax1= plt.subplots(figsize=(8,8))
        ax1.pie(values_sites,
        shadow=True, startangle=90,radius=5,explode=[0,0,0.7],labeldistance=None,autopct='%1.1f%%',normalize=True) #Plot a pieplot
        ax1.axis('equal')
        ax1.set_title('Distribution of Allelic Sites')
        plt.legend(['Non-multi-allelic sites','Non-SNP multi-allelic sites','SNP multi-allelic sites'],loc='best',fontsize='x-small')
        fig1.savefig(os.path.join(output_path,'SN','Distribution_of_Allelic_Sites_PiePlot.png'),format='png') # Save the figure in the appropriate subfolder 
        
    if parser.tstv or parser.ALL: # Check if this section has been requested by the user

        path=os.path.join(output_path,r'TSTV\TSTV.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plots the Ts/Tv ratio per File on the same plot'''
        plt.figure(figsize=(8,8)) #Create figure of a specific size
        sns.scatterplot(data=df,x='id',y="ts/tv") # Create a scatterplot using seaborn
        plt.xticks(df.id) # Set the x-axis tick values
        plt.yticks(df['ts/tv']) # Set the y-axis tick values
        plt.ylabel('Ts/Tv ratio',fontsize=12) # Set the title for the y-axis.
        plt.xlabel('File_IDs',fontsize=12) # Set the title for the x-axis
        plt.title('Ts/Tv ratio by file',fontsize=22) # Set the title
        plt.savefig(os.path.join(output_path,'TSTV','TSTV_ratio.png'),format='png')
        plt.close() #close the figure

        '''Plots a barplot demonstrating the mean of the count of Transitions v. Transversions over all the IDs in the file'''
        plt.figure(figsize=(8,8)) # Open new figure 
        plt.bar(height=[df.ts.mean()/10**6,df.tv.mean()/10**6,df['ts_(1st_ALT)'].mean()/10**6,df['tv_(1st_ALT)'].mean()/10**6],x=['Transitions','Transversions','Transitions- 1st ALT','Tranversions-1st ALT'])
        plt.ylabel('Counts scaled by 10^6',fontsize=15)
        plt.xticks(fontsize=8)
        plt.title('Distribution of Transition/Transversions',fontsize=18)
        plt.savefig(os.path.join(output_path,'TSTV','Transitions_&_Transversions.png'),format='png')
        plt.close() # Close the figure.
    
    if parser.sis or parser.ALL: # Check if the output is requested by the user

        path=os.path.join(output_path,r'SiS\SiS.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))
        df.number_of_SNPs=df.number_of_SNPs/10**5

        '''Plot the Singleton stats per File_ID in the file.'''
        plt.figure(figsize=(8,8)) 
        sns.scatterplot(data=df,x='id',y="number_of_SNPs") #Create a scatterplot using seaborn
        plt.xticks(df['id'])
        plt.ylabel('SNP counts scaled by 10^5',fontsize=12)
        plt.xlabel('File IDs',fontsize=12)
        plt.title('Singleton (SNPs) by ID',fontsize=18)
        plt.savefig(os.path.join(output_path,'SiS','Singleton_stats_by_sample.png'),format='png')
        plt.close()

        '''Plot the Singelton Transitions & Transversions percentages in the file.'''
        plt.figure(figsize=(8,8))
        plt.pie([df.number_of_transitions.mean(),df.number_of_transversions.mean()],autopct='%1.1f%%',normalize=True)
        plt.legend(['percentage of transitions',' percentage of tranversions'],loc='best',fontsize='x-small')
        plt.title('Fractions of transitions vs. tranversions in the number of SNPs',fontsize=10)
        plt.savefig(os.path.join(output_path,'SiS','Singleton_stats_Transitions_v._Transversions.png'),format='png')
        plt.close()

    if parser.af or parser.ALL:
        path=os.path.join(output_path,r'AF\AF.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        #Select the rows to be plotted. If there are more than 10 rows, select only 10 which are evenly spaced
        if len(df)>10:
            rows_to_select=list(range(0,len(df.allele_frequency),int(round((len(df.allele_frequency))/10))))
        else:
            rows_to_select=np.arange(0,len(df))


        labels=df.allele_frequency[rows_to_select]

        # Scale the counts 
        transitions=df.number_of_transitions[rows_to_select]/10**4
        transversions=df.number_of_transversions[rows_to_select]/10**4
        indels=df.number_of_indels[rows_to_select]/10**4

        x = np.arange(len(labels))  # the label locations
        width = 0.3 # the width of the bars

        '''Plot the distribution of SNPs and Indels per allelic frequency'''
        #Create a barplot with 3 bars for each x-axis value
        fig, ax = plt.subplots(figsize=(8,8))
        ax.bar(x - width, transitions, width, label='Count of transitions')
        ax.bar(x, transversions, width, label='Count of transversions')
        ax.bar(x + width, indels,width,label='Count of indels')
        ax.set_xticks(x,labels,fontsize=7)
        ax.legend(loc='best',fontsize='x-small')
        ax.set_title('Distribution of SNPs and Indels per allelic-frequency',fontsize=18)
        ax.set_xlabel('Allelic Frequency',fontsize=12)
        ax.set_ylabel('Count scaled by 10**4',fontsize=12)
        fig.savefig(os.path.join(output_path,'AF','Distribution_of_SNPs_and_Indels_per_allelic-frequency.png'),format='png')
        plt.close(fig)

    if parser.q or parser.ALL:

        path=os.path.join(output_path,r'QUAL\QUAL.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the distribution of number of SNPs & number of Indels v. the Quality metric'''
        ax = df.plot(x="Quality", y="number_of_SNPs", legend=False,ylabel='SNP count',kind='scatter',s=2,figsize=(8,8),alpha=0.4) #Create a scatterplot. Alpha sets the transparency of the points. 's' sets the size of the points.
        ax2 = ax.twinx() # Create a twin y-axis to plot two y-values on one plot
        df.plot(x="Quality", y="number_of_indels", legend=False, color="r",ax=ax2,ylabel='Indel Count',kind='scatter',s=2,alpha=0.4) # Plot the second pair of x-y values as a scatterplot.
        ax.figure.legend(['SNPs', 'Indels']) #Manually set the values in the Legend
        ax.set_title('SNPs and Indels v. Quality',fontsize=15)
        ax.figure.savefig(os.path.join(output_path,'QUAL','Quality_plot.png'))
        ax.figure.clear()

        '''Plot the distribution of the Number of SNPs vs. the Number of Indels '''
        plt.figure(figsize=(8,8))
        sns.scatterplot(data= df, x="number_of_SNPs",y='number_of_indels',size=3,legend=False)
        plt.xlabel('Number of Indels')
        plt.ylabel('Number of SNPs')
        plt.title('SNP count v. Indel Count',fontsize=15)
        plt.savefig(os.path.join(output_path,'QUAL','SNP_v_Indel_Count.png'),format='png')
        plt.close()


    if parser.idd or parser.ALL:

        path=os.path.join(output_path,r'IDD\IDD.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))
        df['count']=df['count']/10**3

        '''Plot the distribution of the length metric vs. the Indel Count.'''
        plt.figure(figsize=(10,10)) #Create a new figure with a specific size.
        sns.barplot(data=df,x='length_(deletions_negative)',y='count')
        if len(df)>10:
            plt.locator_params(axis='x', nbins=10) # Only have 10 evenly spaced tick labels on the x-axis if there are more than 10 x-axis values.
        plt.xlabel('Length') 
        plt.ylabel('Count Scaled by 10**3')
        plt.title('Indel Distribution',fontsize=15)
        plt.savefig(os.path.join(output_path,'IDD','Indel_distribution.png'),format='png')
        plt.close()

    if parser.st or parser.ALL:

        path=os.path.join(output_path,r'ST\ST.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the barplot showing the counts for each Substitution Type.'''
        sr=df['count'] #Create a series object from the created pandas dataframe.
        sr.index=df.type #Set the index for the series object
        sr=sr.sort_values() # Sort the series object in an ascending order
        plt.figure(figsize=(8,8))
        sns.barplot(x=sr.index,y=sr,palette=sns.color_palette('rocket',len(sr))) # Plot a barplot in seaborn using custom colour gradient
        plt.xlabel('Type',fontsize=12)
        plt.ylabel('Count',fontsize=12)
        plt.title('Substitution Type Distribution',fontsize=22)
        plt.savefig(os.path.join(output_path,'ST','Substitution_types.png'),format='png')
        plt.close()

    if parser.dp or parser.ALL:

        path=os.path.join(output_path,r'DP\DP.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the Fraction of Genotypes metric against the Bin metric'''
        plt.figure(figsize=(8,8))
        sns.lineplot(data=df,x='bin',y='fraction_of_genotypes_(%)',color='red') #plot a lineplot in seaborn
        plt.xticks(ticks=df.bin[::int(np.round(len(df.bin)/15))],rotation=45)
        plt.xlabel('Bin',fontsize=12)
        plt.ylabel('Fraction of Genotypes (%)',fontsize=12)
        plt.title('Depth Distribution',fontsize=22)
        plt.savefig(os.path.join(output_path,'DP','Depth_Distribution.png'),format='png')
        plt.close()

        '''Plot the Fraction of Sites metric against the Bin metric'''
        plt.figure(figsize=(8,8)) 
        sns.barplot(data=df,x='bin',y='fraction_of_sites_(%)')
        plt.locator_params(axis='x', nbins=10)
        plt.xlabel('Bin',fontsize=12)
        plt.ylabel('Fraction of Sites (%)',fontsize=12)
        plt.title('Depth Distribution',fontsize=22)
        plt.savefig(os.path.join(output_path,'DP','Distribution_of_Fraction_of_Sites.png'),format='png')
        plt.close()
    
    if parser.psc or parser.ALL:

        path=os.path.join(output_path,r'PSC\PSC.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the sample nHets counts.'''
        plt.figure(figsize=(8,8))
        sns.scatterplot(data=df,x='sample',y='nHets',hue='nHets',palette=sns.color_palette('magma',len(df)),legend=False,s=50)
        plt.xticks(df['sample'],fontsize=10)
        plt.ylabel('Hets count',fontsize=15)
        plt.xlabel('Sample IDs',fontsize=15)
        plt.yticks(fontsize=10)
        plt.title('Per Sample nHets count',fontsize=22)
        plt.savefig(os.path.join(output_path,'PSC','Per_Sample_nHets_Count.png'),format='png')
        plt.close()

        '''Plot the per sample Singleton counts.'''
        plt.figure(figsize=(8,8))
        sns.scatterplot(data=df,x='sample',y='nSingletons',hue='nSingletons',palette=sns.color_palette('magma',len(df)),legend=False,s=50)
        plt.xticks(df['sample'],fontsize=10)
        plt.ylabel('Singletons count',fontsize=15)
        plt.xlabel('Sample IDs',fontsize=15)
        plt.yticks(fontsize=10)
        plt.title('Per Sample Singletons count',fontsize=22)
        plt.savefig(os.path.join(output_path,'PSC','Per_Sample_Singletons_Count.png'),format='png')
        plt.close()

    if parser.psi or parser.ALL:

        path=os.path.join(output_path,r'PSI\PSI.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the per Sample Indel nHets count'''
        plt.figure(figsize=(8,8))
        sns.scatterplot(data=df,x='sample',y='nHets',hue='nHets',palette=sns.color_palette('magma',len(df)),legend=False,s=50)
        plt.xticks(df['sample'],fontsize=10)
        plt.ylabel('Indels Hets count',fontsize=15)
        plt.xlabel('Sample IDs',fontsize=15)
        plt.yticks(fontsize=10)
        plt.title('Per Sample Indels nHets count',fontsize=22)
        plt.savefig(os.path.join(output_path,'PSI','Per_Sample_InDel_Counts.png'),format='png')
        plt.close()
        
        '''Plot the per Sample Indel nAA count.'''
        plt.figure(figsize=(8,8))
        sns.scatterplot(data=df,x='sample',y='nAA',hue='nAA',palette=sns.color_palette('magma',len(df)),legend=False,s=50)
        plt.xticks(df['sample'],fontsize=10)
        plt.ylabel('Indels nAA count',fontsize=15)
        plt.xlabel('Sample IDs',fontsize=15)
        plt.yticks(fontsize=10)
        plt.title('Per Sample nAA count',fontsize=22)
        plt.savefig(os.path.join(output_path,'PSI','Per_Sample_nAA_Counts.png'),format='png')
        plt.close()
    
    if parser.hwe or parser.ALL:

        path=os.path.join(output_path,r'HWE\HWE.txt')
        df=pd.DataFrame(pd.read_csv(path,sep='\t',header=0))

        '''Plot the different percentiles for each of the allelic frequencies.'''
        fig, ax = plt.subplots(figsize=(8,8))
        ax.plot(df.iloc[:,[2]],df['25th_percentile'],label='25th percentile',c='red',ls='--',alpha=0.6)
        ax.plot(df.iloc[:,[2]],df['median'],label='median',c='black',ls='--',alpha=0.8)
        ax.plot(df.iloc[:,[2]],df['75th_percentile'],label='75th percentile',c='blue',ls='--',alpha=0.6)
        ax.set_xticks(ticks=np.arange(0,1.1,0.1),fontsize=12)
        ax.set_xlabel('1st Allele frequency',fontsize=15)
        ax.set_title('HWE summary',fontsize=22)
        ax.legend()
        fig.savefig(os.path.join(os.path.join(output_path,'HWE','HWE_plot.png')),format='png')
        plt.close(fig)

