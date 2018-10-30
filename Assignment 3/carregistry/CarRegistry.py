import sqlite3
from itertools import chain

class CarRegistry:
    # Initialize the CarRegistry. The name of the database file used for
    # this instance is given as a parameter. This database will in some
    # cases be pre populated, and in some cases empty.
    # You do not need to change this function.
    def __init__(self, databaseName):
        self.db = sqlite3.connect(databaseName)

    # Clean up the database. You do not need to change this function.
    def close(self):
        self.db.close()

    # This function should create the two tables registrations and models.
    # You can assume the tables do not exist.
    def createTables(self):
        c = self.db.cursor()

        sqlModels = 'CREATE TABLE models(modelId INTEGER PRIMARY KEY, brand TEXT, maxSpeed REAL)'
        sqlRegistrations = 'CREATE TABLE registrations(carId TEXT PRIMARY KEY, modelId INTEGER, registrationYear INTEGER, price REAL, FOREIGN KEY(modelId) REFERENCES models(modelId))'

        c.execute(sqlModels)
        c.execute(sqlRegistrations)

        self.db.commit()

    # Add a row to the models table.
    def addCarModel(self, modelId, brand, maxSpeed):
        c = self.db.cursor()

        sql = 'INSERT INTO models(modelId, brand, maxSpeed) VALUES (?, ?, ?)'
        c.execute(sql, (modelId, brand, maxSpeed))

        self.db.commit()

    # Add a row to the registration table.
    def registerCar(self, carId, modelId, registrationYear, price):
        c = self.db.cursor()

        sql = 'INSERT INTO registrations(carId, modelId, registrationYear, price) VALUES (?, ?, ?, ?)'
        c.execute(sql, (carId, modelId, registrationYear, price))

        self.db.commit()

    # Delete the row with the given carId from the registration table.
    def deleteRegistration(self, carId):
        c = self.db.cursor()

        sql = 'DELETE FROM registrations WHERE carId=?'
        c.execute(sql, (carId,))

        self.db.commit()

    # Update the price of the registration with the given carId.
    def updatePrice(self, carId, newPrice):
        c = self.db.cursor()

        sql = 'UPDATE registrations SET price=? WHERE carId=?'
        c.execute(sql, (newPrice,carId))

        self.db.commit()

    # Populate the registration and models tables with meaningful data.
    # Ie. carIds must be unique, for any modelId in registration there
    # should be a corresponding row in models, etc. You must add at least
    # 10 rows to each of the two tables.
    def populateSampleData(self):
        self.addCarModel(1, "Alfa Romeo", 225)
        self.addCarModel(2, "Aston Martin", 297)
        self.addCarModel(3, "BMW", 255)
        self.addCarModel(12, "BMW", 200)
        self.addCarModel(4, "Bugatti", 452)
        self.addCarModel(5, "Volvo", 235)
        self.addCarModel(6, "Mercedes", 255)
        self.addCarModel(7, "Citroen", 175)
        self.addCarModel(8, "Ford", 155)
        self.addCarModel(9, "Suzuki", 255)
        self.addCarModel(11, "MG", 165)
        self.registerCar("DK12346", 1, 2016, 150000)
        self.registerCar("DK12347", 2, 2008, 1500000)
        self.registerCar("DK12348", 3, 2017, 350000)
        self.registerCar("DK12349", 4, 2016, 9500000)
        self.registerCar("DK12350", 5, 2015, 500000)
        self.registerCar("DK12351", 6, 2015, 750000)
        self.registerCar("DK12352", 7, 2013, 100000)
        self.registerCar("DK12353", 8, 2015, 99000)
        self.registerCar("DK12354", 9, 2016, 87000)
        self.registerCar("DK12355", 11, 2000, 60000)
        self.registerCar("DK12356", 3, 2015, 980000)
        self.registerCar("DK12357", 4, 2013, 9000000)
        self.registerCar("DK12358", 5, 2016, 900000)
        self.registerCar("DK12359", 6, 2014, 670000)
        self.db.commit()

    # Should output all models in the table. For each row in the table,
    # it should output a line as "modelId,brand,maxSpeed" and nothing else.
    def printModelsAsCsv(self):
        c = self.db.cursor()

        sql = 'SELECT * FROM models'

        # Run trough each row of the result and print the values of the tuple
        # joined by a comma.
        for row in c.execute(sql):
            print(','.join(str(e) for e in row))

    # Should output all registrations in the table. For each row in the table,
    # it should output a line as "carId,modelId,registrationYear,price" and nothing else.
    def printRegistrationsAsCsv(self):
        c = self.db.cursor()

        sql = 'SELECT * FROM registrations'

        # Run trough each row of the result and print the values of the tuple
        # joined by a comma.
        for row in c.execute(sql):
            print(','.join(str(e) for e in row))

    # Should return the average price of all registrered cars.
	# WARNING: You should NOT just retrieve all registrations from
	# the database and process afterwards (points may be subtracted then)
    def averagePrice(self):
        c = self.db.cursor()

        sql = 'SELECT AVG(price) FROM registrations'
        c.execute(sql)

        return c.fetchone()[0]

    # Return the number of registration where registration year is
    # between startYear and endYear (both inclusive).
	# WARNING: You should NOT just retrieve all registrations from
	# the databse and process afterwards (points may be subtracted then)
    def numberOfRegistrationsBetween(self, startYear, endYear):
        c = self.db.cursor()

        sql = 'SELECT COUNT(*) FROM registrations WHERE registrationYear >=? AND registrationYear <= ?'
        c.execute(sql, (startYear, endYear))

        return c.fetchone()[0]

    # Return a list of all brands that have at least one car strictly
    # faster than the given speed.
	# WARNING: You should NOT just retrieve all models from
	# the databse and process afterwards (points may be subtracted then)
    def brandsWithACarFasterThan(self, speed):
        c = self.db.cursor()

        sql = 'SELECT DISTINCT brand FROM models WHERE maxSpeed > ?'
        c.execute(sql, (speed,))

        rows = c.fetchall()

        # Make a list of all the first values of the tuples in rows
        result = [row[0] for row in rows]
        return result

    # Return the average price of cars with a given brand.
	# WARNING: You should NOT just retrieve all models/registrations from
	# the databse and process afterwards (points may be subtracted then)
    def averagePriceOfBrand(self, brand):
        c = self.db.cursor()

        sql = 'SELECT AVG(registrations.price) FROM models INNER JOIN registrations ON registrations.modelId = models.modelId WHERE models.brand = ?'
        c.execute(sql, (brand,))

        return c.fetchone()[0]

    # This function should create an index that ensures
    # queries of the following form execute fast:
    # SELECT * FROM registrations WHERE registrationYear > 100
    def createIndexForYearQueries(self):
        c = self.db.cursor()

        sql = 'CREATE INDEX registrationYearIndex ON registrations(registrationYear)'
        c.execute(sql)
