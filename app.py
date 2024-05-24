import streamlit as st
import sqlite3
import csv
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute(""" CREATE TABLE if not exists tracker_mgr(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                     Division varchar(255) not null,
                                                     Jira_ticket varchar(255) not null,
                                                     State varchar (50) not null,
                                                     Name varchar (50) not null,
                                                     Notes varchar (500) not null,
                                                     Merge varchar(50) not null,
                                                     Legacy_URL varchar(255) not null,
                                                     New_URL varchar(255) not null,  
                                                     Page_title varchar(255) not null
                                                     );""")


# with open('appendix_8.csv', 'r') as csvfile:
#     csvreader = csv.reader(csvfile)

#     # Skip the header row
#     next(csvreader)

#     # Insert data from CSV into the database
#     for row in csvreader:
#         Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title = row
#         c.execute("INSERT INTO tracker_mgr (Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                     (Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title))


# # Commit the changes and close the connection
#     conn.commit()
#     # conn.close()






# CRUD functions
# Create a new entry
def create_entry(Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title):
    c.execute("INSERT INTO tracker_mgr (Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)",
              (Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title))
    conn.commit()

# Read entries
def read_entries(Division=None):
    if Division:
        c.execute("SELECT * FROM tracker_mgr WHERE Division=?", (Division,))
    else:
        c.execute("SELECT * FROM tracker_mgr")
    return c.fetchall()

# Update an entry
def update_entry(Division=None, Jira_ticket=None, State=None, Name=None, Note=None, Merge=None, Legacy_URL=None, New_URL=None, Page_title=None):
    data = []
    set_clause = []
    if Division:
        set_clause.append("Division=?")
        data.append(Division)
    if Jira_ticket:
        set_clause.append("Jira_ticket=?")
        data.append(Jira_ticket)
    if State:
        set_clause.append("State=?")
        data.append(State)
    if Name:
        set_clause.append("Name=?")
        data.append(Name)
    if Notes:
        set_clause.append("Notes=?")
        data.append(Notes)
    if Merge:
        set_clause.append("Merge=?")
        data.append(Merge)
    if Legacy_URL:
        set_clause.append("Legacy_URL=?")
        data.append(Legacy_URL)
    if New_URL:
        set_clause.append("New_URL=?")
        data.append(New_URL)
    if Page_title:
        set_clause.append("Page_title=?")
        data.append(Page_title)
    set_clause = ", ".join(set_clause)
    data.append(id)
    c.execute(f"UPDATE tracker_mgr SET {set_clause} WHERE id=?", data)
    conn.commit()

# Delete an entry
def delete_entry(id):
    c.execute("DELETE FROM tracker_mgr WHERE id=?", (id,))
    conn.commit()

# Close the database connection
# conn.close()

def save_to_db(df):
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    cursor = conn.cursor()

    for index, row in df.iterrows():
        try:
    # Construct the SQL UPDATE statement
            
            sql = "UPDATE tracker_mgr SET Division = ?, Jira_ticket = ?, State = ?, Name = ?, Notes = ?, Merge = ?, Legacy_URL = ?, New_URL = ?, Page_title = ? WHERE id = ?"
            values = (row['Division'], row['Jira_ticket'], row['State'], row['Name'], row['Notes'], row['Merge'], row['Legacy_URL'], row['New_URL'], row['Page_title'], row['id'])

    # Execute the SQL statement
            cursor.execute(sql, values)
        except sqlite3.Error as e:
            print(f"Error updating row {index}: {e}")
            continue

    # Convert dataframe to list of tuples
    # rows = [tuple(row) for row in edited_df.to_numpy()]
    # edited_rows = [tuple(row) for row in edited_df.to_numpy()]
    # original_rows = [tuple(row) for row in changed_df.to_numpy()]

    # Clear the existing data in the table
    # c.execute("DELETE FROM tracker_mgr")
    # Find the rows that have been changed
    # changed_rows = [edited_row for edited_row in edited_rows if edited_row not in original_rows]

    # Insert the new data
    # c.executemany("INSERT INTO tracker_mgr VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)", rows)
     # Update the changed rows in the database
    # for changed_row in changed_rows:
        # c.execute("UPDATE tracker_mgr SET id=?, Division=?, Jira_ticket=?, State=?, Name=?, Notes=?, Merge=?,Legacy_URL=?,New_URL=?,Page_title=? WHERE id=? AND Division=? AND Jira_ticket=? AND State=? AND Name=? AND Notes=? AND Merge=? AND Legacy_URL=? AND New_URL=? AND Page_title=?", changed_row + changed_row)

    # Commit the changes and close the connection
        try:
            conn.commit()
        except sqlite3.Error as e:
            print(f"error committing changes:{e}")
            return
        
       
        # try:
        #     conn.close()
        # except sqlite3.Error as e:
        #     print(f"Error closing the database connection: {e}")

# def get_changed_rows(edited_df, original_df):
#     # Convert dataframes to lists of tuples
#     edited_rows = [tuple(row) for row in edited_df.to_numpy()]
#     original_rows = [tuple(row) for row in original_df.to_numpy()]

#     # Find the rows that have been changed
#     changed_rows = [row for row in edited_rows if row not in original_rows]

#     # Create a new DataFrame with the changed rows
#     changed_df = pd.DataFrame(changed_rows, columns=edited_df.columns)
    
#     return changed_df


def main():
    # Streamlit-related code goes here
    st.set_page_config(page_title="Migration Tracker", page_icon="📄", initial_sidebar_state="collapsed", layout="wide", menu_items={'About': "# This is a header. This is an *extremely* cool app!"})
    
    # st.image('SEO-Website-Migration-Strategy-Guide-1.png')
    st.title('Migration tracker')
    st.divider()
    col1, col2, col11 = st.columns(3)
    
   
    menu = ["View all", "Create"]
    choice = col1.selectbox("View all pages or create a new page", menu)

    progress = ['Backlog','In Progress', 'Content Review', 'Client Review', 'Done', 'Not Prioritized', 'Not migrating', 'Blocked']
    merge = ["Merge ⬆️", "Merge ⬇️"] 
    users = ['Jim', 'Sarah P', 'Sarah C', 'Alice', 'Open']
    divisions = ['DCI','Insurance','Finance', 'Credit Unions', 'OPC']

    config = {
      
      'Division' : st.column_config.SelectboxColumn('Division',options=divisions),  
      'Jira_ticket': st.column_config.LinkColumn('Jira Ticket'),
      'State' : st.column_config.SelectboxColumn('State', options=progress, default='Backlog'),
      'Name' : st.column_config.SelectboxColumn('Name', options=users),
      'Merge' : st.column_config.SelectboxColumn('Merge', options=merge, width="Large"),
      'Notes': st.column_config.TextColumn('Notes', width="Large"),
      'New_URL': st.column_config.TextColumn('New URL', width="Medium"),
      'Legacy_URL': st.column_config.LinkColumn('Legacy URL', help="URL to old site", validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,),
       'Page_title': st.column_config.TextColumn('Page Title')
    }





    if choice == "Create":
        st.subheader("Create a new entry")
        Division = st.text_input("Division")
        Jira_ticket = st.text_input("Jira_ticket")
        State = st.text_input("State")
        Name = st.text_input("Name")
        Notes = st.text_area("Notes")
        Merge = st.text_input("Merge")
        Legacy_URL = st.text_input("Legacy URL")
        New_URL = st.text_input("New URL")
        Page_title = st.text_input("Page Title")

        if st.button("Create"):
            create_entry(Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title)
            st.success("Entry created successfully!")

    elif choice == "View all":
        st.subheader("Page Migrations")
        st.write('Track the progress of individual page migration status for the project') 
        col3, col4, col5 = st.columns(3)
        dmenu = ["",'DCI','Insurance','Finance', 'Credit Unions', 'OPC']
        dchoice = col3.selectbox("Select a division", dmenu)
        st.write('Filter results')
        # page_num = col3.text_input("The name of the user (leave blank to show all)")
        page_num = dchoice
                
        # if st.button("Read"):
        showall = read_entries(None)
        for allentry in showall:
            # st.write(entry)
            # st.table(entries)
            columns = [desc[0] for desc in c.description]
            df_all = pd.DataFrame(showall, columns=columns)
            entries = read_entries(page_num if page_num else None)

        # with st.expander("Show raw data"):    
        #     if page_num == None:    
        #         st.dataframe(df_all)

        #     entries = read_entries(page_num if page_num else None)

        for entry in entries:
            # st.write(entry)
            # st.table(entries)
            columns = [desc[0] for desc in c.description]
            df = pd.DataFrame(entries, columns=columns)
        if page_num != None:    
            # st.dataframe(df)
        # st.dataframe(df_all)    
            edited_df = st.data_editor((df), column_config=config, column_order=('id','Division','Jira_ticket', 'State', 'Name', 'Notes','Merge','Legacy_URL','New_URL', 'Page_title'),key="data_editor")
        st.write('Make sure you save your changes')

        if st.button("Save to Database"):
            # changes = edited_df != df_all   
            # # st.dataframe(changes) 
            # changed_values = pd.DataFrame(columns=df_all.columns)
            # for col in df_all.columns:
            #     if changes[col].any():
            #         changed_values[col] = edited_df.loc[changes[col], col]
            # st.write('change values')        
            # st.dataframe(changed_values)        

            # all_rows = pd.concat([df_all, edited_df]).drop_duplicates(keep=False)

            # st.write('All Rows')
            # st.dataframe(all_rows)

                        
            # result = pd.concat([changed_values, all_rows])
            # st.write('results')
            # st.dataframe(result)
            if page_num == None:
                changes = edited_df != df_all
             
                changed_rows = edited_df.loc[changes.any(axis=1)] 
                st.dataframe(changed_rows)
            else:
                changes = edited_df != df
             
                changed_rows = edited_df.loc[changes.any(axis=1)] 
                st.dataframe(changed_rows)




            # df_all.update(changes) 

                                  

            # if "data_editor" in st.session_state:
            #     changed_rows = st.session_state["data_editor"]["edited_rows"]
            #     changed_rows
               
            
            # changed_df = pd.DataFrame.from_dict(changed_rows, orient='index')
            # # results = edited_df.loc[changed_df]
           
            # st.dataframe(changed_df)

                  
            
            save_to_db(changed_rows)
                
            st.success("Data saved to database successfully!")
            

    

        st.header('Migration Stats')  
        st.divider() 
        try: inprog = edited_df.groupby('State').size()['In Progress']  
        except KeyError:
            inprog = 0

        try: backlog = edited_df['State'].value_counts()['Backlog']  
        except KeyError:
            backlog = 0

        try: done = edited_df['State'].value_counts()['Done'] 
        except KeyError:
            done = 0 

        try: review = edited_df['State'].value_counts()['Client Review']
        except KeyError:
            review = 0   

        try: content = edited_df['State'].value_counts()['Content Review'] 
        except KeyError:
            content = 0 

        countofRows = len(edited_df)

        bcklog=round(backlog/countofRows*100)
        inp = round(inprog/countofRows*100)
        cont = round(content/countofRows*100)
        rev = round(review/countofRows*100)
        don = round(done/countofRows*100)



        with st.expander("Story Metrics"):
            st.write('Story status metrics')
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Backlog", backlog)
            col1.metric('% ', bcklog)
            col2.metric("In Progress", inprog)
            col2.metric("%", inp)
            col3.metric("Content Review", content)
            col3.metric("%", cont)
            col4.metric("Client Review", review)
            col4.metric("%", rev)
            col5.metric("Done", done)
            col5.metric("%", don)
        
        try: u1 = edited_df.groupby('Name').size()[users[0]]  
        except KeyError:
            u1 = 0

        try: u2 = edited_df.groupby('Name').size()[users[1]]  
        except KeyError:
            u2 = 0

        try: u3 = edited_df.groupby('Name').size()[users[2]]  
        except KeyError:
            u3 = 0

        try: u4 = edited_df.groupby('Name').size()[users[3]]  
        except KeyError:
            u4 = 0  

        try: u5 = edited_df.groupby('Name').size()[users[4]]  
        except KeyError:
            u5 = 0
             
        
        with st.expander("Migrator Metrics"):
            st.write('Number of stories assigned to each migrator')
            col6, col7, col8, col9, col10 = st.columns(5)
            col6.metric(users[0], u1)
            col7.metric(users[1], u2)
            col8.metric(users[2], u3)
            col9.metric(users[3], u4)
            col10.metric(users[4], u5)



    


    elif choice == "Update":
        st.subheader("Update an entry")
        st.subheader("Create a new entry")
        Division = st.text_input("Division")
        Jira_ticket = st.text_input("Jira_ticket")
        State = st.text_input("State")
        Name = st.text_input("Name")
        Notes = st.text_area("Notes")
        Merge = st.text_input("Merge")
        Legacy_URL = st.text_input("Legacy URL")
        New_URL = st.text_input("New URL")
        Page_title = st.text_input("Page Title")

        if st.button("Update"):
            update_entry(Division, Jira_ticket, State, Name, Notes, Merge, Legacy_URL, New_URL, Page_title)
            st.success("Entry updated successfully!")

    elif choice == "Delete":
        st.subheader("Delete an entry")
        page_num = st.text_input("Page Number")
        if st.button("Delete"):
            delete_entry(page_num)
            st.success("Entry deleted successfully!")

   

if __name__ == '__main__':
    main()
    conn.close()