'''
Python version 2.7.4
Author: Xiao Hu
Description: Hammurabi: The classic game of strategy and resource allocation
'''

def print_intro():
	'''print the introduction of the game the player.'''
	print """
Congratulations, you are the newest ruler of ancient Samaria, elected
for a ten year term of office. Your duties are to dispense food, direct
farming, and buy and sell land as needed to support your people. Watch
out for rat infestations and the plague! Grain is the general currency,
measured in bushels. The following will help you in your decisions:

  * Each person needs at least 20 bushels of grain per year to survive.

  * Each person can farm at most 10 acres of land.

  * It takes 2 bushels of grain to farm an acre of land.

  * The market price for land fluctuates yearly.

Rule wisely and you will be showered with appreciation at the end of
your term. Rule poorly and you will be kicked out of office!
	"""

def ask_to_buy_land(bushels, cost):
	'''Ask user how many bushels to spend buying land.'''
	acres = input("How many acres will you buy?\t")
	while acres * cost > bushels:
		print "O great Hammurabi, we have only", bushels, "bushels of grain!"
		acres = input("How many acres will you buy?\t")
	return acres

def ask_to_sell_land(acres_owned):
	'''Ask user how much land they want to sell. '''
	acres = input("How many acres will you sell?\t")
	while acres_owned<acres:
		print "O great Hammurabi, we have only", acres_owned, "acres to sell!"
		acres = input("How many acres will you buy?\t")
	return acres

def ask_to_feed(bushels):
	'''Ask user how many bushels they want to use for feeding.'''
	feed = input("How many bushels they want to use for feeding?\t")
	while feed>bushels:
		print "O great Hammurabi, we have only", bushels, "bushels of grain!"
		feed = input("How many bushels they want to use for feeding?\t")
	return feed

def ask_to_cultivate(acres, population, bushels):
	'''Ask user how much land they want to plant seed in'''
	cultivate = input("How much land they want to plant seed in?\t")
	while acres<cultivate or cultivate > population*10 or 2*cultivate > bushels:
		if acres < cultivate: print "O great Hammurabi, we have only", acres, "acres to plant in!"
		elif cultivate > population*10: print "O great Hammurabi, we can at most take", population*10, "acres to plant in!"
		elif 2*cultivate > bushels: print "O great Hammurabi, we have only", bushels, "bushels of grain!"
		cultivate = input("How much land they want to plant seed in?\t")
	return cultivate

def isPlague():
	'''judge whether or not a horrible plague happened this year'''
	#Each year, there is a 15% chance of a horrible plague. When this happens, half your people die.
	a=random.randint(1,100)
	if a>15: plague=1
	else: plague=0
	return plague

def numStarving(population, bushels):
	'''get the number of starved people'''
	#Each person needs 20 bushels of grain to survive.
	#If you feed them more than this, the grain has been wasted.
	#If more than 45% of the people starve, you will be immediately thrown out of office and the game ends.
	if population > bushels/20: starving=population-bushels/20
	else: starving=0
	return starving

def numImmigrants(land, grainInStorage, population, numStarving):
	'''get the number of immigrants'''
	if numStarving==0: Immigrants=(20*land-grainInStorage)/(100*population+1)
	else: Immigrants=0
	return Immigrants

def getHarvest():
	'''get the harvest of the land'''
	harvest=random.randint(1,8)
	return harvest

def doRatsInfest():
	'''get the infestation rate'''
	InfestRate=0
	infestation=random.randint(1,100)
	if infestation<=40: InfestRate=random.randint(10,30)
	InfestRate=InfestRate/100.0
	return InfestRate

def priceOfLand():
	'''get the price of the land'''
	price=random.randint(16,22)
	return price

def PrintUpdate(year,starved,immigrants,population,harvest,bushels_per_acre,rats_ate,bushels_in_storage,acres_owned,cost_per_acre,plague_deaths):
	print "************************************************************************************\n"
	print "O great Hammurabi!"
	print "You are in year",year,"of your ten year rule."
	print "In the previous year",starved,"people starved to death."
	print "In the previous year",immigrants,"people entered the kingdom."
	print "The population is now",population,"."
	print "We harvested",harvest,"bushels at",bushels_per_acre,"bushels per acre."
	print "Rats destroyed",rats_ate,"bushels, leaving",bushels_in_storage,"bushels in storage."
	print "The city owns",acres_owned,"acres of land."
	print "Land is currently worth",cost_per_acre,"bushels per acre."
	print "There were",plague_deaths,"deaths from the plague."
	print "************************************************************************************\n"

def Hammurabi():
	year=1
	starved = 0
	immigrants = 5
	population = 100
	harvest = 3000	# total bushels harvested
	bushels_per_acre = 3	# amount harvested for each acre planted
	rats_ate = 200	# bushels destroyed by rats
	bushels_in_storage = 2800	
	acres_owned = 1000
	cost_per_acre = 19	# each acre costs this many bushels plague_deaths = 0
	plague_deaths = 0
	print_intro()
	while year<=10:
		PrintUpdate(year,starved,immigrants,population,harvest,bushels_per_acre,rats_ate,bushels_in_storage,acres_owned,cost_per_acre,plague_deaths)
		#update
		buy_land=ask_to_buy_land(bushels_in_storage, cost_per_acre)
		bushels_in_storage=bushels_in_storage-cost_per_acre*buy_land
		if buy_land==0:
			sell_land=ask_to_sell_land(acres_owned)
			bushels_in_storage=bushels_in_storage+cost_per_acre*sell_land
		feed=ask_to_feed(bushels_in_storage)
		bushels_in_storage=bushels_in_storage-feed
		cultivate=ask_to_cultivate(acres_owned, population, bushels_in_storage)
		bushels_in_storage=bushels_in_storage-2*cultivate
		starved=numStarving(population, feed)
		if float(starved)/population>0.45:
			print "\n######################################################\n"
			print "You are a fatuous and self-indulgent ruler! Game Over!"
			print "\n######################################################\n"
			break
		immigrants=numImmigrants(acres_owned, bushels_in_storage, population, starved)
		plague_deaths=int(round(isPlague()*0.5*population))
		population=population-starved+immigrants-plague_deaths
		bushels_per_acre=getHarvest()
		if buy_land==0:
			acres_owned=acres_owned-sell_land
		else: acres_owned=acres_owned+buy_land
		harvest=bushels_per_acre*cultivate
		rats_ate=bushels_in_storage*doRatsInfest()
		bushels_in_storage=bushels_in_storage-rats_ate+harvest
		cost_per_acre=priceOfLand()
		year+=1
	
	if year==11:
		print "\n######################################################\n"
		print "Congratulations! You are a winner!"
		print "\n######################################################\n"

if __name__=='__main__':
	#PrintIntro()
	import sys,random
	Hammurabi()


