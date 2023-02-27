import re
import os

def parse_bcf(input_file,output_path,parser):
   
    bcf=open(input_file,'r') #Open the input file as readable 
    
    with bcf as fr:
        for line in fr: #Iterate line by line in the open file handler
        
            if "Summary numbers" in line: #Check if the line contains the section descriptor we are searching for
                description_table={} # Create an emtpy data stucture to store future parsed values
                Note="" # Create empty string to store future values
                break_flag=False #Variable to signal when to break out of nested for loop
                for seq_line in fr: #Iterate through lines found after the section descriptor
                    if (seq_line.startswith('#   ')):  # Find lines which contain descriptors of the Summary Number Keys
                        seq_line=seq_line.lstrip("#").rstrip('\n') # Clean the lines of ancilliary characters
                        seq_line_split=re.split('\.{2,}',seq_line) # Split the line on '..'
                        try:
                            description_table[seq_line_split[0].lstrip(" ").rstrip(" ")]=seq_line_split[1].lstrip(" ").rstrip(" ") # Add the Summary Number key-value pairs into the description table dictionary
                        except IndexError: # A try and Error block was created to deal with empty and indented strings in this section.
                            if (seq_line_split[0].lstrip(" ").startswith('Note') or len(Note)>0):
                                Note+=" " + seq_line_split[0].lstrip(" ") # Add strings to the note variable if string starts with Note or if it has been appended to by previous lines.
                            else:
                                description_table['number of others']=description_table['number of others'] + " " + seq_line_split[0].lstrip(" ").rstrip(" ") #Add certain indented strings to the 'Number of Others' key in the descriptor table.
                                
                    if seq_line.startswith("# SN"): # Check if line starts with this section header we are searching for
                        header=re.sub('[#\d\[\]]','',seq_line.replace(" ","_")).lstrip('_') #Replace numeric and special characters 
                        if parser.sn or parser.ALL: # Check if the user wants to export the SN section 
                            try: #Check if the required .txt file exists, if not, create and open it
                                fw=open(os.path.join(output_path,'SN','SN.txt'),'w')
                            except FileNotFoundError:
                                os.mkdir(os.path.join(output_path, 'SN'))
                                fw=open(os.path.join(output_path,'SN','SN.txt'),'w')
                        for key in description_table: # Print out the Summary Number descriptor section
                            print('\n'+ key + " : " + description_table[key])
                            if parser.sn or parser.ALL: # Write in the required file if user requested it
                                fw.write(key + ' : ' + description_table[key] + '\n')
                        print('\n'+ 'Note:' + Note + '\n') # Print out the Note section from the Summary NUmber section
                        print('\n'+ header + '\n') # Print the table header
                        if parser.sn or parser.ALL: # Write the Note section and the section header in the output file if the user requsted an output file.
                            fw.write('\n'+ "Note:" + Note + '\n')
                            fw.write('\n' + header + '\n')
                        for seq_line_2 in fr: #Iterate through the lines after the section header.
                            if 'transitions' in seq_line_2: #Check if the next section has been reached yet. If so, break out of the 'seq_line_2' For loop.
                                break_flag=True #Set break flag to True to break out of the outer 'seq_line' For loop
                                break
                            print(seq_line_2)
                            if parser.sn or parser.ALL: # Check if user requested this section, if so, write it into the SN.txt file.
                                value= seq_line_2.strip('\n')
                                fw.write(value +'\n')
                    if break_flag: #  If True, break out of 'seq_line' For loop
                        if parser.sn or parser.ALL: #Close the fw file handler if it had been opened
                            fw.close()
                        break

            if '# TSTV' in line and (parser.tstv or parser.ALL): # Check if the line starts with the required section header and if the user requested this section  
                header=line.rstrip('\n').replace(" ","_") 
                header=re.sub('(\[\d\])|#','',header).lstrip("_") # Clean the header line off unrequired characters
                value=next(fr).strip('\n') # Iterate to the next line after the header to extract the values of this table
                try: 
                    os.mkdir(os.path.join(output_path, 'TSTV')) # Make the subfolder to store this section
                except FileExistsError: # Handle the exception if this subfolder already exists.
                    if os.path.isfile(os.path.join(output_path,'TSTV','TSTV.txt')): # Check if the a file with the same name as the file we are going to create exists. If so, inform the user that this file has been overwritten. 
                        print( '\n' + 'An existing file named TSTV.txt existed in this location. It has been overwritten to create the current TSTV.txt file.')
                fw=open(os.path.join(output_path,'TSTV','TSTV.txt'),'w') #Open and write the requested file.
                fw.write(header +"\n"+value)
                fw.close()

            
            if '# SiS' in line and (parser.sis or parser.ALL): # The same logic as the previous section is followed here.
                header=next(fr).rstrip('\n').replace(" ","_")
                header=re.sub('[#\d\[\]]','',header).lstrip("_")
                value=next(fr).strip('\n')
                try:
                    os.mkdir(os.path.join(output_path,'SiS'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'SiS','SiS.txt')):
                        print( '\n'+'An existing file named SiS.txt existed in this location. It has been overwritten to create the current SiS.txt file.')  
                with open(os.path.join(output_path,'SiS','SiS.txt'),'w') as fw: 
                    fw.write(header + '\n' + value)
                    fw.close()

            
            if (line.startswith('# AF') and (parser.af or parser.ALL)): # The same logic as the previous section is followed
                header=next(fr).rstrip('\n').replace(" ","_")
                header=re.sub('[#\d\[\]]','',header).lstrip('_')
                try:
                    os.mkdir(os.path.join(output_path,'AF'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'AF','AF.txt')):
                        print( '\n'+'An existing file named AF.txt existed in this location. It has been overwritten to create the current AF.txt file.')

                with open(os.path.join(output_path,'AF','AF.txt'),'w') as fw: # Open the file to be written.
                    fw.write(header + '\n') #Add the Section Header to the file 
                    for seq_line in fr: # Iterate through the lines after the Section Header
                        if seq_line.startswith('# QUAL'): # Check if the next section header has been reached. If so, break out of this 'seq_line' For loop.
                            break
                        fw.write(seq_line +'\n') # Write each line from this section into the open file.
                    fw.close()
            
            if (line.startswith('# QUAL') and (parser.q or parser.ALL)): # The same logic as the previous section is followed.
                
                if not (parser.af or parser.ALL): #Check if the previous section was iterated through. If so, it means that this section Descriptor was previously reached by the file pointer and the current line is the Section Table Header.
                    header=next(fr).strip('\n').replace(" ","_") #If the Previous Section was not reached, it means the file pointer is currently at the Section Descriptor and therefore the next line is the Section Table Header.
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('(\[\d\])|#','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'QUAL'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'QUAL','QUAL.txt')):
                        print( '\n'+'An existing file named QUAL.txt existed in this location. It has been overwritten to create the current QUAL.txt file.')

                with open(os.path.join(output_path,'QUAL','QUAL.txt'),'w') as fw:
                    fw.write(header + '\n')
                    for seq_line in fr:
                        if seq_line.startswith('# IDD'): #Check if the next Section Descriptor has been reached, if so break out of this For loop.
                            break
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()

            if (line.startswith('# IDD') and (parser.idd or parser.ALL)): # The same logic as the previous section is followed. 
                if not (parser.q or parser.ALL): 
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('(\[\w\])|#','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'IDD'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'IDD','IDD.txt')):
                        print( '\n'+'An existing file named IDD.txt existed in this location. It has been overwritten to create the current IDD.txt file.')

                with open(os.path.join(output_path,'IDD','IDD.txt'),'w') as fw:
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        if seq_line.startswith('# ST'): #Check if the next Section Descriptor has been reached, if so break out of this For loop and search for a different Section Descriptor.
                            break
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()

            if (line.startswith('# ST') and (parser.st or parser.ALL)): # The same logic as the previous section is followed.
                if not (parser.idd or parser.ALL): 
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('(\[\w\])|#','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'ST'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'ST','ST.txt')):
                        print( '\n'+'An existing file named ST.txt existed in this location. It has been overwritten to create the current ST.txt file.')

                with open(os.path.join(output_path,'ST','ST.txt'),'w') as fw: 
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        if seq_line.startswith('# DP'): #Check if the next Section Descriptor has been reached, if so break out of this For loop and search for a different Section Descriptor.
                            break 
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()
            
            if (line.startswith("# DP") and (parser.dp or parser.ALL)): # The same logic as the previous section is followed.
                if not (parser.st or parser.ALL):
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('[#\d\[\]]','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'DP'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'DP','DP.txt')):
                        print( '\n'+'An existing file named DP.txt existed in this location. It has been overwritten to create the current DP.txt file.')

                with open(os.path.join(output_path,'DP','DP.txt'),'w') as fw: 
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        if seq_line.startswith('# PSC'): #Check if the next Section Descriptor has been reached, if so break out of this For loop and search for a different Section Descriptor.
                            break 
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()

            
            if (line.startswith('# PSC') and (parser.psc or parser.ALL)): # The same logic as the previous section is followed.
                if not (parser.dp or parser.ALL):
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('[#\d\[\]]','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'PSC'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'PSC','PSC.txt')):
                        print( '\n'+'An existing file named PSC.txt existed in this location. It has been overwritten to create the current PSC.txt file.')

                with open(os.path.join(output_path,'PSC','PSC.txt'),'w') as fw:
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        if seq_line.startswith('# PSI'): #Check if the next Section Descriptor has been reached, if so break out of this For loop and search for a different Section Descriptor.
                            break
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()


            if (line.startswith('# PSI') and (parser.psi or parser.ALL)): # The same logic as the previous section is followed.
                if not (parser.psc or parser.ALL):
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","")
                header=re.sub('[#\d\[\]]','',header).lstrip("_")
                try:
                    os.mkdir(os.path.join(output_path,'PSI'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'PSI','PSI.txt')):
                        print( '\n'+'An existing file named PSI.txt existed in this location. It has been overwritten to create the current PSI.txt file.')

                with open(os.path.join(output_path,'PSI','PSI.txt'),'w') as fw: 
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        if seq_line.startswith('# HWE'): #Check if the next Section Descriptor has been reached, if so break out of this For loop and search for a different Section Descriptor.
                            break 
                        value=seq_line.strip('\n')
                        fw.write(value + '\n')
                    fw.close()      

            if (line.startswith('# HWE') and (parser.hwe or parser.ALL)): 
                if not (parser.psi or parser.ALL):
                    header=next(fr).strip('\n').replace(" ","_")
                else: 
                    header=line.strip('\n').replace(" ","_")
                header=re.sub('(\[\d\])|#','',header).lstrip("_")
                
                try:
                    os.mkdir(os.path.join(output_path,'HWE'))
                except FileExistsError:
                    if os.path.isfile(os.path.join(output_path,'HWE','HWE.txt')):
                        print( '\n'+'An existing file named HWE.txt existed in this location. It has been overwritten to create the current HWE.txt file.')

                with open(os.path.join(output_path,'HWE','HWE.txt'),'w') as fw: 
                    fw.write(header + '\n')
                    for seq_line in fr: 
                        value= seq_line.strip('\n')
                        fw.write(value +'\n')
                    fw.close()

        bcf.close()