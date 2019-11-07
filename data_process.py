import csv

def parse_semester(semester_text):
    # Binary representation of semester, 0 means slot taken and 1 means available,
    # two courses must not overlap on taken slots if their time are also the same.
    if semester_text == '1st half':
        return 1
    elif semester_text == '2nd half':
        return 2
    return 0

def parse_day(day_text):
    day_mapping = {
        'M': [1],
        'T': [2],
        'W': [3],
        'Th': [4],
        'S': [6],
        'MW': [1, 3],
        'TTh': [2, 4],
    }
    return day_mapping[''.join(day_text.split(','))]

def parse_time(begin_time_text, end_time_text):
    # Convert time range to an integer for easier overlap detection.
    def parse_12h_time(time_text):
        hm_text, ampm = time_text.split(' ') 
        hour, minute = [int(hm) for hm in hm_text.split(':')]
        if ampm == 'PM' and hour < 12:
            hour += 12
        return hour * 100 + minute
    return parse_12h_time(begin_time_text), parse_12h_time(end_time_text) 

def read_schedule():
    class_infos = []
    with open('data/elective_schedule.csv') as elective_schedule:
        reader = csv.DictReader(elective_schedule)
        for row in reader:
            class_info = {
                'id': row['Course'],
                'unit': float(row['Units']),
                'semester': parse_semester(row['Sem']),
                'day': parse_day(row['Days']),
                'time': parse_time(row['Begin Time'], row['End Time']),
                'capacity': 0 if not row['FT 1st '] else int(row['FT 1st ']),
            }
            class_infos.append(class_info)
    return class_infos

if __name__ == '__main__':
    print(read_schedule())