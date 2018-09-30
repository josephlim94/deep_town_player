
# import the mining module
import mining
# import crafting module
# import smelting module
import smelting

# score calculation module
from score_calculator import calculate_score

# create a set of variable that conforms to all rules defined by modules
mining_station1 = mining.MiningFloor()
mining_station1.set_location(1)
mining_station2 = mining.MiningFloor()
mining_station2.set_location(2)
mining_station3 = mining.MiningFloor()
mining_station3.set_location(3)

mining_station4 = mining.ChemistryMining()
mining_station4.set_location(4)

mining_station5 = mining.OilMining()
mining_station5.set_location(5)

# another set of variable for crafting stations
smelting_pot1 = smelting.SmeltingPot()
smelting_pot1.set_name(smelting.craftables[0])
smelting_pot2 = smelting.SmeltingPot()
smelting_pot2.set_name(smelting.craftables[0])
smelting_pot3 = smelting.SmeltingPot()
smelting_pot3.set_name(smelting.craftables[1])
smelting_pot4 = smelting.SmeltingPot()
smelting_pot4.set_name(smelting.craftables[0])

# pass in dataset to mining module
engine1 = mining.MiningEngine()
engine1.set_mining_station(mining_station1)
engine1.set_mining_station(mining_station2)
engine1.set_mining_station(mining_station3)
engine1.set_chemistry_mining(mining_station4)
engine1.set_oil_mining(mining_station5)

# pass in data to crafting module
smelting_floor = smelting.SmeltingFloor()
smelting_floor.set_smelting_pot(smelting_pot1)
smelting_floor.set_smelting_pot(smelting_pot2)
smelting_floor.set_smelting_pot(smelting_pot3)
smelting_floor.set_smelting_pot(smelting_pot4)

# obtain score in gold per second (gps)
mining_floor_data = engine1.get_production_rate()
'''
score_gps = 0
for key in score1:
    score_gps += score1[key].rate*float(score1[key].price)/60
print("Gold per second: " + str(score_gps))
'''

# get production data of mining floor
# get production data of smelting floor
smelting_prod_data = smelting_floor.get_production_rate()
# get production data of crafting floor

# combine all production data
all_production_data = {**mining_floor_data, **smelting_prod_data}

# calculate final score from all production data
final_score = calculate_score(all_production_data)

# tweak the set and repeat
mining_station1.set_location(1)
mining_station2.set_location(2)
mining_station3.set_location(3)
mining_station4.set_location(4)
mining_station5.set_location(5)

# stop when no higher score can be found for a certain amount of time
