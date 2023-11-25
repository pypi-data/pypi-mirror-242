__author__ = "datacorner.fr"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import pandas as pd
import pipelite.constants as C
from collections import Counter
import re
import datetime
import math
from dateutil.parser import parse

REGEX_CARS = r'[a-zA-Z]'
REGEX_NUMS = r'\d'
REGEX_NOISE = r'[µ&#@^~]'
REGEX_SPECCARS = r'[<>µ+=*&\'"#{}()|/\\@][]^~]'
REGEX_PONCT = r'[,.;:?!]'

class plDataset:
    """ This class encapsulate the data set management (currently Pandas DataFrames) 
        (here it's currently managed by using Pandas DataFrame)
    """
    def __init__(self):
        self.id = C.EMPTY
        self.__content = pd.DataFrame() # encapsulate DataFrame

    @property
    def columns(self) -> []:
        """ Returns all the dataset columns names
        Returns:
            list: columns names
        """
        return self.__content.columns

    def applyTrans(self, toColumn, function):
        self.__content[toColumn] = self.__content.apply(function, axis=1)

    def set(self, value, defaultype=None):
        """ initialize a dataset from a list ofr another Dataframe

        Args:
            value (object): other object to init from
            defaultype (_type_, optional): type by default. Defaults to None.
        """
        if (isinstance(value, list)):
            self.__content = pd.DataFrame(value, defaultype)
        elif (isinstance(value, pd.DataFrame)):
            self.__content = value
    
    def get(self) -> pd.DataFrame: 
        return self.__content
    
    def copy(self):
        """Returns a copy of the Dataset (to avoid any reference issues)
        Returns:
            etlDataset: strict copy of the current dataset
        """
        newDS = plDataset()
        newDS.id = self.id
        newDS.__content = self.__content.copy(deep=True)
        return newDS

    @property
    def count(self):
        """Return the Data rows count
        Returns:
            int: row count
        """
        return self.__content.shape[0]

    def read_sql(self, odbcConnection, query):
        """ Launch a SQL statement and get the resultset
        Args:
            odbcConnection (ODBC connection): ODBC connection via pyodbc
            query (str): SQL statement
        """
        self.__content = pd.read_sql(query, odbcConnection)

    def read_csv(self, filename, separator, encoding):
        """ Read the Data from a CSV file by using Pandas
        Args:
            filename (str): filename and path
            separator (str): CSV delimiter
            encoding (str): encoding
        """
        self.__content = pd.read_csv(filepath_or_buffer=filename, 
                                    encoding=encoding, 
                                    delimiter=separator)

    def read_excel(self, filename, sheet=0):
        # Read the Excel file and provides a DataFrame
        self.__content = pd.read_excel(filename, sheet_name=sheet) #, engine='openpyxl')

    def write_csv(self, filename, separator, encoding):
        """ Write the Data into a CSV file by using Pandas
        Args:
            filename (str): filename and path
            separator (str): CSV delimiter
            encoding (str): encoding
        """
        self.__content.to_csv(path_or_buf=filename, 
                            encoding=encoding, 
                            index=False, 
                            sep=separator)
    
    def get_csv(self, encoding=C.ENCODING):
        """return the csv content

        Args:
            encoding (_type_, optional): encoding content. Defaults to C.ENCODING UTF-8
        Returns:
            str: csv content
        """
        return self.__content.to_csv(header=True, 
                                     encoding=encoding, 
                                     dtype=str,
                                     index=False)

    def concatWith(self, etlDatasetB, keys=None):
        """Concatenate the current dataset with the one in arg
        Args:
            etlDatasetB (etlDataset): other dataset to concat
            keys (str, optional): key to concat. Defaults to None.
        """
        self.__content = pd.concat([self.__content, etlDatasetB], keys=keys)
    
    def joinWith(self, ds, on, how ="inner"):
        """ Makes a inner join from the current dataset and the given one. 
        the join is made on the mapColName which must exists in both sides
        Args:
            dsLookup (etlDataset): lookup dataset
            mapColName (str): column name on both side
            how (str) : join type -> inner (default), left, right or outer
        """
        self.__content = pd.merge(self.__content, ds, on=on, how=how)

    def dropLineNaN(self, column):
        """ Drops all rows if the column value is NaN
        Args:
            column (str): column name
        """
        self.__content = self.__content.dropna(subset=[column])

    def dropColumn(self, column):
        """Drop a column
        Args:
            column (str): column name
        """
        del self.__content[column]

    def subString(self, columnName, start, length):
        """extract a substring
        Args:
            columnName (str): column name
            start (int): start index
            length (int): extraction length
        """
        self.__content[columnName] = self.__content[columnName].str[start:start+length]

    def renameColumn(self, oldName, newName):
        """rename a column inside the dataset
        Args:
            oldName (str): Old column name
            newName (str): New column name
        """
        self.__content.rename(columns={oldName:newName}, inplace=True)

    def getRowBloc(self, rowIndexfrom, rowIndexTo):
        """ split the current content (by row) and returns the dataset which starts at row index rowIndexfrom and
            end at row index rowIndexTo
            indexes starts at 0
        Args:
            rowIndexfrom (int): row index start
            rowIndexTo (int): row index end

        Returns:
            _type_: _description_
        """
        newDatasetBloc = plDataset()
        newDatasetBloc.__content = self.__content.iloc[rowIndexfrom:rowIndexTo+1:,:]
        return newDatasetBloc

    def getStringPattern(self, string):
        """Returns the data pattern by replacing strings by S, digits by N and noises (special characters) by ?
        Args:
            string (str): data in input
        Returns:
            str: pattern
        """
        if (string == 'nan'):
            return "NULL"
        mystr = re.sub(REGEX_CARS, 'C', string)
        mystr = re.sub(REGEX_NUMS, 'N', mystr)
        mystr = re.sub(REGEX_NOISE, '?', mystr)
        #mystr = re.sub(REGEX_PONCT, 'P', mystr)
        return mystr

    def getType(self, value):
        """Returns the data type on the value in input
        Args:
            value (object): data
        Returns:
            str: type namen can be [ null, number, date, string, unknown]
        """
        if value is None:
            return "null"
        if isinstance(value, (int, float)):
            if math.isnan(value):
                return "null"
            else:
                return "number"
        elif isinstance(value, str):
            try:
                parse(value, fuzzy=False)
                return "date"
            except ValueError:
                return "string"
        elif isinstance(value, datetime.datetime):
            return "date"
        else:
            return "unknown"

    def profile(self, maxvaluecounts=10) -> dict:
        """Build a JSON which contains some basic profiling informations
        Args:
            maxvaluecounts (int, optional): Limits the number of value_counts() return. Defaults to 10.
        Returns:
            json: data profile in a JSON format
        """
        profile = {}
        # Get stats per columns/fields
        profileColumns = []
        for col in self.__content.columns:
            profileCol = {}
            counts = self.__content[col].value_counts()
            profileCol['name'] = col
            profileCol['type'] = str(self.__content[col].dtypes)
            profileCol['inferred'] = str(self.__content[col].infer_objects().dtypes)
            profileCol['distinct'] = int(len(counts))
            profileCol['nan'] = int(self.__content[col].isna().sum())
            profileCol['null'] = int(self.__content[col].isnull().sum())
            profileCol['stats'] = self.__content[col].describe().to_dict()
            profileCol['top values'] = dict(Counter(counts.to_dict()).most_common(maxvaluecounts))
            # Get pattern for that column
            dfProfPattern = pd.DataFrame()
            dfProfPattern['profile'] = self.__content[col].apply(lambda x:self.getStringPattern(str(x)))
            profileCol['pattern'] = dict(Counter(dfProfPattern['profile'].value_counts().to_dict()).most_common(maxvaluecounts))
            # get types for that columns
            dfProfType = pd.DataFrame()
            dfProfType['types'] = self.__content[col].apply(lambda x:self.getType(x))
            profileCol['types'] = dict(Counter(dfProfType['types'].value_counts().to_dict()).most_common(maxvaluecounts))
            profileColumns.append(profileCol)
        profile["rows count"] = self.count
        profile["columns count"] = len(self.__content.columns)
        profile["columns names"] = [ name for name in self.__content.columns ]
        profile["columns"] = profileColumns
        return profile

    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__content.__getitem__(item)

    def __getattr__(self, name):
        """ Makes the Data accessible via attribute name
            example: df.colName
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__content.__getattr__(name)
    
    def __str__(self):
        return self.__content.__str__()
    
    def __iter__(self):
        return iter(self.__content)