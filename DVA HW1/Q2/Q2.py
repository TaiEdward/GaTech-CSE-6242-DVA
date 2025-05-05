########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "gtai3"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = '''
        CREATE TABLE IF NOT EXISTS movies (
            id integer,
            title text,
            score real
        )
        
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = '''
        CREATE TABLE IF NOT EXISTS movie_cast(
            movie_id integer,
            cast_id integer,
            cast_name text,
            birthday text,
            popularity real)
       
        
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        with open(path,'r') as movie_csv:
            csv_reader=csv.reader(movie_csv)
     
            for row in csv_reader:
                connection.execute('''
                insert into movies (id,title,score)
                values(?,?,?)
            ''',(row[0],row[1],row[2]))
            connection.commit()
            
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        with open(path,'r') as movie_cast_csv:
            csv_reader=csv.reader(movie_cast_csv)
     
            for row in csv_reader:
                connection.execute('''
                insert into movie_cast (movie_id,cast_id,cast_name,birthday,popularity)
                values(?,?,?,?,?)
            ''',(row[0],row[1],row[2],row[3],row[4]))
            connection.commit()
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = '''
        CREATE TABLE IF NOT EXISTS cast_bio (
        cast_id integer,
        cast_name text,
        birthday text,
        popularity real
        )'''
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql ='''
        insert into cast_bio
        (cast_id,
         cast_name,
         birthday,
         popularity)
        select distinct cast_id,cast_name,birthday,popularity from movie_cast'''
     
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = '''
        create index if not exists movie_index on movies(id)'''
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql ='''
        create index if not exists cast_index on movie_cast(cast_id)'''
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = '''
        create index if not exists cast_bio_index on cast_bio(cast_id)'''
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        
        part_c_sql = '''
        SELECT printf('%.2f',COUNT(id)/(select count(id)*1.0 from movies)*100) FROM movies WHERE score >= 7 AND score <= 20'''

    # Execute the query
        cursor = connection.execute(part_c_sql)
        Proportion = cursor.fetchall()[0][0]

    # Return the proportion
        return Proportion
       



    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql ='''
        select distinct cast_name, count(movie_id) as appearance_count 
        from movie_cast
        where popularity>10 
        group by cast_id
        order by appearance_count desc,cast_name limit 5
        '''
      
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = '''
        select distinct movie_title, printf('%.2f', score) AS score,cast_count from
        (select distinct a.title as movie_title,max(a.score) as score, count(distinct b.cast_id) as cast_count
         from movies a inner join movie_cast b on a.id=b.movie_id
         group by a.id
        order by score desc, cast_count, movie_title limit 5)'''
        
        
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
        
        ######################################################################
        
         
    
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = '''
        select distinct cast_id, cast_name,average_score from 
        (select distinct t1.cast_id,t1.cast_name,printf("%.2f",avg(t2.score)) as average_score,count(t2.id) as cnt from
         movie_cast t1 inner join movies t2 on t1.movie_id=t2.id and t2.score>=25
         group by t1.cast_id
         having cnt>=3)
        order by average_score desc,cast_name limit 10'''

        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = '''
        CREATE VIEW good_collaboration AS
        SELECT distinct
        MIN(a.cast_id) AS cast_member_id1,
        MAX(b.cast_id) AS cast_member_id2,
        COUNT(DISTINCT a.movie_id) AS movie_count,
        AVG(c.score) AS average_movie_score
        FROM movie_cast a JOIN movie_cast b ON a.movie_id = b.movie_id AND a.cast_id < b.cast_id
        JOIN movies c ON a.movie_id = c.id
        GROUP BY a.cast_id, b.cast_id
        HAVING movie_count >= 2 and average_movie_score>=40;
        
        '''
        

        
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = '''
        
        select
        distinct t1.cast_id,t2.cast_name,printf("%.2f",avg(t1.average_movie_score)) as collaboration_score
        from
        (select  cast_member_id1 as cast_id,average_movie_score from good_collaboration
        union all
        select  cast_member_id2 as cast_id,average_movie_score from good_collaboration
        ) t1 
        inner join movie_cast t2 on t1.cast_id=t2.cast_id
        group by t1.cast_id
        order by avg(t1.average_movie_score) desc, cast_name limit 5
        
        '''
        

        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = '''
        create virtual table movie_overview using fts4(
            id integer,
            overview text)
        '''
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path,'r') as movie_overview:
            csv_reader=csv.reader(movie_overview)
     
            for row in csv_reader:
                connection.execute('''
                insert into movie_overview (id,overview)
                values(?,?)
            ''',(row[0],row[1]))
            connection.commit()
        
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = '''
        select count(distinct id) from movie_overview
        where overview match 'fight'  COLLATE NOCASE '''
        
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = '''
        select count(distinct id) from movie_overview
        WHERE overview MATCH 'space NEAR/5 program' COLLATE NOCASE
        '''
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except Exception as e:
         print("Error in Part a.i")
         print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except Exception as e:
        print("Error in part a.ii")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except Exception as e:
        print("Error in part a.iii")
        print(e)

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except Exception as e:
        print("Error in part b")
        print(e)

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except Exception as e:
        print("Error in part c")
        print(e)

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part d")
        print(e)

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part e")
        print(e)

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part f")
        print(e)
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m", conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part g")
        print(e)

    try:   
        print('\033[32m' + "part h: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.i: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hii(conn)))
    except Exception as e:
        print("Error in part h")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################
  
