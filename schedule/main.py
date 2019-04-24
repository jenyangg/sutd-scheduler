    
import random, copy
import time
from Classes import Group, Professor, CourseClass, Room, Slot
from math import ceil, log2
import math
import csv
import db_to_algo as dba
import datetime
from datetime import timedelta 
    
def run():    
    dbh = dba.db_helper(r"C:\Users\jen yang\Desktop\sutd scheduler\220402\django\mysite\db.sqlite3")
    dbh2 = dba.db_helper(r"C:\Users\jen yang\Desktop\sutd scheduler\220402\django\mysite\db.sqlite3")
    dbh2.print_all_columns("formstoadmin_schedulerequest")
    data = dbh.get_columns(["id","title","assigned_professors","class_related","location","pillar","duration","type"],"users_class")
    soft = dbh2.get_columns(['id', 'name', 'course_name', 'class_related','duration', 'lesson_type','preferred_timings', 'approved'  ],"formstoadmin_schedulerequest")
    print(soft)
    #soft = [(1, 'Gemma Roig', 'Introduction to Algorithms', '4CISTD1', '120', 'cohort', 'morning', 1)]
    
    firstday = datetime.date(2019,4,22)
    def db_to_ls():
        new_data = []
        for d in data:
            #print(d)
            new_d = list(d)
            new_data.append(new_d)
        
           
        for i in range(len(new_data)):
            #print(new_data[i])
            new_data[i][2] = new_data[i][2].split(",")
            new_data[i][3] = new_data[i][3].split(",")
            new_data[i][6] = int(float(new_data[i][6]) * 2)
            #print(new_data[i])
        #print(new_data)
         
            count_C = 2
        for i in range(len(new_data)-1):
        
            new_data[0][4] = "CC1"
            if new_data[i][1] == new_data[i+1][1]:
                new_data[i+1][4] = new_data[i][4]
                
            else:
                new_data[i+1][4] = "CC" + str(count_C)
                
        for j in range(len(new_data)):
            if new_data[j][-1] == "LEC" or new_data[j][-1] == "LAB":
                new_data[j][4] = "lt" + str(j) 
            #print(new_data[j])
            
        
        inputls = []
        for i in range(40,51):
            inputls.append(new_data[i])
        
        #return new_data
        return inputls    
    
    inputls = db_to_ls()
    
    for i in range(len(soft)):
        if soft[i][7] == 1:
            for j in range(len(inputls)):
            
            #approve
            
                
                #prof
                
                if soft[i][1] in inputls[j][2]:
                    
                    #course
                    if inputls[j][1] == soft[i][2]:
                        
                        #class
                        if inputls[j][3] == soft[i][3].split():
                            
                            #duration
                            if inputls[j][6] == int(soft[i][4])/30:
                                #type
                                if soft[i][5] == "lecture" and inputls[j][7] == "LEC":
                                    if soft[i][6] == "morning":
                                        inputls[j].append("morning")
                                    elif soft[i][6] == "afternoon":
                                        inputls[j].append("afternoon")
                               
                                elif soft[i][5] == "cohort" and inputls[i][7] == "CBL":
                                    if soft[i][6] == "morning":
                                        inputls[j].append("morning")
                                    elif soft[i][6] == "afternoon":
                                        inputls[j].append("afternoon")
                                else:
                                    if soft[i][6] == "morning":
                                        inputls[j].append("morning")
                                        
                                    elif soft[i][6] == "afternoon":
                                        inputls[j].append("afternoon")
    print(inputls)
                                
                                        
                                
                                
            
    
    #print("data!!!!", new_data)
    
    initial_slots = [Slot([1,2,3,4,5,6,7,8,9,10,11,12,13], 1), Slot([4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 2), Slot([1,2,3,4,5,6,7,8,9], 3),
                  Slot([1,2,3,4,5,6,7,8,9,10,11,12,13], 4), Slot([1,2,3,4,5,6], 5)]
    initial_slots_HASS = [Slot([14,15,16,17,18,19], 1, True), Slot([1,2,3], 2, True),
                  Slot([14,15,16,17,18,19], 4, True), Slot([7,8,9,10], 5, True)]
    initial_slots_other = [Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 1), Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 2), Slot([1,2,3,4,5,6,7,8,9], 3),
                  Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 4), Slot([1,2,3,4,5,6,7,8,9,10], 5)]
    temp = initial_slots + initial_slots_HASS + initial_slots_other
    
    Slot.slots = copy.deepcopy(temp)
    print(initial_slots_HASS)
    given_duration = 0
    for i in range(len(initial_slots)):
        given_duration = given_duration + len(initial_slots[i].block)
    print(given_duration)
    
    max_score = None
    
    cpg = []
    slots = []
    CourseClass.classes = []
    Professor.professors = []
    Group.groups = []
    Room.rooms = []
    bits_needed_backup_store = {}  # to improve performance
    '''
    inputls = [[500051, "CSE", ["Natalie"], ["Cl02"], "CC12","ISTD",3], [500052, "CSE", ["David"], ["Cl03"], "CC12","ISTD",3], [500053, "CSE", ["Natalie"], ["Cl01"], "CC12","ISTD", 3],\
               [500054, "CSE", ["Natalie"], ["Cl02"], "CC12","ISTD",3], [500055, "CSE", ["David"], ["Cl03"], "CC12","ISTD",3], [500056, "CSE", ["Natalie"], ["Cl01"], "CC12","ISTD",3],\
               [500057, "CSE lab", ["Natalie", "David"], ["Cl01", "Cl02", "Cl03"], "lt2", "ISTD", 4, "lab", "morning"], \
               [500031, "ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",3], [500032, "ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",3], [500033, "ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",3]]
    
               ["ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",3],\
               ["ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",4], ["ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",4], ["ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",4],\
               ["P&S lec", ["Tony", "ABC"], ["Cl01", "Cl02", "Cl03"],"lt5", "ISTD", 3, "lecture", "morning"], ["P&S lec", ["Tony", "ABC"], ["Cl01", "Cl02", "Cl03"], "lt5", "ISTD", 3, "lecture", "morning"],\
               ["P&S", ["Tony"], ["Cl01"], "CC12","ISTD",3], ["P&S", ["Tony"], ["Cl02"], "CC12","ISTD",3], ["P&S", ["Tony"], ["Cl03"], "CC12","ISTD",3],\
               ["MICROE", ["zsombor"], ["microe1"], "tt10", "HASS", 4], ["MICROE", ["zsombor"], ["microe2"], "tt10", "HASS", 4],\
               ["MICROE lec", ["zsombor"], ["microe1", "microe2"], "lt4", "HASS", 2, "lecture", "morning"],
               ["urban planning", ["Samsom Lim"], ["urban1"], "tt9", "HASS", 6], ["urban planning", ["Samsom Lim"], ["urban2"], "tt9", "HASS", 6],\
               ["DW", ["Natalie"], ["FC01"], "CC01", "freshmore", 4], ["core design", ["Jackson"], ["ASD01"], "studio01", "ASD", 16]]
    '''
    
    total_duration = 0
    for inp in inputls:
        #print(inp)
        total_duration = total_duration + inp[6]
    print("total duration")
    print(total_duration)  
    
            
    def input_info(): 
    
        for e in inputls:
            if CourseClass.find(e[0], e[1], e[6], e[7]) == -1:
                CourseClass.classes.append(CourseClass(e[0], e[1], e[6], e[5], e[7]))
            if Professor.find(e[2]) == -1:
                Professor.professors.append(Professor(e[2]))
            if Group.find(e[3]) == -1:
                Group.groups.append(Group(e[3]))  
            if Room.find(e[4]) == -1:
                Room.rooms.append(Room(e[4]))
            if "LEC" in e:
                CourseClass.classes[CourseClass.find(e[0], e[1], e[6], e[7])].isLecture = True
            if "LAB" in e:
                CourseClass.classes[CourseClass.find(e[0], e[1], e[6], e[7])].isLab = True
            if "HASS" in e:
                CourseClass.classes[CourseClass.find(e[0], e[1], e[6], e[7])].isHASS = True
            if "morning" in e:
                CourseClass.classes[CourseClass.find(e[0], e[1], e[6], e[7])].isMorning = True
            if "afternoon" in e:
                CourseClass.classes[CourseClass.find(e[0], e[1], e[6], e[7])].isAfternoon = True
    
       
    def get_cpg():
        input_info()
        len1 = len(inputls)
        for i in range(len1):
           cpg.append(CourseClass.find(inputls[i][0], inputls[i][1], inputls[i][6], inputls[i][7]))
           cpg.append(Professor.find(inputls[i][2]))
           cpg.append(Group.find(inputls[i][3]))
           cpg.append(Room.find(inputls[i][4]))
        print("CPG EXISTS")
    
    def bits_needed(x):
        global bits_needed_backup_store
        r = bits_needed_backup_store.get(id(x))
        if r is None:
            r = int(ceil(log2(len(x))))
            bits_needed_backup_store[id(x)] = r
        return max(r, 1)
    
    
    def join_cpg_pair(_cpg):
        res = []
        for i in range(0, len(_cpg), 4):
            res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2] + _cpg[i + 3])
        return res
    
    
    def convert_input_to_bin():
        global cpg, slots, max_score, inputls, max_size
        input_info()
        cpg.clear()
        '''
        cpg = [CourseClass.find("CSE"),Professor.find("Natalie"),Group.find("Cl02"),
               CourseClass.find("CSE"),Professor.find("David"),Group.find("Cl03"),
               CourseClass.find("CSE"),Professor.find("Natalie"),Group.find("Cl01")]
        '''
        get_cpg()
    
        for _c in range(len(cpg)):
            #print(type(_c))
            
            if _c % 4 == 0:  # CourseClass
                cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')       
            elif _c % 4 == 1:  # Professor
                cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
            elif _c % 4 == 2:  # Group
                cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')
            else:
                cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Room.rooms), '0')
    
        cpg = join_cpg_pair(cpg)
    
        max_size = 0
        for s in initial_slots:
            if len(s.block) > max_size:
                max_size = len(s.block)
                
    
        for t in range(len(Slot.slots)):
            slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
    
    
    
    
    def course_bits(chromosome):
        i = 0
    
        return chromosome[i:i + bits_needed(CourseClass.classes)]
    
    
    def professor_bits(chromosome):
        i = bits_needed(CourseClass.classes)
    
        return chromosome[i: i + bits_needed(Professor.professors)]
    
    
    def group_bits(chromosome):
        i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors)
    
        return chromosome[i:i + bits_needed(Group.groups)]
    
    def lt_bits(chromosome):
        i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
            bits_needed(Group.groups)
    
        return chromosome[i:i + bits_needed(Room.rooms)]
    
    def slot_bits(chromosome):
        i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
            bits_needed(Group.groups) + bits_needed(Room.rooms)
    
        return chromosome[i:i + (bits_needed(Slot.slots) * ceil(log2(max_size)))]
    
    
    def slot_clash(a, b):
        if Slot.slots[int(slot_bits(a),2)].day == Slot.slots[int(slot_bits(b),2)].day:
            #print(Slot.slots[int(slot_bits(a),2)].day + " " +Slot.slots[int(slot_bits(b),2)].day)
            for i in range(len(Slot.slots[int(slot_bits(a),2)].block)):
                for j in range(len(Slot.slots[int(slot_bits(b),2)].block)):
                    if Slot.slots[int(slot_bits(a),2)].block[i] == Slot.slots[int(slot_bits(b),2)].block[j]:
                        #print(Slot.slots[int(slot_bits(a),2)].block)
                        #print(Slot.slots[int(slot_bits(b),2)].block)
                        return 1
        return 0
    
    def appropriate_cohort(chromosomes):
        scores = 0   
        max_score = 0
        for i in range(len(chromosomes)-1):
            course_cohort = CourseClass.classes[int(course_bits(chromosomes[i]),2)].code
            cohort_class = Group.groups[int(group_bits(chromosomes[i]),2)].name
            for j in range(i + 1, len(chromosomes)):
                if CourseClass.classes[int(course_bits(chromosomes[j]),2)].code == course_cohort and Group.groups[int(group_bits(chromosomes[j]),2)].name == cohort_class: 
                    max_score = max_score + 1
                    if Slot.slots[int(slot_bits(chromosomes[i]), 2)].day != Slot.slots[int(slot_bits(chromosomes[j]), 2)].day:
                        scores = scores + 1
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score))
        #print("return: " + str(scores/max_score))
        if max_score == 0:
            return 1
        return scores/max_score
    
    def appropriate_slot(chromosomes):
        scores = 0
        max_score = 0
        for _c in chromosomes:
            
            if CourseClass.classes[int(course_bits(_c), 2)].code != "ASD" and\
            CourseClass.classes[int(course_bits(_c), 2)].code != "freshmore":
                max_score = max_score + 1
                if CourseClass.classes[int(course_bits(_c), 2)].isHASS:    
                    if Slot.slots[int(slot_bits(_c), 2)].isHASS:
                        scores = scores + 1
                else: 
                    if Slot.slots[int(slot_bits(_c), 2)].isHASS == False:
                        scores = scores + 1
                
        #print("scores: ", scores)
        #print("max_score: ", max_score)
        #print("return: ", scores/max_score)
        if max_score == 0:
            return 1
        return scores/max_score
        
    def appropriate_lecture(chromosomes):
        scores = 0
        max_score = 0
        for _c in chromosomes:
            if CourseClass.classes[int(course_bits(_c),2)].isLecture:
                #print("course class" + str(Professor.professors[int(professor_bits(_c),2)].name))
                course_code_lec = CourseClass.classes[int(course_bits(_c),2)].code
                #print("course_code" + course_code)
                for _l in chromosomes:
                    course_code_cohort = CourseClass.classes[int(course_bits(_l),2)].code
                    if CourseClass.classes[int(course_bits(_l),2)].isLecture == False and course_code_cohort in course_code_lec:
                        max_score = max_score + 1
                        if Slot.slots[int(slot_bits(_l),2)].day > Slot.slots[int(slot_bits(_c),2)].day:
                            scores = scores + 1
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score))  
        #print("return: " + str(scores/max_score))
        if max_score == 0:
            return 1
        return scores/max_score
                
    def appropriate_lab(chromosomes):
        scores = 0
        max_score = 0
        for _c in chromosomes:
            if CourseClass.classes[int(course_bits(_c),2)].isLab:
                #print(CourseClass.classes[int(course_bits(_c),2)].code)
                course_code = CourseClass.classes[int(course_bits(_c),2)].code
                #print("course_code" + course_code)
                for _l in chromosomes:
                    if CourseClass.classes[int(course_bits(_l),2)].code in course_code and CourseClass.classes[int(course_bits(_l),2)].isLab == False:
                        max_score = max_score + 1
                        if Slot.slots[int(slot_bits(_l),2)].day < Slot.slots[int(slot_bits(_c),2)].day:
                            scores = scores + 1
        #print("scores: ", scores)
        #print("max_score: ", max_score)
        #print("return: ", scores/max_score)
        if max_score == 0:
            return 1
        return scores/max_score
                
    # checks that a faculty member teaches only one course at a time.
    def faculty_member_one_class(chromosome):
        scores = 0
        max_score = 0
        for i in range(len(chromosome) - 1):  # select one cpg pair
            clash = False
            profs = Professor.professors[int(professor_bits(chromosome[i]),2)].name
            for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
                
                if slot_clash(chromosome[i], chromosome[j]):
                    max_score = max_score + 1
                    profs1 = Professor.professors[int(professor_bits(chromosome[j]),2)].name
                    for prof in profs:
                        
                        if prof in profs1:
                            clash = True
                            break
                    if clash == False:
                        scores = scores + 1
    
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score))
        #print("return: " + str(scores/max_score))
        
        if max_score == 0:
            return 1
        return scores/max_score
    
    def room_member_one_class(chromosome):
        scores = 0
        max_score = 0
        for i in range(len(chromosome) - 1):
            for j in range(i + 1, len(chromosome)):
                
                if slot_clash(chromosome[i], chromosome[j]):
                    max_score = max_score + 1
                    if lt_bits(chromosome[i]) != lt_bits(chromosome[j]):
                        scores = scores + 1
                
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score)) 
        #print("return: " + str(scores/max_score))           
        if max_score == 0:
            return 1
        return scores/max_score
    # check that a group member takes only one class at a time.
    def group_member_one_class(chromosomes):
        scores = 0
        max_score = 0
        for i in range(len(chromosomes) - 1):
            clash = False
            grps1 = Group.groups[int(group_bits(chromosomes[i]),2)].name
            for j in range(i + 1, len(chromosomes)):
                
                if slot_clash(chromosomes[i], chromosomes[j]):
                    max_score = max_score + 1
                    grps2 = Group.groups[int(group_bits(chromosomes[j]),2)].name
                    for grp in grps1:
                        if grp in grps2:
                            clash = True
                            break
                    if clash == False:
                        scores = scores + 1
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score))
        #print("return: " + str(scores/max_score))
        if max_score == 0:
            return 1
        return scores/max_score            
    
    
    def check_slots(chromosomes):
        scores = 0  
        max_score = 0
        for _c in chromosomes:
            max_score = max_score + 1
            if CourseClass.classes[int(course_bits(_c),2)].duration == len(Slot.slots[int(slot_bits(_c),2)].block):
                #print("wrong slot" + CourseClass.classes[int(course_bits(_c),2)].code)
                scores = scores + 1
        #print("scores: "+str(scores))
        #print("max_score: "+str(max_score)) 
        #print("return: " + str(scores/max_score))
        if max_score == 0:
            return 1
        return scores/max_score
    
    def check_slot_time(chromosomes):
        scores = 0
        max_score = 0
        for _c in chromosomes:
            if CourseClass.classes[int(course_bits(_c),2)].isMorning:
                max_score = max_score + 1
                if Slot.slots[int(slot_bits(_c),2)].block[0] <= 4:
                    scores = scores + 1
            elif CourseClass.classes[int(course_bits(_c),2)].isAfternoon:
                max_score = max_score + 1
                if Slot.slots[int(slot_bits(_c),2)].block[0] >= 11:
                    scores = scores + 1
        #print("score", scores)
        #print("max score", max_score)
        if max_score == 0:
            return 1
        
        return scores/max_score
            
           
    def random_slot(cpg_c):
        if CourseClass.classes[int(course_bits(cpg_c),2)].isHASS:
            #print(CourseClass.classes[int(course_bits(cpg_c), 2)].code, Group.groups[int(group_bits(cpg_c), 2)].name)
            temp_duration = CourseClass.classes[int(course_bits(cpg_c),2)].duration
            #print(temp_duration)
            temp_slot = random.choice(initial_slots_HASS)
            #print(temp_slot)
    
            while temp_duration > len(temp_slot.block):
                #print(temp_duration)
                #print(len(temp_slot.block))
                #print(temp_duration > len(temp_slot.block))
                temp_slot = random.choice(initial_slots_HASS)
                #print("new", temp_slot)
            #print("finish while loop")
            #print(initial_slots)
            #print(temp_slot)
            temp_block = temp_slot.block
            random_day = temp_slot.day
            #print(CourseClass.classes[int(course_bits(cpg_c),2)])
            
            #print(temp_duration)
            random_start = temp_block[0]
            temp_block = []
            random_end = random_start + int(temp_duration)
            for i in range(random_start, random_end):
                temp_block.append(i)
            random_slot = Slot(temp_block, random_day, True)
            if Slot.find(random_slot.block, random_slot.day) == -1:
                Slot.slots.append(random_slot)
                slots.append((bin(Slot.find(random_slot.block, random_slot.day))[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
            
            return slots[Slot.find(random_slot.block, random_slot.day)]
        
        elif CourseClass.classes[int(course_bits(cpg_c),2)].pillar == "ASD" or CourseClass.classes[int(course_bits(cpg_c),2)].pillar == "freshmore":
            temp_duration = CourseClass.classes[int(course_bits(cpg_c),2)].duration
            #print(temp_duration)
            temp_slot = random.choice(initial_slots_other)
            #print(temp_slot)
    
            while temp_duration > len(temp_slot.block):
                #print(temp_duration)
                #print(len(temp_slot.block))
                #print(temp_duration > len(temp_slot.block))
                temp_slot = random.choice(initial_slots_other)
                #print("new", temp_slot)
            #print("finish while loop")
            #print(initial_slots)
            #print(temp_slot)
            temp_block = temp_slot.block
            random_day = temp_slot.day
            #print(CourseClass.classes[int(course_bits(cpg_c),2)])
            
            #print(temp_duration)
            random_start = random.randint(temp_block[0], temp_block[-1] - temp_duration)
            #print(random_start)
            temp_block = []
            random_end = random_start + int(temp_duration)
            for i in range(random_start, random_end):
                temp_block.append(i)
            random_slot = Slot(temp_block, random_day)
            if Slot.find(random_slot.block, random_slot.day) == -1:
                Slot.slots.append(random_slot)
                slots.append((bin(Slot.find(random_slot.block, random_slot.day))[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
            return slots[Slot.find(random_slot.block, random_slot.day)]
        
        else:
            temp_slot = random.choice(initial_slots)
            #print(temp_slot)
            temp_block = temp_slot.block
            random_day = temp_slot.day
            #print(CourseClass.classes[int(course_bits(cpg_c),2)])
            temp_duration = CourseClass.classes[int(course_bits(cpg_c),2)].duration
            random_start = random.randint(temp_block[0], temp_block[-1] - temp_duration)
            #print(random_start)
            temp_block = []
            random_end = random_start + int(temp_duration)
            for i in range(random_start, random_end):
                temp_block.append(i)
            random_slot = Slot(temp_block, random_day)
            if Slot.find(random_slot.block, random_slot.day) == -1:
                Slot.slots.append(random_slot)
                slots.append((bin(Slot.find(random_slot.block, random_slot.day))[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
            return slots[Slot.find(random_slot.block, random_slot.day)]
    
    def evaluate(chromosomes):
    
        score = 0
        score = score + faculty_member_one_class(chromosomes)
        score = score + room_member_one_class(chromosomes)
        score = score + group_member_one_class(chromosomes)
        score = score + appropriate_cohort(chromosomes)
        score = score + appropriate_lecture(chromosomes)
        score = score + appropriate_lab(chromosomes)
        score = score + check_slots(chromosomes)
        score = score + appropriate_slot(chromosomes)
        return score
    
    def evaluate_softconstraints(chromosomes):
        score = 0
        score = score + check_slot_time(chromosomes)
        
        return score / 1
        
    def cost(solution):
        # solution would be an array inside an array
        # it is because we use it as it is in genetic algorithms
        # too. Because, GA require multiple solutions i.e population
        # to work.
        return 1 / float(evaluate(solution))
    
    def cost_soft(solution):
        
        return 1/ float(evaluate_softconstraints(solution))
    
    def init_population(n):
        global cpg
        chromosomes = []
        for _n in range(n):
            chromosome = []
            for _c in cpg:
                #print(CourseClass.classes[int(course_bits(_c), 2)].code, Group.groups[int(group_bits(_c), 2)].name)
                chromosome.append(_c + random_slot(_c))
    
            chromosomes.append(chromosome)
        return chromosomes
    
    
    # Modified Combination of Row_reselect, Column_reselect
    def mutate(chromosome):
        # print("Before mutation: ", end="")
        # printChromosome(chromosome)
    
        a = random.randint(0, len(chromosome) - 1)
        
        rand_slot = random_slot(chromosome[a])
        
        chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) +\
            group_bits(chromosome[a]) + lt_bits(chromosome[a]) + rand_slot
    
        # print("After mutation: ", end="")
        # printChromosome(chromosome)
    
    
    def crossover(population):
        a = random.randint(0, len(population) - 1)
        b = random.randint(0, len(population) - 1)
        cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
        population.append(population[a][:cut] + population[b][cut:])
        
    
    def selection(population, n):
        population.sort(key=evaluate, reverse=True)
        while len(population) > n:
            population.pop()
    
    
    def print_chromosome(chromosome):
        print(chromosome)
        print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
              Professor.professors[int(professor_bits(chromosome), 2)], " | ",
              Group.groups[int(group_bits(chromosome), 2)], " | ",
              Room.rooms[int(lt_bits(chromosome), 2)], " | ",
              Slot.slots[int(slot_bits(chromosome), 2)])
        
    def print_chromosome_csv(max_chromosomes):
        label = ["id", "Course", "Professors", "Class", "Room", " Day", "Start", "End"]
        out = open('schedule.csv','a', newline='')
        csv_write = csv.writer(out, dialect = 'excel')
        csv_write.writerow(label)
        for i in range(0,14):
            if i != 6:
                print (i)
                for chromosome in max_chromosomes:
                    date = firstday + timedelta(days = (i * 7 + Slot.slots[int(slot_bits(chromosome), 2)].day-1))
                    time = str(Slot.slots[int(slot_bits(chromosome),2)]).split("-")
                    csv_row = [CourseClass.classes[int(course_bits(chromosome), 2)].dbid,\
                               CourseClass.classes[int(course_bits(chromosome), 2)].code,\
                               Professor.professors[int(professor_bits(chromosome), 2)],\
                               Group.groups[int(group_bits(chromosome), 2)],\
                               Room.rooms[int(lt_bits(chromosome), 2)]] +time
                    csv_row.append(date)
                    csv_write.writerow(csv_row)
                    print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
                      Professor.professors[int(professor_bits(chromosome), 2)], " | ",
                      Group.groups[int(group_bits(chromosome), 2)], " | ",
                      Room.rooms[int(lt_bits(chromosome), 2)], " | ",
                      Slot.slots[int(slot_bits(chromosome), 2)], " | ", date)
                    
        
        out.close()
        print("finish csv writing")
                   
    def write_to_db(max_chromosomes):
        db = dba.db_helper("db.sqlite3")
        out = []
        for chromosome in max_chromosomes:
            time = str(Slot.slots[int(slot_bits(chromosome),2)]).split("-")
            data = [CourseClass.classes[int(course_bits(chromosome), 2)].dbid,\
                       Group.groups[int(group_bits(chromosome), 2)],\
                       Room.rooms[int(lt_bits(chromosome), 2)],\
                       Slot.slots[int(slot_bits(chromosome), 2)].day] + time
            out.append(data)
        print(out)
        db.update_db(out)
        print("UPDATED DB")  
    
    # Simple Searching Neighborhood
    # It randomly changes timeslot of a class/lab
    
    def ssn(solution):
    
        a = random.randint(0, len(solution) - 1)
        
        rand_slot = random_slot(solution[a])
        new_solution = copy.deepcopy(solution)
        new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
            group_bits(solution[a]) + lt_bits(solution[a]) + rand_slot 
            
        if(CourseClass.classes[int(course_bits(solution[a]), 2)].duration != len(Slot.slots[int(slot_bits(solution[a]), 2)].block)):
            print("ssn")
        
        return [new_solution]
    
    # Swapping Neighborhoods
    # It randomy selects two classes and swap their time slots
       
    def swn(solution):
        a = random.randint(0, len(solution) - 1)
        b = random.randint(0, len(solution) - 1)
        while CourseClass.classes[int(course_bits(solution[b]), 2)].duration != CourseClass.classes[int(course_bits(solution[a]), 2)].duration:
            b = random.randint(0, len(solution) - 1)
        if CourseClass.classes[int(course_bits(solution[b]), 2)].duration != CourseClass.classes[int(course_bits(solution[a]), 2)].duration:
            print("swn")
        new_solution = copy.deepcopy(solution)
        temp = slot_bits(solution[a])
        new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
            group_bits(solution[a]) + lt_bits(solution[a]) + slot_bits(solution[b])
    
        new_solution[b] = course_bits(solution[b]) + professor_bits(solution[b]) +\
            group_bits(solution[b]) + lt_bits(solution[b]) + temp 
        # print("Diff", solution)
        # print("Meiw", new_solution)
        return [new_solution]
    
    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        else:
            return math.exp((old_cost - new_cost) / temperature)
    
    def simulated_annealing():
        print("\n------------- Simulated Annealing Start--------------\n")
        alpha = 0.9
        T = 0.5
        T_min = 0.00001
        convert_input_to_bin()
        population = init_population(1) # as simulated annealing is a single-state method
        old_cost = cost(population[0])
        # print("Cost of original random solution: ", old_cost)
        # print("Original population:")
        # print(population)
    
        while evaluate(population[0]) != 8.0 or evaluate_softconstraints(population[0]) < 0.3:
            new_solution = swn(population[0])
            new_solution = ssn(population[0])
            new_cost = cost(new_solution[0])
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random.random():
                population = new_solution
                old_cost = new_cost
            T = T * alpha
    
        # print("Cost of altered solution: ", cost(population[0]))
        print("\n------------- Simulated Annealing Result--------------\n")
        out = open('schedule.csv','a', newline='')
        csv_write = csv.writer(out, dialect = 'excel')
        csv_write.writerow(["soft constraints score"])
    
        csv_write.writerow([str(evaluate_softconstraints(population[0]))])
        out.close()
        print_chromosome_csv(population[0])
        write_to_db(population[0])
        print("Score: ", evaluate(population[0]))
        print("Soft score: ", evaluate_softconstraints(population[0]))
    
    def genetic_algorithm():
        generation = 0
        convert_input_to_bin()
    
        population = init_population(3)
    
        # print("Original population:")
        # print(population)
        print("\n------------- Genetic Algorithm --------------\n")
    
        
        while True:
            
            # if termination criteria are satisfied, stop.
            if evaluate(max(population, key=evaluate)) == 8.0 or generation == 500:
                print("Generations:", generation)
                print("Best Chromosome fitness value", evaluate(max(population, key=evaluate)))
                print("Best Chromosome: ", max(population, key=evaluate))
                for lec in max(population, key=evaluate):
                    print_chromosome(lec)
                print("Score: ",evaluate(max(population, key=evaluate)))
                break
            
            # Otherwise continue
            else:
                for _c in range(len(population)):
                    #crossover(population)
                    #selection(population, 5)
                    mutate(population[_c])
    
                    #print("mutate time :" + str(dtime3))
            generation = generation + 1
            # print("Gen: ", generation)
    
        # print("Population", len(population))
    
            
            
            
    def main():
        starttime = time.time()
        print(starttime)
        random.seed()
        #genetic_algorithm()
        startsimu = time.time()
        simulated_annealing()
        endsimu = time.time()
        print("simulation time: ", endsimu - startsimu)
        #print(Slot.slots)
        endtime = time.time()
        dtime = endtime - starttime
        
        print("time take: ",dtime)
    main()
