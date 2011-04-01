echo '!!!Oversikt over antall ord i de semantiske settene (noen ord er med i flere sett):' > Sem_sett_stat.jspwiki
echo '!!HUMAN:' >> Sem_sett_stat.jspwiki
wc -l Sem_PEOPLE.jspwiki Sem_ACTOR.jspwiki Sem_MYTH_HUMAN.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!RELATIVES:' >> Sem_sett_stat.jspwiki
wc -l  RELATIVES.jspwiki Sem_FAMILY.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!WORKERS:' >> Sem_sett_stat.jspwiki
wc -l  WORKERS.jspwiki Sem_PROFESSION.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!HUMAN_DOING:' >> Sem_sett_stat.jspwiki
wc -l  HUMAN_DOING.jspwiki Sem_HUMAN_V.jspwiki Sem_HUMAN_A.jspwiki Sem_EXPERIENCE_A.jspwiki Sem_VERBAL_V.jspwiki Sem_EXPERIENCE_V.jspwiki Sem_AUX_V.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!FOOD/DRINK:' >> Sem_sett_stat.jspwiki
wc -l  FOOD/DRINK.jspwiki Sem_FOOD_GROCERY.jspwiki Sem_FOOD_DISH.jspwiki Sem_FOOD_OTHER.jspwiki Sem_DRINK.jspwiki Sem_FOOD_DRINK_V.jspwiki Sem_SOUP_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!ANIMAL:' >> Sem_sett_stat.jspwiki
wc -l  ANIMAL.jspwiki Sem_ANIMAL_DOM.jspwiki Sem_ANIMAL_WILD.jspwiki Sem_ANIMAL_PET.jspwiki Sem_ANIMAL_OTHER.jspwiki Sem_ANIMAL_V.jspwiki Sem_ANIMAL_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!BIRD_FISH:' >> Sem_sett_stat.jspwiki
wc -l  BIRD_FISH.jspwiki Sem_BIRD.jspwiki Sem_FISH.jspwiki Sem_BIRD_FISH_OTHER.jspwiki Sem_BIRD_FISH_V.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!OBJECT:' >> Sem_sett_stat.jspwiki
wc -l  OBJECT.jspwiki Sem_TOOL.jspwiki Sem_THING.jspwiki Sem_KITCHEN.jspwiki Sem_BATHROOM.jspwiki Sem_SLEEPINGROOM.jspwiki Sem_CONTAINER.jspwiki Sem_OBJECT_V.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!CONCRETES:' >> Sem_sett_stat.jspwiki
wc -l  CONCRETES.jspwiki Sem_CONTAINER.jspwiki Sem_INSTRUMENT.jspwiki Sem_EXPOSURE_V.jspwiki Sem_OBJECT_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!BODY:' >> Sem_sett_stat.jspwiki
wc -l  BODY.jspwiki Sem_BODYPART.jspwiki Sem_BODYPART_PL.jspwiki Sem_ILLNESS.jspwiki Sem_BODY_V.jspwiki Sem_BODY_A.jspwiki Sem_BODY_ADV.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!CLOTHES:' >> Sem_sett_stat.jspwiki
wc -l  CLOTHES.jspwiki Sem_CLOTHING.jspwiki Sem_CLOTHING_PL.jspwiki Sem_CLOTHING_OTHER.jspwiki Sem_CLOTHES_V.jspwiki Sem_CLOTHES_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!BUILDINGS/ROOMS:' >> Sem_sett_stat.jspwiki
wc -l  BUILDINGS/ROOMS.jspwiki Sem_BUILDING.jspwiki Sem_ROOM.jspwiki Sem_ROOM_PART.jspwiki Sem_ROOM_OTHER.jspwiki Sem_SHOP.jspwiki Sem_CONSTRUCTION.jspwiki Sem_FURNITURE.jspwiki Sem_BUILDING_ROOM_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!NATUREWORDS:' >> Sem_sett_stat.jspwiki
wc -l  NATUREWORDS.jspwiki Sem_NATURE.jspwiki Sem_NATURE_WATER.jspwiki Sem_NATURE_PLACE.jspwiki Sem_NATURE_OTHER.jspwiki Sem_NATURE_V.jspwiki Sem_NATURE_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!PLANTS:' >> Sem_sett_stat.jspwiki
wc -l  PLANTS.jspwiki Sem_PLANT.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!WEATHERTYPES:' >> Sem_sett_stat.jspwiki
wc -l  WEATHERTYPES.jspwiki Sem_WEATHER.jspwiki Sem_WEATHER_V.jspwiki Sem_WEATHER_A.jspwiki Sem_SNOW.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!LEISURETIME/AT_HOME:' >> Sem_sett_stat.jspwiki
wc -l  LEISURETIME/AT_HOME.jspwiki Sem_ARRANGEMENT.jspwiki Sem_SPORT.jspwiki Sem_HOME_ACTIVITY.jspwiki Sem_CHRISTMAS.jspwiki Sem_SLIDE_TOOL.jspwiki Sem_TOY.jspwiki Sem_LEISURETIME_HOME_V.jspwiki Sem_SHOW.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!TRAVEL:' >> Sem_sett_stat.jspwiki
wc -l  TRAVEL.jspwiki Sem_PLACE_NAME.jspwiki Sem_PLACE_COUNTRY.jspwiki Sem_PLACE_NATURE.jspwiki Sem_PLACE_STAYING.jspwiki Sem_PLACE_OTHER.jspwiki Sem_PLACE_LOCAL.jspwiki Sem_TRAVELLING.jspwiki Sem_VEHICLE.jspwiki Sem_ROAD.jspwiki Sem_TRAVEL_V.jspwiki Sem_MOVEMENT_V.jspwiki Sem_MOVEMENT_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!ABSTRACTS:' >> Sem_sett_stat.jspwiki
wc -l  ABSTRACTS.jspwiki Sem_FEELING.jspwiki Sem_THOUGHT.jspwiki Sem_ACTION.jspwiki Sem_ACTION_V.jspwiki Sem_ABSTRACT.jspwiki Sem_SOUND.jspwiki Sem_AMOUNT.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!WORK/ECONOMY/TOOLS:' >> Sem_sett_stat.jspwiki
wc -l  WORK/ECONOMY/TOOLS.jspwiki Sem_JOB.jspwiki Sem_ORGANIZATION.jspwiki Sem_FINANCE.jspwiki Sem_TOOL.jspwiki Sem_WORK_ECONOMY_V.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!TIMEEXPRESSIONS:' >> Sem_sett_stat.jspwiki
wc -l  TIMEEXPRESSIONS.jspwiki Sem_TIME.jspwiki Sem_TIME_V.jspwiki Sem_TIME_A.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!LITERATURE/TEXT:' >> Sem_sett_stat.jspwiki
wc -l  LITERATURE/TEXT.jspwiki Sem_TEXT.jspwiki Sem_LANGUAGE.jspwiki Sem_LANGUAGEPART.jspwiki Sem_ISSUE_adj.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!SCHOOL/EDUCATION:' >> Sem_sett_stat.jspwiki
wc -l  SCHOOL/EDUCATION.jspwiki Sem_SCHOOL.jspwiki Sem_EDUCATION.jspwiki Sem_SCHOOL_V.jspwiki Sem_SCHOOL_A.jspwiki Sem_SCHOOL_ADV.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!REINDEER/HERDING:' >> Sem_sett_stat.jspwiki
wc -l  REINDEER/HERDING.jspwiki Sem_HERDING.jspwiki Sem_REINDEER.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!TRADITIONAL:' >> Sem_sett_stat.jspwiki
wc -l  TRADITIONAL.jspwiki Sem_GAMME.jspwiki Sem_FISHING.jspwiki Sem_TRAD_OBJECT.jspwiki Sem_TRAD_OTHER.jspwiki Sem_TRAD_FOOD.jspwiki Sem_TRAD_CLOTHING.jspwiki Sem_VUEKIE.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!DUEDTIE:' >> Sem_sett_stat.jspwiki
wc -l  DUEDTIE.jspwiki Sem_VÆTNOE.jspwiki Sem_HANDICRAFTS.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!MULTIWORD:' >> Sem_sett_stat.jspwiki
wc -l  MULTIWORD.jspwiki Sem_EXPRESSIONS.jspwiki Sem_TIME_U.jspwiki | sed 's/    /* /' >> Sem_sett_stat.jspwiki
echo '!!ACTIVITY_V:' >> Sem_sett_stat.jspwiki
wc -l   Sem_ACTIVITY_V.jspwiki   >> Sem_sett_stat.jspwiki
