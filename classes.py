class DataInfo:
    def __init__(self,df):
        self.df = df

    def info(self): 
        
        # Numero de filas
        print(f'\nFilas totales : {self.df.shape[0]} \n')
      
        # Numero de columnas
        print(f'\nColumnas totales : {self.df.shape[1]} \n')
        
        # Nombres de las columnas
        column_name =  self.df.columns 
        print(f'\nNombres de las columnas\n'+  f'\n{column_name} \n \n')
        
        # Tipo de datos (info)
        print(f'Info de los datos\n')
        data_summary = self.df.info() 
        
        # Valores nulos 
        null_values = self.df.isnull().sum() 
        print(f'\nValores nulos\n' +  f'\n{null_values} \n \n')

        # Estadística descriptiva
        describe =  self.df.describe() 
        print(f'\nEstadística descriptiva\n' + f'\n{describe} \n \n')
    
    def clean(self):
        # Eliminamos una columna
        self.df.drop(columns='Code', inplace=True)
    
    def dfcont(self):
        x = self.df[self.df['Country'].str.contains('WHO')].copy()
        x.rename(columns={'Country': 'Continent'}, inplace=True)
        return x
    def dfincome(self):
        x = self.df[self.df['Country'].str.contains('Bank')].copy()
        x.rename(columns={'Country': 'Income'}, inplace=True)
        return x