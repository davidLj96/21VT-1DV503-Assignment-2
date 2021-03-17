import csv
import mysql.connector
from mysql.connector import errorcode
import msvcrt as m
import sys

cnx = mysql.connector.connect(user='root',
                              password='root',
                              unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',
                              )
DB_NAME = 'ljungberg'
cursor=cnx.cursor()
def create_database(cursor, DB_NAME): #code was taken from the example cars without asking the Illir for permission aswell as connect_to_db
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def connect_to_db(DB_NAME):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME

        else:
            print(err)

def create_table_planet(cursor):
    create_planet = "CREATE TABLE `planet` (" \
                 "  `planet` varchar(100) NOT NULL," \
                 "  `rotation_period` varchar(100)," \
                 "  `orbital_period` varchar(100)," \
                 "  `diameter` varchar(100)," \
                 "  `climate` varchar(100)," \
                 "  `gravity` varchar(100)," \
                 "  `terrain` varchar(100)," \
                 "  `surface_water` varchar(100)," \
                 "  `population` varchar(100)," \
                 "  PRIMARY KEY (`planet`)" \
                 ") ENGINE=InnoDB"
                 
    try:
        print("Creating table planet: ")
        cursor.execute(create_planet)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

def create_table_species(cursor):
    create_species = "CREATE TABLE `species` (" \
                 "  `species` varchar(100) NOT NULL," \
                 "  `classification` varchar(100)," \
                 "  `designation` varchar(100)," \
                 "  `average_height` varchar(100)," \
                 "  `skin_colors` varchar(100)," \
                 "  `hair_colors` varchar(100)," \
                 "  `eye_colors` varchar(100)," \
                 "  `average_lifespan` varchar(100)," \
                 "  `language` varchar(100)," \
                 "  `homeworld` varchar(100)," \
                 "  PRIMARY KEY (`species`)" \
                 ") ENGINE=InnoDB"
                 
    try:
        print("Creating table species: ")
        cursor.execute(create_species)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
          
def create_table_characters(cursor):
    create_characters = "CREATE TABLE `characters` (" \
                 "  `name` varchar(100) NOT NULL," \
                 "  `height` varchar(100)," \
                 "  `mass` varchar(100)," \
                 "  `hair_color` varchar(100)," \
                 "  `skin_color` varchar(100)," \
                 "  `eye_color` varchar(100)," \
                 "  `birth_year` varchar(100)," \
                 "  `gender` varchar(100)," \
                 "  `homeworld` varchar(100)," \
                 "  `specie` varchar(100) NOT NULL," \
                 "  PRIMARY KEY (`name`)" \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table characters: ")
        cursor.execute(create_characters)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:   
            print(err.msg)
                 

def insert_into_species(cursor):
    with open('species.csv',) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0]!="name":
                sql="INSERT INTO species (species, classification, designation, average_height, skin_colors, hair_colors, eye_colors, average_lifespan, language, homeworld) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9] ) 
                try:
                    cursor.execute(sql,val)
                except:
                    pass
                cnx.commit()

def insert_into_planet(cursor):
    with open('planets.csv',) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0]!="name":
                sql="INSERT INTO planet (planet, rotation_period, orbital_period, diameter, climate, gravity, terrain ,surface_water, population) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8] ) 

                try:
                    cursor.execute(sql,val)
                except:
                    pass
                cnx.commit()

def insert_into_characters(cursor):
  with open('characters.csv') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0]!="name":
                sql="INSERT INTO characters (name, height, mass, hair_color ,skin_color, eye_color, birth_year, gender, homeworld, specie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9] ) 
                try:
                    cursor.execute(sql,val)
                except:
                    pass
                cnx.commit()


def average_lifespan():#gives the average lifespan based on the classification of the species.
    query="SELECT classification , AVG(average_lifespan) FROM species GROUP BY classification HAVING AVG(average_lifespan)!='NA'"
    cursor.execute(query)
    data=cursor.fetchall()
    for i in data:
        print("-----------------------------------------------------------------")
        print("classification:%-20s average lifespan:%s"% (i[0],int(i[1])))
    print("-----------------------------------------------------------------")
    print("press any key to continue")
    m.getch()
    #since indefinite cant be calculate i choose not to have it in the output.
    #classifications that have only NA os and output haave also been removed as it can be seen as they then only live under 1 year.

def compare_height():#compares average height of a species on a planet to the overall heagh of the species this data is taken from the known characters in the star wars universe
    compare="Y"
    while compare=="Y":  

        #gather what data the user want to see
        specie = input("please enter a name of a specie:\n")
        planet = input("please enter a planets name:\n")
        planet_specific= input("please enter a planet charistic to compare (rotation_period, orbital_period, diameter,climate,gravity,terrain,surface_water,population);\n")    

        #creates th query
        query = "SELECT"\
                        " specie,"\
                        "AVG(height),"\
                        "species.average_height,"\
                        "characters.homeworld,"\
                        "planet."+planet_specific+""\
                    " FROM"\
                        " characters"\
                    " INNER JOIN"\
                        " species on characters.specie=species.species"\
                    " INNER JOIN"\
                        " planet on characters.homeworld=planet"\
                    " WHERE"\
                        " characters.specie='"+specie+"' AND characters.homeworld='"+planet+"';"

        cursor.execute(query)
        data = cursor.fetchall()
        #prints the data in a nice format for view
        print("\nspecie: "+(data[0][0])+"\n"\
            "average height on specie (planet): ",int(data[0][1]),"\n"\
            "average on specie (general): ",int(data[0][2]),"\n"\
            "planet: "+data[0][3]+"\n"\
            "planet "+planet_specific+": "+str(data[0][4])+"\n")

        #checks if the user want to look up other statistics
        compare = input("want to compare with another planet, species or planet charestic?(Y/N)")

def inspect_classifications(): #finds what classifications of characters
    cursor.execute("DROP VIEW IF EXISTS class;")  

    #gives the user all avalible classifications
    show_name = input("want to see all classifications with names in the database(Y/N)?: ")
    if show_name == "Y":
        query = "SELECT DISTINCT classification FROM species INNER JOIN characters on specie=species "
        cursor.execute(query)
        data=cursor.fetchall()
        for i in data:
            print(i[0])

    #creates the query to se all the species and characters that exists in the desired classificaion
    classification = input("please enter a classification you want to inspect: ")
    query = "CREATE VIEW class as "\
            "SELECT "\
                "name,species,classification "\
            "FROM "\
                "species "\
            "INNER JOIN "\
                "characters "\
            "ON "\
                "species=specie"\
            " where classification='"+classification+"';"
    cursor.execute(query)

    choice=0
    while choice!=4:
        choice=int(input("\n+================================================================+\n"\
            "|1.view all character within classification and their species.   |\n"\
            "|2.view species grouped by known characters.                     |\n"\
            "|3.view all character by specified species                       |\n"\
            "|4.back                                                          |\n"\
            "+================================================================+\n"))

        if choice==1:
            view_characters_by_species()
        if choice==2:
            view_species_by_group()
        if choice==3:
            view_specie()


    cursor.execute("DROP VIEW IF EXISTS class;")  

def view_characters_by_species(): # Uses view from inspect classifications to compare species and characaters
    cursor.execute("SELECT name,species FROM class")
    data = cursor.fetchall()

    for i in data:
        print("-----------------------------------------------------------------")
        print("name:%-30s species:%-20s|"% (i[0],i[1]))
    print("-----------------------------------------------------------------")
    print("press any key to continue")
    m.getch()

def view_species_by_group():  #counts how many characters each classification contains
 

    cursor.execute("SELECT COUNT(name),species FROM class GROUP BY species ")
    data = cursor.fetchall()
    for i in data:
        print("-----------------------------------------------------------------")
        print("specie:%-30s number of characters:%s"% (i[1],i[0]))
    print("-----------------------------------------------------------------")
    print("press any key to continue")
    m.getch()

def view_specie(): # Uses view from inspect classificaion to view all characters from a specie
    view_all = input("want to view all species within the classification?(Y/N): ")
    if view_all == "Y":
        cursor.execute("SELECT DISTINCT species FROM class;")
    data = cursor.fetchall()
    for i in data:
        print("|%-10s|"%(i[0]),end="")
    print("")

    specie = input("please enter a specific species: ")
    cursor.execute("SELECT name FROM class where species='"+specie+"';")
    data = cursor.fetchall()
    for i in data:
        print(i[0])
    print("\npress any key to continue")
    m.getch()

def characters_height(): #checks height of different characters
    height = input("please enter lowest desired height:\n")

    #gets info from mysql
    query="SELECT"\
        " name, height"\
    " FROM"\
        " characters"\
    " WHERE"\
        " height >=" +height+""

    cursor.execute(query)
    data=cursor.fetchall()

    for i in data:
        print("-------------------------------------------------------------------|")
        print("name:%-30s |   height:%-20s|"% (i[0],i[1]))
    print("-------------------------------------------------------------------|")
    print("\npress any key to continue")
    m.getch()

def UI():# This is the user interface where the user can select what statistik they want to see
    a=0
    while a!=5:
        a=int(input("\n+================================================================+\n"\
            "|1.What is the average lifespan per species classification?      |\n"\
            "|2.compare the avarege height on the different planets           |\n"\
            "|3.Inspect classifications                                       |\n"\
            "|4.character height                                              |\n"\
            "|5.End program                                                   |\n"\
            "+================================================================+\n"))
        

        if a==1:
            average_lifespan()
        elif a==2:
            compare_height()
        elif a==3:
            inspect_classifications()
        elif a==4:
            characters_height()


#"boots" up the program 
connect_to_db(DB_NAME)
create_table_planet(cursor)
insert_into_planet(cursor)
create_table_species(cursor)
insert_into_species(cursor)
create_table_characters(cursor)
insert_into_characters(cursor)
UI()

