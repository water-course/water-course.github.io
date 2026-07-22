import random
from datetime import datetime

participants = [
    {"name": "Ryan Campbell", "paper": "chaussard2014.pdf"},
    {"name": "Milou De Jong", "paper": "chutbert2019.pdf"},
    {"name": "Ethan Dunkley", "paper": "condon2020.pdf"},
    {"name": "Sophie Simpson", "paper": "dalin2017.pdf"},
    {"name": "Ahmad Surosh Yousufzai", "paper": "famiglietti2011.pdf"},
    {"name": "Crystal Yan", "paper": "feng2018.pdf"},
    {"name": "Fred Fifield", "paper": "frappart2018.pdf"},
    {"name": "Charlie Tapsfield", "paper": "gleeson2012.pdf"},
    {"name": "Stephan Kashkarov", "paper": "gleeson2016.pdf"},
    {"name": "Savannah Easterby-W...", "paper": "glenn2011.pdf"},
    {"name": "Tara Glover", "paper": "hahnlein2013.pdf"},
    {"name": "Ben McFadden", "paper": "ketabchi2016.pdf"},
    {"name": "Sheryl Shankar", "paper": "lapworth2012.pdf"},
    {"name": "Michael James Yake", "paper": "long2013.pdf"},
    {"name": "Alliya Alvaran", "paper": "meixner2016.pdf"},
    {"name": "Bradley Gardiner", "paper": "mueller2016.pdf"},
    {"name": "Sarah Meixner", "paper": "pfeffer2014.pdf"},
    {"name": "Maya Taib", "paper": "podgorski2020.pdf"},
    {"name": "Max Rechner Thomas", "paper": "reager2016.pdf"},
    {"name": "Justin Mann", "paper": "richey2015.pdf"},
    {"name": "Saskia Lai Butler", "paper": "rodell2018.pdf"},
    {"name": "Declan Pascoe", "paper": "song2019.pdf"},
    {"name": "Ciara Wilson", "paper": "taylor2012.pdf"},
    {"name": "Josie Lemm", "paper": "veit2016.pdf"},
    {"name": "Lily Delves", "paper": "wada2012.pdf"}
]

# Define time slots (8 hours × 4 quarters = 32 slots across 2 weeks)
time_slots = [
    # WEEK 1
    # Monday 9-10
    {"day": "Monday (Week 1)", "time": "9:00-9:15", "slot": 1},
    {"day": "Monday (Week 1)", "time": "9:15-9:30", "slot": 2},
    {"day": "Monday (Week 1)", "time": "9:30-9:45", "slot": 3},
    {"day": "Monday (Week 1)", "time": "9:45-10:00", "slot": 4},

    # Wednesday 11-12
    {"day": "Wednesday (Week 1)", "time": "11:00-11:15", "slot": 5},
    {"day": "Wednesday (Week 1)", "time": "11:15-11:30", "slot": 6},
    {"day": "Wednesday (Week 1)", "time": "11:30-11:45", "slot": 7},
    {"day": "Wednesday (Week 1)", "time": "11:45-12:00", "slot": 8},

    # Thursday 12-13
    {"day": "Thursday (Week 1)", "time": "12:00-12:15", "slot": 9},
    {"day": "Thursday (Week 1)", "time": "12:15-12:30", "slot": 10},
    {"day": "Thursday (Week 1)", "time": "12:30-12:45", "slot": 11},
    {"day": "Thursday (Week 1)", "time": "12:45-13:00", "slot": 12},

    # Thursday 17-18
    {"day": "Thursday (Week 1)", "time": "17:00-17:15", "slot": 13},
    {"day": "Thursday (Week 1)", "time": "17:15-17:30", "slot": 14},
    {"day": "Thursday (Week 1)", "time": "17:30-17:45", "slot": 15},
    {"day": "Thursday (Week 1)", "time": "17:45-18:00", "slot": 16},

    # WEEK 2
    # Monday 9-10
    {"day": "Monday (Week 2)", "time": "9:00-9:15", "slot": 17},
    {"day": "Monday (Week 2)", "time": "9:15-9:30", "slot": 18},
    {"day": "Monday (Week 2)", "time": "9:30-9:45", "slot": 19},
    {"day": "Monday (Week 2)", "time": "9:45-10:00", "slot": 20},

    # Wednesday 11-12
    {"day": "Wednesday (Week 2)", "time": "11:00-11:15", "slot": 21},
    {"day": "Wednesday (Week 2)", "time": "11:15-11:30", "slot": 22},
    {"day": "Wednesday (Week 2)", "time": "11:30-11:45", "slot": 23},
    {"day": "Wednesday (Week 2)", "time": "11:45-12:00", "slot": 24},

    # Thursday 12-13
    {"day": "Thursday (Week 2)", "time": "12:00-12:15", "slot": 25},
    {"day": "Thursday (Week 2)", "time": "12:15-12:30", "slot": 26},
    {"day": "Thursday (Week 2)", "time": "12:30-12:45", "slot": 27},
    {"day": "Thursday (Week 2)", "time": "12:45-13:00", "slot": 28},

    # Thursday 17-18
    {"day": "Thursday (Week 2)", "time": "17:00-17:15", "slot": 29},
    {"day": "Thursday (Week 2)", "time": "17:15-17:30", "slot": 30},
    {"day": "Thursday (Week 2)", "time": "17:30-17:45", "slot": 31},
    {"day": "Thursday (Week 2)", "time": "17:45-18:00", "slot": 32},
]


def assign_presentations():
    """Randomly assign students to presentation time slots"""
    # Make a copy of participants to shuffle
    shuffled_participants = participants.copy()
    random.shuffle(shuffled_participants)

    # Create assignments
    assignments = []

    # Assign students to available slots
    for i, participant in enumerate(shuffled_participants):
        if i < len(time_slots):
            assignment = {
                "student": participant["name"],
                "paper": participant["paper"],
                "day": time_slots[i]["day"],
                "time": time_slots[i]["time"],
                "slot": time_slots[i]["slot"]
            }
            assignments.append(assignment)
        else:
            # Handle extra students if any
            print(f"Warning: {participant['name']} could not be assigned (no available slots)")

    return assignments


def print_schedule(assignments):
    """Print the presentation schedule in a readable format"""
    print("=" * 80)
    print("PRESENTATION SCHEDULE")
    print("=" * 80)

    current_day = ""
    for assignment in assignments:
        if assignment["day"] != current_day:
            current_day = assignment["day"]
            print(f"\n{current_day.upper()}")
            print("-" * 40)

        print(f"{assignment['time']:>12} | {assignment['student']:<25} | {assignment['paper']}")

    print("\n" + "=" * 80)
    print(f"Total presentations scheduled: {len(assignments)}")
    print(f"Available time slots: {len(time_slots)}")


def save_schedule_to_file(assignments, filename="presentation_schedule.txt"):
    """Save the schedule to a text file"""
    with open(filename, 'w') as f:
        f.write("PRESENTATION SCHEDULE\n")
        f.write("=" * 80 + "\n\n")

        current_day = ""
        for assignment in assignments:
            if assignment["day"] != current_day:
                current_day = assignment["day"]
                f.write(f"\n{current_day.upper()}\n")
                f.write("-" * 40 + "\n")

            f.write(f"{assignment['time']:>12} | {assignment['student']:<25} | {assignment['paper']}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Total presentations scheduled: {len(assignments)}\n")
        f.write(f"Available time slots: {len(time_slots)}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    # Set random seed for reproducibility (remove this line for truly random assignments)
    # random.seed(42)

    # Generate random assignments
    schedule = assign_presentations()

    # Print the schedule
    print_schedule(schedule)

    # Save to file
    save_schedule_to_file(schedule)
    print("\nSchedule saved to 'presentation_schedule.txt'")

    # Show some statistics
    if len(participants) > len(time_slots):
        print(f"\nNote: You have {len(participants)} students but only {len(time_slots)} time slots.")
        print(f"{len(participants) - len(time_slots)} students could not be assigned.")
    elif len(participants) < len(time_slots):
        print(f"\nNote: You have {len(time_slots)} time slots but only {len(participants)} students.")
        print(f"{len(time_slots) - len(participants)} time slots will remain empty.")
