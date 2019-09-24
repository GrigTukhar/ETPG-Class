import json
import time

answers = ("check", "exit")
days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
times = ("morning", "lunch", "day", "evening", "exit")

class athlete:

    def __init__(self):
        pass

    @classmethod
    def loadData(cls):
        with open('main.json') as data_file:
            schedule = json.load(data_file)
        return schedule

    @classmethod
    def loadDataForWeekAndDay(cls,full_schedule, week, day):
        week_schedule = full_schedule["schedule"][week][day]
        if (week_schedule["morning"] == -1) and (week_schedule["lunch"] == -1) and (week_schedule["day"] == -1) and (
                week_schedule["evening"] == -1):
            return (0)
        return (week_schedule)

    @classmethod
    def loadPredef(cls):
        with open('main.json') as data_file:
            predata = json.load(data_file)
        preworkouts = predata["workouts"]
        return (preworkouts)

    @classmethod
    def loadFeedback(cls):
        with open('feedback.json') as data_file:
            preFeedback = json.load(data_file)
        return (preFeedback)

    @classmethod
    def currDay(cls,schedule, day, preworkouts):
        if schedule == 0:
            return 0
        curr_work = {day: {}}
        for key in schedule:
            if (schedule[key] != -1 and "predefinedworkout" in schedule[key].keys()):
                curr_work[day][key] = preworkouts[schedule[key]["predefinedworkout"]]
            else:
                curr_work[day][key] = schedule[key]
        return curr_work

    @classmethod
    def saveWorkouts(cls,workouts):
        if workouts == 0:
            file = open("current_workouts.json", "w")
            file.write('{"info": "No workouts set for today"}')
            file.close()
        else:
            file = open("current_workouts.json", "w")
            file.write(json.dumps(workouts))
            file.close()

    @classmethod
    def printWorkouts(cls,curr_work, week, day):
        if curr_work != 0:
            print("\nShowing workouts for |", week, ",", day)
            for key in curr_work[day]:
                if curr_work[day][key] == -1:
                    print(key, ":", "no excerisize for this time of day")
                else:
                    print(key, ":", curr_work[day][key]["type"], "for", curr_work[day][key]["minutes"], "minutes and",
                          curr_work[day][key]["distance"], "kilometers, at a", curr_work[day][key]["load"], "load")

    @classmethod
    def feedback(cls,curr_work, day, week, preFeedback):
        answer = "x"
        time_answer = "x"
        date = time.time()
        feedback_work = preFeedback
        if curr_work != 0:
            while (answer != "no"):
                answer = input("\nWould you like to provide feedback for a workout? yes/no: ")
                if (answer != "yes" and answer != "no"):
                    print("Invalid input, try again")
                elif (answer == "yes"):
                    while time_answer not in times or time_answer != exit:
                        time_answer = input(
                            "\nChoose one of the following options for " + day + " in " + week + " (" + (", ").join(
                                times) + "): ")
                        if time_answer not in times:
                            print("That does not exist, try again")
                        elif time_answer == "exit":
                            return 0
                        else:
                            if curr_work[day][time_answer] == -1:
                                print("No workout for this time of day, cannot provide feedback")
                            else:
                                ifDone = "x"
                                while (ifDone != "yes" and ifDone != "no"):
                                    ifDone = str(input("Have you completed the workout? yes/no: "))
                                    if (ifDone != "yes" and ifDone != "no"):
                                        print("Invalid input, try again")
                                text_feedback = input(
                                    "Input feedback (if you did the workout how you felt, if not why): ")
                                feedback_work[date] = {
                                    week: {day: {time_answer: {}, "hasCompleted": {}, "feedback": {}}}}
                                feedback_work[date][week][day][time_answer] = curr_work[day][time_answer]
                                feedback_work[date][week][day]["hasCompleted"] = ifDone
                                feedback_work[date][week][day]["feedback"] = text_feedback
                                feedback_work[date][week][day]["resolved"] = "no"
                                file = open("feedback.json", "w")
                                file.write(json.dumps(feedback_work))
                                file.close()
                                print("\nFeedback added for", time_answer, "during", day, "in", week)
        else:
            print("No workouts set for today")


def main():

    full_schedule = athlete.loadData()
    answer = "x"
    while (answer not in answers) or  answer != "exit":
        answer = str(input("\nAthlete Menu | What would you like to do with the schedule (" + (", ").join(answers) + "): "))
        if (answer not in answers):
            print("Invalid input, try again")
        elif(answer == "check"):
            week = "x"
            while week not in full_schedule["schedule"].keys():
                week = input(str("\nInput week (" + (", ").join(full_schedule["schedule"].keys()) + "): "))
                if week not in full_schedule["schedule"].keys():
                    print("That does not exist, try again")
                else:
                    day ="x"
                    while day not in days:
                        day = input(str("Input day (" + (", ").join(days) + "): "))
                        print("")
                        if day not in days:
                            print("That does not exist, try again")
                        else:
                            week_schedule =athlete.loadDataForWeekAndDay(full_schedule,week,day)
                            preWorkouts = athlete.loadPredef()
                            preFeedback = athlete.loadFeedback()
                            current_workout = athlete.currDay(week_schedule,day,preWorkouts)
                            athlete.saveWorkouts(current_workout)
                            athlete.printWorkouts(current_workout,week,day)
                            athlete.feedback(current_workout,day,week,preFeedback)

