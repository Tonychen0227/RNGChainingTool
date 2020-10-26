# RNG Seed Chaining Tool

Special Thanks to: [PokeFinder](https://github.com/Admiral-Fish/PokeFinder), [RNGReporter](https://github.com/Admiral-Fish/RNGReporter), [werster](https://www.twitter.com/wersterlobe)

Only Diamond/Pearl/Platinum supported (no PKRS in Diamond/Pearl). HG/SS perhaps if enough interest.

## How to use
1. You may choose to compile this using `pyinstaller` and then executing `pyinstaller --onefile main.py`
     * You may also choose to simply run `python main.py` (there are no outside dependencies)
2. Think about what mons you want to RNG manipulate (only works for Diamond, Pearl, Platinum)
3. Three types of queries you can chain together, see query information below to read more.
4. Type in a `file_name` and Save to save your query to a JSON, and load it upon next application launch to fill in where you left off.
     * Accidental saves might happen. When you save backups will be created!
5. After adding in your queries, click "Start Search!". Pay attention to the error message entry in the bottom left.
6. If the application freezes, **that's expected**! It's chugging away. In the same directory, you will notice 1 or 2 new CSV being created
     * The "_progress" csv will tell you every 100 checks: how many seeds it has checked, how many remain to be checked, estimated ETA in seconds
     * The other csv will contain successful seeds, along with the frames at which each query was fulfilled. So if you see bugs, please send me that file as well as your saved query.

Note: Seeds are 0 indexed. What this means is that "603" in the report actually means 604. That also means if you search for [400, 600] in frame range, It will actually search [401, 601].

### Querying instructions
* General information
  * All filters are INCLUSIVE (e.g. between 20 and 30 produces 20, 21, 22, ...., 29, 30)
  * Leave a field blank if you don't care about the result
  * Label has no functional use, with the exception of when you are going to use Synchronize.
  * Separate lists by `/` (e.g. you can query for natures `Jolly/Adamant/Brave`)
* Method 1 - Stationary Encounters
  * Input the RNG frame you want to encounter this, along with other parameters you would like.
  * All fields are optional, except `min_frame` and `max_frame`
  * Can leave a field blank if you do not want it to be queried
* Method J - Wild Encounters
  * Input the RNG frame you want to encounter this, along with other parameters you would like.
  * All fields are optional, except `min_frame`, `max_frame`, `enc_rate`, `movement_rate`
    * enc_rate is 10 in caves/water, 30 in grass
    * movement_rate is 40 on foot or surfing, 70 if you have a bike (70 produces more hits, so do 70 if you have bike)
  * One of is_grass and is_surfing must be checked.
  * Important: if you choose to use synchronize, you must input the label of the Pokemon that is to have synchronize
    * e.g. To use MethodJ encounter named "Abra" has ability "Synchronize" as your synchronize lead, the synchronize label must be "Abra"
* PKRS (Pokerus)
  * Input the RNG frame range you want to have Pokerus. Script returns if any of the frame Primary RNG calls are "4000", "8000" or "C000" (TY werster)
  
## Other interesting notes

* Surfing levels and Cute Charm are NOT implemented! 
* Also not implemented: does not check if frame before an encounter is a SKIP
* Year is actually nearly trivial. Delay gets added by 1 for every year above 2000 you currently are. 
  * E.g. if seed K calls for 2000/1/1 15:00:00 Delay 5, you can also hit seed K at 2001/1/1 15:00:00 Delay 4
* To use item determinator: if pokemon can hold Lucky Egg with 5% chance, you want item determin to be >= 95
  * Generally: if Pokemon can hold item A with x%, you want item determin to be >= (100 - x)
  * NOTE: if Pokemon can hold two items A with x% and B with y% where y < x, you want item determin to be: (100 - x) <= x <= (100 - y)
* DemoPlat is there for you to get familiar with the system. This contains a trivial, backwards search based on [werster's Plat Tenta Any% Route](https://drive.google.com/file/d/1MfYngPEStkXIo8GD9HFsY6xy2R8Y-RJj/view)

Please feel free to find me at xSLAY3RL0Lx#0630 on Discord if you see issues. 