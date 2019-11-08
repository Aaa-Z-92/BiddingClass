import pandas as pd

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
    df = pd.read_csv('data/elective_schedule.csv')
    df['Units'] = df['Units'].apply(float)
    df['Sem'] = df['Sem'].apply(parse_semester)
    df['Days'] = df['Days'].apply(parse_day)
    df['Times'] = df.apply(lambda row: parse_time(row['Begin Time'], row['End Time']), axis=1)
    df['Capacity'] = df.apply(lambda row: 0 if pd.isna(row['FT 1st']) else int(row['FT 1st']), axis=1)
    return df

if __name__ == '__main__':
    print(read_schedule())