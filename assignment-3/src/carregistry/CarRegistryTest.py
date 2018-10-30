from CarRegistry import CarRegistry

# Below are examples of how to call each of the functions in the CarRegistry.
# You probably wont to comment out/in some of these depending on what you are testing.

registry = CarRegistry("CarRegistry.sqlite")

registry.createTables()
registry.addCarModel(10, "Audi", 240)
registry.registerCar("DK12345", 10, 2014, 900000)
#registry.deleteRegistration("DK12345")
registry.updatePrice("DK12345", 870000)
registry.populateSampleData()
registry.printModelsAsCsv()
registry.printRegistrationsAsCsv()
print("Average price:", registry.averagePrice())
print("Registrations between:", registry.numberOfRegistrationsBetween(2014, 2016))
print("Fast brands:", registry.brandsWithACarFasterThan(220))
print("Average price of Audis: ", registry.averagePriceOfBrand("Audi"))
print("Average price of BMW: ", registry.averagePriceOfBrand("BMW"))
#registry.createIndexForYearQueries()
