#  Watauga Court Calendar


class Calendar:
 
    def __init__(self):
        self.location = None
        self.date = None
        self.time = None
        self.run_date = None
        self.room = None
        self.entries = []

    def to_csv(self):
        csv_calendar = '{0},{1},{2},{3},"{4}"'.format(self.run_date,
                                                      self.date,
                                                      self.time,
                                                      self.room,
                                                      self.location,)

        mylist = []
        for entry in self.entries:
            for item in entry.to_csv():
                s2 ='{0},{1}'.format(csv_calendar, item)
                mylist.append(s2)
        
        return mylist
          
 
          
 
class CalendarEntry:
 
    def __init__(self):
        self.defendant = None
        self.filenumber = None
        self.attorney = None
        self.complainant = None
        self.no = None
        self.cont = None
        self.aka = None
        self.needs_fingerprinted = False
        self.bond = None
        self.charges = []
    
    def to_csv(self):
        csv_entry = '{0},{1},"{2}","{3}","{4}",{5},"{6}",{7},"{8}"'.format(self.no,
                                                                     self.filenumber,
                                                                     self.defendant,
                                                                     self.attorney,
                                                                     self.complainant,
                                                                     self.cont,
                                                                     self.aka,
                                                                     self.needs_fingerprinted,
                                                                     self.bond)
        mylist = []
        for charge in self.charges:
            s1 = '{0},{1}'.format(csv_entry, charge.to_csv())
            mylist.append(s1)
        
        return mylist
 
class Charges: 
 
    def __init__(self):
        self.crime = None
        self.plea = None
        self.verdict = None
        self.cls = None
        self.p = None
        self.l = None
        self.judgement = None
        self.ada = None
    
    def to_csv(self):
        return '{0},{1},{2},{3},{4},{5},{6},{7}'.format(self.crime,
                                                    self.plea,
                                                    self.verdict,
                                                    self.cls,
                                                    self.p,
                                                    self.l,
                                                    self.judgement,
                                                    self.ada)

class CalendarParser:
    # Constants
    HEADER_END = '*' * 20
 
    def __init__(self):
        self._currentline = None
        self._calendar = None
        self._file = None
        self._infile = None
        self._charge = None
        self._entry = None
 
    # Common functions
    def _readline(self):
        # Remove extra lines
        self._currentline = self._infile.readline().rstrip('\n')
 
    def _readnext(self):
        # Read Output from line
        while True:
            self._readline()
 
            if self._currentline == '':
                continue
            elif self.is_page_header():
                self._process_page_header()
            else:
                break
 
    # Header processing functions
    def is_report_header(self):
        return self._currentline[0] != '1' and "RUN DATE:" in self._currentline
 
    def is_page_header(self):
        return self._currentline[0] == '1' and "RUN DATE:" not in self._currentline
 
    def is_summary_header(self):
        return self._currentline[0] == '1' and "RUN DATE:" in self._currentline
 
    def is_header_end(self):
        return self.HEADER_END in self._currentline
 
    def _process_page_header(self):
        while True:
            self._readline()
            if self.is_header_end():
                break
 
    def _process_report_header(self):
        self._calendar.run_date = self._currentline[12:20]
 
        while True:
            self._readline()
            if self.is_header_end():
                break
            elif "LOCATION" in self._currentline:
                self._calendar.location = self._currentline[12:22].strip()
            elif "COURT DATE" in self._currentline:
                self._calendar.date = self._currentline[22:30].strip()
                self._calendar.time = self._currentline[44:52].strip()
                self._calendar.room = self._currentline[78:].strip()
                
    # Data processing functions
    def is_entry_start(self):
        try:
            int(self._currentline[0:6])
            return True
        except ValueError:
            return False
 
    def _process_entry(self):
        self._entry.no = int(self._currentline[0:6])
        self._entry.filenumber = self._currentline [8:20].strip()
        self._entry.defendant = self._currentline[20:42].strip()
        self._entry.attorney = self._currentline[57:81].strip()
        self._entry.complainant = self._currentline[42:61].strip()
        self._entry.cont = self._currentline[84:86].strip()
        self._entry.aka = None
        self._entry.needs_fingerprinted = None
        self._entry.bond = None

    def _process_charge(self):
        self._charge.crime = self._currentline[8:37].strip()
        self._charge.plea = self._currentline[49:65].strip()
        self._charge.verdict = self._currentline[69:84].strip()
        

        
    
    def _process_charge_2(self):
        self._charge.cls = self._currentline[12:15].strip()
        self._charge.p = self._currentline[17:20].strip()
        self._charge.l = self._currentline[22:40].strip()
        self._charge.judgement = self._currentline[49:66].strip()
        self._charge.ada = self._currentline[80:].strip()
            
    # Main parse function
    def parse(self, filename):
        # Parse a calendar text file
        self._filename = filename
        self._infile = open(filename)
        self._calendar = Calendar()
        self._entry = None
        self._charge = None
    
        self._readnext()
        while True:
            if self._currentline =='':
                break
            
            elif self.is_summary_header():
                break
            
            elif self.is_report_header():
                self._process_report_header()
            
            elif self.is_entry_start():
                if self._entry is not None:
                    self._calendar.entries.append(self._entry)
                self._entry = CalendarEntry()
                self._process_entry()
 
            elif "FINGERPRINTED" in self._currentline:
                self._entry.needs_fingerprinted = True

            elif "BOND" in self._currentline:
                self._entry.bond = self._currentline[25:].strip()
            
            elif "AKA" in self._currentline:
                self._entry.aka = self._currentline[18:].strip()
            
            elif "PLEA" in self._currentline:
                if self._charge is not None:
                    self._entry.charges.append(self._charge)

                self._charge = Charges()
                self._process_charge()
            
            elif "JUDGMENT" in self._currentline:
                self._process_charge_2()
            
            else:
                print(self._currentline)
            
            self._readnext()
    
        self._infile.close()
        return self._calendar
 
if __name__ == "__main__":
    filename = r'DISTRICT.DISTRICT_COURT_.11.15.19.AM.000B.CAL.txt'
    parser = CalendarParser()
    calendar = parser.parse(filename)
    csv_line_list = calendar.to_csv()
    # open output file
    # open new file for writing - will erase file if it already exists -
    csvfile = open('courtCalendar.csv', 'w', newline='', encoding='utf-8')
    
    # write a column headings row - do this only once -
    csvfile.write('Run Date,date,time,room,location,no,filenumber,defendant,attorney,complainant,cont,aka,fingerprint,bond,crime,plea,verdict,cls,p,l,judgement,ada\n')
    # use a for-loop to write each row into the CSV file
    for item in csv_line_list:
        # write one row to csv — item MUST BE a LIST
        csvfile.write('{0}\n'.format(item))
    
    # save and close the file
    csvfile.close() 

