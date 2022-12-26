import sqlite3
import pandas as pd

def Input_DB_file_LSTM(a) :
    #createDB
    conn = sqlite3.connect ("binar_LSTM.db")
    # create table
    conn. execute("CREATE TABLE IF NOT EXISTS fileLSTM (clean_text varchar (255), label varchar (255));")
    # ubah ke dataframe
    a = pd.DataFrame(a)
    a.rename (columns={'text': "clean_text", 'label': "label"}, inplace=True)
    # print(a)
    # insert to database
    a.to_sql('fileLSTM', con=conn, index=False, if_exists='append') ## if_exists -› replace -> bikin tabel baru, senghapus y3 lass
    #commit the changes to db 
    conn.commit ()
    #close the connection 
    conn.close()
    print ("Data berhasil disimpan di db sqlite")

def Input_DB_text_LSTM(a,b):
    #create DB
    conn = sqlite3.connect ("binar_LSTM.db")
    # create table
    conn. execute("CREATE TABLE IF NOT EXISTS stringLSTM (clean_text varchar (255), label varchar (255));")
    # insert data
    conn.execute("INSERT into stringLSTM (clean_text, label) values (?,?)", (a,b))
    #commit to change to db
    conn.commit ()
    #close the connection 
    conn.close()
    print ("Data berhasil disimpan di db sqlite")
